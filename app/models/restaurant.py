from pydantic import BaseModel
from typing import List, Optional

class Restaurant(BaseModel):
    restaurant_code: str
    name: str

class UserProfile(BaseModel):
    user_id: int
    username: str
    viewed_restaurants: Optional[List[Restaurant]] = None
