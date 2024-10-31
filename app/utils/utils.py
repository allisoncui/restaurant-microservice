from typing import Dict
from fastapi import Request
from app.models.restaurant import Link

def generate_restaurant_links(request: Request, restaurant_code: int) -> Dict[str, Link]:
    base_url = request.url_for("get_restaurant", restaurant_code=restaurant_code)
    return {
        "self": Link(href=base_url, method="GET"),
        "update": Link(href=base_url, method="PUT"),
        "delete": Link(href=base_url, method="DELETE"),
        "viewed_restaurants": Link(href=f"{base_url}/viewed_restaurants", method="GET"),
        "add_to_viewed": Link(href=f"{base_url}/viewed_restaurants", method="POST"),
    }
