from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict

class Link(BaseModel):
    href: HttpUrl
    method: str = "GET"

class Restaurant(BaseModel):
    restaurant_code: str
    name: str
    _links: Dict[str, Link]

class UserProfile(BaseModel):
    user_id: int
    username: str
    viewed_restaurants: Optional[List[Restaurant]] = None

class ViewedRestaurantsUpdate(BaseModel):
    username: str
    viewed_restaurants: List[Restaurant]
