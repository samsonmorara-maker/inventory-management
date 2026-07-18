from flask import Flask, jsonify, request
from inventory import inventory
from openfoodfacts import (
    fetch_product_by_barcode,
    fetch_product_by_name
)
app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory API running"
    })

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200

@app.route("/inventory/<int:id>", methods=["GET"])
def get_single_inventory(id):
    item = next(
        (item for item in inventory if item["id"] == id),
        None
    )

    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    return jsonify(item), 200

@app.route("/inventory", methods=["POST"])
def create_inventory():
    data = request.get_json()
    if "barcode" not in data:
        return jsonify({
            "error": "Barcode is required"
        }), 400
    # Get product details from OpenFoodFacts
    api_product = fetch_product_by_barcode(
        data["barcode"]
    )
    if api_product is None:
        return jsonify({
            "error": "Product could not be found"
        }), 404

    new_item = {
        "id": len(inventory) + 1,
        "product_name": api_product.get(
            "product_name"
        ),
        "brands": api_product.get(
            "brands"
        ),
        "category": api_product.get(
            "categories"
        ),
        "ingredients_text": api_product.get(
            "ingredients_text"
        ),
        "image_url": api_product.get(
            "image_url"
        ),

        "barcode": data["barcode"],
        "quantity": data.get(
            "quantity",
            0
        ),
        "price": data.get(
            "price",
            0
        )
    }
    # Add to temporary storage
    inventory.append(new_item)
    return jsonify(new_item), 201
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_inventory(id):
    item = next(
        (item for item in inventory if item["id"] == id),
        None
    )

    # Check if item exists
    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404

    data = request.get_json()

    # Update only fields provided by the user
    allowed_fields = [
        "product_name",
        "brands",
        "category",
        "ingredients_text",
        "barcode",
        "quantity",
        "price"
    ]

    for field in allowed_fields:
        if field in data:
            item[field] = data[field]


    return jsonify(item), 200


@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_inventory(id):
    item = next(
        (item for item in inventory if item["id"] == id),
        None
    )
    # Check if item exists
    if item is None:
        return jsonify({
            "error": "Inventory item not found"
        }), 404
    # Remove item from array
    inventory.remove(item)
    return jsonify({
        "message": "Inventory item deleted",
        "deleted_item": item
    }), 200  
  
@app.route("/products/barcode/<barcode>", methods=["GET"])
def get_product_barcode(barcode):
    product = fetch_product_by_barcode(barcode)
    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404
    return jsonify(product), 200

@app.route("/products/search/<name>", methods=["GET"])
def search_product(name):

    product = fetch_product_by_name(name)
    if product is None:
        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product), 200
if __name__ == "__main__":
    app.run(debug=True)