import logging
import sys
from typing import List

import models
from bson.objectid import ObjectId
from config import DB, LOG_LEVEL, SERVE_PORT, close_db_client
from fastapi import Body, FastAPI, HTTPException, Query
from pydantic import PositiveInt

sys.path.append(".")


if SERVE_PORT is not None and SERVE_PORT.isdigit():
    SERVE_PORT = int(SERVE_PORT)
else:
    quit("SERVE_PORT is unknow")


logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("devops")


app = FastAPI()


def validate_object_id(id_: str):
    """ verify the obj type is ObjectId

    :param id_: the document's id in mongo DB
    :raise HTTPException if the id_'s type is not ObjectId
    """
    try:
        _id = ObjectId(id_)
    except Exception:
        raise HTTPException(status_code=400)
    return _id


async def _get_404(id_: str, coll: str):
    """ verify the obj id is exist

    :param id_: the document's id in mongo DB
    :param coll: collection's name
    :raise HTTPException if the id_ is not found
    """
    _id = validate_object_id(id_)
    obj = await DB[coll].find_one({"_id": _id})
    if obj:
        return fix_obj_id(obj)
    else:
        raise HTTPException(status_code=404, detail=f"{_id} not found")


def fix_obj_id(obj):
    """ change the Id's type from ObjectId to string for iterator

    :raise ValueError obj.id not found
    """
    if obj.get("_id", False):
        obj["_id"] = str(obj["_id"])
        return obj
    else:
        raise ValueError(f"No `_id` found! Unable to fix obj ID for obj: {obj}")


@app.on_event("shutdown")
async def app_shutdown():
    close_db_client()


@app.get("/")
async def health_check():
    """ It's application heart beat, to make sure app still alive
    """
    logger.debug(f"Call root URL")
    return {"Running": True}


@app.get("/configs/", response_model=List[models.metadata])
async def list_all(limit: PositiveInt = 10, skip: PositiveInt = 0) -> list:
    """ List all collection's (exclude system's) documents.

    :param limit: limit how many documents list at once in each collection.
    :param skip: skip the first amounts in collections
    :return a list of documents in monitor and nutrition
    """
    logger.debug(f"Call list_all, limit: {limit}, skip: {skip}")
    collections = await DB.list_collection_names(
        filter={"name": {"$regex": r"^(?!system\.)"}}
    )
    ret = []

    for name in collections:
        _cursor = DB[name].find().skip(skip).limit(limit)
        _list = await _cursor.to_list(length=limit)
        ret += _list
    return list(map(fix_obj_id, ret))


@app.post("/configs/", response_model=List[models.metadata])
async def create(bodies: List[models.metadata] = Body(...)):
    """ Add new document into monitor or nutrition collection

    :param bodies: it's mmandatory, it could be monitor or nutrition
    """
    logger.debug(f"Call Create with body: {bodies}")
    ret = []
    for body in bodies:
        if "datacenter" in body.name:
            result = await DB.monitor.insert_one(body.dict())
            if result.inserted_id:
                id_check = await _get_404(result.inserted_id, "monitor")
        elif "nutrition" in body.name:
            result = await DB.nutrition.insert_one(body.dict())
            if result.inserted_id:
                id_check = await _get_404(result.inserted_id, "nutrition")
        ret.append(id_check)

    return ret


@app.get("/configs/{name}", response_model=List[models.metadata])
async def get_by_name(name: str, limit: PositiveInt = 10):
    """ List document by name, it will print all documents in the same collection

    :param name: depend on name to filter the documents
    :return List of documents
    """
    logger.debug(f"Call Get {name}")
    _list = []
    if "datacenter" in name:
        ret_cur = DB.monitor.find({"name": name})
    elif "nutrition" in name:
        ret_cur = DB.nutrition.find({"name": name})
    if ret_cur:
        _list = await ret_cur.to_list(length=limit)
    return _list


@app.put("/configs/{name}", response_model=List[models.metadata])
@app.patch("/configs/{name}", response_model=List[models.metadata])
async def update_by_name(name: str, data: models.metadata):
    """ Updateing one document by name, we have to patch the whole object's info

    :param name: the document's name
    :param data: the updated object's info
    :return The updated object in a list
    :raise HTTPException 404 checking the updated result is faild
    :raise HTTPException 304 not updated
    """
    logger.debug(f"update {name}")
    if "datacenter" in name:
        result = await DB.monitor.update_one({"name": name}, {"$set": data.dict()})
    elif "nutrition" in name:
        result = await DB.nutrition.update_one({"name": name}, {"$set": data.dict()})
    if result.modified_count:
        if "datacenter" in name:
            result = await DB.monitor.find_one({"name": name})
        elif "nutrition" in name:
            result = await DB.nutrition.find_one({"name": name})
        if result:
            return [result]
        else:
            raise HTTPException(status_code=404, detail=f"{name} not found")
    else:
        raise HTTPException(status_code=304)


@app.delete("/configs/{name}", response_model=dict)
async def delete_by_name(name: str):
    """ Delete document by its name, delete one ducument at once

    :return how many document been deleted
    """
    logger.debug(f"delete_by_name {name}")
    if "datacenter" in name:
        result = await DB.monitor.delete_one({"name": name})
    elif "nutrition" in name:
        result = await DB.nutrition.delete_one({"name": name})
    if result.deleted_count:
        return {"status": f"deleted count: {result.deleted_count}"}


@app.get("/search/{metadata_key}={value}", response_model=List[models.metadata])
async def query(metadata_key: str, value: str, limit: PositiveInt = 10):
    """ Query the documents by metadata key

    :param metadata_key: it's filter string, e.g: metadata.allergens.eggs
    :param value: the value of metadata_key
    :return A list of documents from monitor and nutrition collection.
    """
    _filter = {metadata_key: value}
    logger.debug(f"filter: {_filter}")
    _projection = {"_id": False}
    nutrition_cur = DB.nutrition.find(filter=_filter, projection=_projection)
    monitor_cur = DB.monitor.find(filter=_filter, projection=_projection)
    nutrition_list = await nutrition_cur.to_list(length=limit)
    monitor_list = await monitor_cur.to_list(length=limit)
    return nutrition_list + monitor_list
