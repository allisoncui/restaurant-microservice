from typing import Dict
from fastapi import Request
from pydantic import BaseModel


class Link(BaseModel):
    href: str
    method: str

def generate_restaurant_links(request: Request, restaurant_code: int) -> Dict[str, Link]:
    # Build the URLs with full paths and valid TLDs
    self_url = str(request.url_for("get_restaurant", restaurant_code=restaurant_code))
    base_url = str(request.base_url)

    return {
        "self": Link(href=self_url, method="GET"),
        "viewed_restaurants": Link(
            href=f"{base_url}user/{restaurant_code}/viewed_restaurants", method="GET"
        ),
        "add_viewed_restaurants": Link(
            href=f"{base_url}user/{restaurant_code}/viewed_restaurants", method="POST"
        ),
        "update_viewed_restaurants": Link(
            href=f"{base_url}user/{restaurant_code}/viewed_restaurants", method="PUT"
        ),
        "delete_viewed_restaurants": Link(
            href=f"{base_url}user/{restaurant_code}/viewed_restaurants", method="DELETE"
        ),
    }