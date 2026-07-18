from flask import Flask, jsonify, request
from inventory import inventory

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory API running"
    })

@app.route("/inventory", methods=["GET"])
def get_inventory():

    return jsonify(inventory), 200


if __name__ == "__main__":
    app.run(debug=True)