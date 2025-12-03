# app.py
import sys
from flask import Flask, request, jsonify
from utils import api_handler, logger, APIError, NotFoundError
from db import init_db
from models import User, Product, Order
from services import bulk_upload_products

app = Flask(__name__)
@app.route("/")
def home():
    return "Mini E-commerce API is running!"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# ---- User endpoints ----
@app.route("/users", methods=["POST"])
@api_handler
def create_user():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        raise APIError("name and email required")
    user = User.create(name, email)
    return jsonify({"user": user.__dict__}), 201

@app.route("/users", methods=["GET"])
@api_handler
def list_users():
    users = User.list_all()
    return jsonify({"users": users}), 200

@app.route("/users/<int:user_id>", methods=["GET"])
@api_handler
def get_user(user_id):
    user = User.get_by_id(user_id)
    return jsonify({"user": user.__dict__}), 200

# ---- Product endpoints ----
@app.route("/products", methods=["POST"])
@api_handler
def create_product():
    data = request.get_json() or {}
    for fld in ("name", "price", "stock"):
        if fld not in data:
            raise APIError(f"{fld} required")
    p = Product.create(
        name=data["name"],
        description=data.get("description", ""),
        price=float(data["price"]),
        stock=int(data["stock"])
    )
    return jsonify({"product": p.__dict__}), 201

@app.route("/products", methods=["GET"])
@api_handler
def list_products():
    prods = Product.list_all()
    return jsonify({"products": prods}), 200

@app.route("/products/<int:product_id>", methods=["GET"])
@api_handler
def get_product(product_id):
    p = Product.get_by_id(product_id)
    return jsonify({"product": p.__dict__}), 200

@app.route("/products/<int:product_id>", methods=["PUT"])
@api_handler
def update_product(product_id):
    p = Product.get_by_id(product_id)
    data = request.get_json() or {}
    updated = p.update(**data)
    return jsonify({"product": updated.__dict__}), 200

@app.route("/products/<int:product_id>", methods=["DELETE"])
@api_handler
def delete_product(product_id):
    p = Product.get_by_id(product_id)
    p.delete()
    return jsonify({"deleted": True}), 200

# Bulk upload CSV
@app.route("/products/bulk-upload", methods=["POST"])
@api_handler
def bulk_upload():
    """
    Expects form-data with file field 'file' containing CSV.
    CSV columns: name,description,price,stock
    """
    if 'file' not in request.files:
        raise APIError("file (CSV) required")
    file = request.files['file']
    results = bulk_upload_products(file.stream, max_workers=5)
    return jsonify({"results": results}), 200

# ---- Orders ----
@app.route("/orders", methods=["POST"])
@api_handler
def create_order():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    items = data.get("items")  # expected list of {"product_id": int, "quantity": int}
    if not user_id or not isinstance(items, list) or len(items) == 0:
        raise APIError("user_id and items required")
    order = Order.create(user_id=user_id, items=items)
    return jsonify(order), 201

@app.route("/orders/<int:order_id>", methods=["GET"])
@api_handler
def get_order(order_id):
    order = Order.get_by_id(order_id)
    return jsonify(order), 200

@app.route("/orders", methods=["GET"])
@api_handler
def list_orders():
    orders = Order.list_all()
    return jsonify({"orders": orders}), 200

# CLI helpers
def main():
    if len(sys.argv) >= 2:
        cmd = sys.argv[1]
        if cmd == "init-db":
            init_db()
            return
        elif cmd == "run":
            # default run
            app.run(debug=True)
            return
    print("Usage: python app.py [init-db|run]")

if __name__ == "__main__":
    main()
