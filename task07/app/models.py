from typing import Union

from pydantic import BaseModel, PositiveInt


class monitoring(BaseModel):
    enabled: str


class cpu(BaseModel):
    enabled: str
    value: str


class Limits(BaseModel):
    cpu: cpu


class monitor_meta(BaseModel):
    monitoring: monitoring
    limits: Limits


class fats(BaseModel):
    saturated_fat: str
    trans_fat: str


class carbohydrates(BaseModel):
    dietary_fiber: str
    sugars: str


class allergens(BaseModel):
    nuts: str
    seafood: str
    eggs: str


class nutrition_meta(BaseModel):
    calories: PositiveInt
    fats: fats
    carbohydrates: carbohydrates
    allergens: allergens


class metadata(BaseModel):
    """ check the schema of metadata is match with monitor and nuttition
    """

    name: str
    metadata: Union[monitor_meta, nutrition_meta]
