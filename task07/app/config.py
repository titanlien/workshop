import os

import yaml
from motor.motor_asyncio import AsyncIOMotorClient

SERVE_PORT = os.environ.get("SERVE_PORT")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")


def load_config() -> dict:
    """Load mongo DB configure from config.yml  file"""
    conf = {}
    with open("app/config.yml") as yaml_file:
        conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
    return conf


CONF = load_config()


def _get_client_config():
    conf = CONF
    client_conf = {
        "host": conf.get("databases", {}).get(ENVIRONMENT, {}).get("HOST"),
        "port": int(conf.get("databases", {}).get(ENVIRONMENT, {}).get("PORT")),
        "username": conf.get("databases", {}).get(ENVIRONMENT, {}).get("USER"),
        "password": conf.get("databases", {}).get(ENVIRONMENT, {}).get("PASSWORD"),
    }
    return client_conf


DB_CLIENT = AsyncIOMotorClient(**_get_client_config())

DB = DB_CLIENT[CONF.get("databases", {}).get(ENVIRONMENT, {}).get("NAME")]


def close_db_client():
    DB_CLIENT.close()
