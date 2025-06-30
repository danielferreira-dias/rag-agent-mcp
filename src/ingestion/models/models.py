from typing import List, Optional
from pydantic import BaseModel

class Restaurant(BaseModel):
    name: str
    description: Optional[str]
    address: str
    cuisine_type: Optional[str]
    rating: Optional[float]
    price_range: Optional[str]
    michelin_star: Optional[str]

class Monument(BaseModel):
    name: str
    description: str
    address: str
    rating: Optional[float]
    price_range: Optional[str]

class Porto(BaseModel):
    city: str = "Porto"
    restaurants: List[Restaurant]
    monuments: List[Monument]