from src.ingestion.models.models import Restaurant

pricing_tier = {
    "$": "cheap",
    "$-$$": "cheap-moderate",
    "$$": "moderate",
    "$$-$$$": "moderate-expensive",
    "$$$": "expensive",
    "$$$-$$$$": "expensive-luxury",
    "$$$$": "luxury",
}

def process_restaurant_data(data_dict: list[dict]) -> list[Restaurant]:
    for data in data_dict:
        restaurant = Restaurant(
            name=data["restaurant_name"],
            rating=data["rating"],
            cuisine=data["cuisine"],
            price_range=data["price_range"],
            restaurant_url=data["restaurant_url"]
        )

