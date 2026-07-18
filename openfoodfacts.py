import requests


def fetch_product_by_barcode(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()
        # OpenFoodFacts returns status 1 when product exists
        if data.get("status") != 1:
            return None


        product = data.get("product", {})


        return {
            "product_name": product.get("product_name"),
            "brands": product.get("brands"),
            "categories": product.get("categories"),
            "ingredients_text": product.get("ingredients_text"),
            "image_url": product.get("image_url")
        }


    except requests.exceptions.RequestException:
        return None
    
def fetch_product_by_name(name):
    """
    Search OpenFoodFacts by product name.
    """
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1
    }

    try:

        response = requests.get(
            url,
            params=params
        )

        if response.status_code != 200:
            return None

        data = response.json()
        products = data.get("products", [])
        if len(products) == 0:
            return None
        product = products[0]
        return {
            "product_name": product.get("product_name"),
            "brands": product.get("brands"),
            "categories": product.get("categories"),
            "ingredients_text": product.get("ingredients_text"),
            "image_url": product.get("image_url")
        }


    except requests.exceptions.RequestException:
        return None