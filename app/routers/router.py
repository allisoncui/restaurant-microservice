from fastapi import APIRouter, HTTPException
from app.resources.restaurant_resource import RestaurantResource

router = APIRouter()
restaurant_resource = RestaurantResource(config=db_config)

@router.get("/restaurants", tags=["restaurants"])
async def get_all_restaurants():
    restaurants = restaurant_resource.get_restaurants()
    return {"restaurants": restaurants}

@router.get("/user/{username}/viewed_restaurants", tags=["user"])
async def get_user_viewed_restaurants(username: str):
    user_id = restaurant_resource.get_user_id(username)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")
    
    viewed_restaurants = restaurant_resource.get_viewed_restaurants(user_id)
    return {"username": username, "viewed_restaurants": viewed_restaurants}

@router.post("/user/{username}/viewed_restaurants", tags=["user"])
async def add_viewed_restaurants(username: str, restaurant_codes: list):
    user_id = restaurant_resource.get_user_id(username)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    restaurant_resource.insert_viewed_restaurants(user_id, restaurant_codes)
    return {"message": "Viewed restaurants added successfully"}

@router.delete("/user/{username}/viewed_restaurants", tags=["user"])
async def remove_viewed_restaurants(username: str, restaurant_codes: list):
    user_id = restaurant_resource.get_user_id(username)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    restaurant_resource.remove_viewed_restaurants(user_id, restaurant_codes)
    return {"message": "Viewed restaurants removed successfully"}