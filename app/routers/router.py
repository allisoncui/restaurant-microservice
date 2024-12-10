from fastapi import APIRouter, HTTPException, Request
from app.resources.restaurant_resource import RestaurantResource
from app.models.restaurant import Restaurant
from pydantic import BaseModel
from typing import List
from app.utils.utils import generate_restaurant_links
import logging

router = APIRouter()
restaurant_resource = RestaurantResource(config={})

class RestaurantCodesRequest(BaseModel):
    restaurant_codes: List[str]

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Format of the log message
    handlers=[
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

@router.get("/restaurant/{restaurant_code}")
async def get_restaurant(request: Request, restaurant_code: int):
    # Fetch the restaurant details from the resource
    restaurant = restaurant_resource.get_by_key(restaurant_code)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Generate HATEOAS links
    links = generate_restaurant_links(request, restaurant_code)

    # Return restaurant data along with links
    return {
        "restaurant_code": restaurant.restaurant_code,
        "name": restaurant.name,
        "_links": links  # Add the links here
    }

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
    #print(viewed_restaurants)
    return {"username": username, "viewed_restaurants": viewed_restaurants}

@router.put("/user/{username}/viewed_restaurants", tags=["user"])
async def update_viewed_restaurants(username: str, restaurant: int):
    user_id = restaurant_resource.get_user_id(username)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove all current entries for this user
    #restaurant_resource.remove_viewed_restaurants(user_id)

    # Insert the new list of viewed restaurants
    restaurant_resource.insert_viewed_restaurants(user_id, restaurant)

    return {"message": "Viewed restaurants updated successfully"}

@router.post("/user/{username}/viewed_restaurants", tags=["user"])
async def add_viewed_restaurant(username: str, restaurant_code: int):
    try:
        user_id = restaurant_resource.get_user_id(username)
        if not user_id:
            raise HTTPException(status_code=404, detail="User not found")

        user_id = int(user_id)
        restaurant_code = int(restaurant_code)
        restaurant_resource.insert_viewed_restaurants(user_id, restaurant_code)
        return {"message": f"Restaurant {restaurant_code} added to viewed restaurants."}
    except Exception as e:
        logger.error(f"Error in add_viewed_restaurant: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while adding viewed restaurant.")

@router.delete("/user/{username}/viewed_restaurants", tags=["user"])
async def remove_viewed_restaurant(username: str, restaurant_code: int):
    """
    Remove a single viewed restaurant for the user.
    """
    user_id = restaurant_resource.get_user_id(username)
    if not user_id:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove the single restaurant code
    restaurant_resource.remove_viewed_restaurants(user_id, [restaurant_code])
    return {"message": f"Restaurant {restaurant_code} removed from viewed restaurants."}


@router.get("/restaurant/{restaurant_code}/rating", tags=["restaurants"])
async def get_restaurant_rating(restaurant_code: int):
    rating = restaurant_resource.get_restaurant_rating(restaurant_code)
    if rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return {"rating": rating}
