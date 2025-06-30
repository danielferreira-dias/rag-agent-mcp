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
    restaurants = []
    print(data_dict)
    for data in data_dict:
        restaurants.append(Restaurant(
            name=data["restaurant_name"],
            rating=data["rating"],
            cuisine_type=data["cuisine_type"],
            price_range=pricing_tier[data["price_range"]],
            restaurant_url=data["restaurant_url"],
        ))
    return restaurants

