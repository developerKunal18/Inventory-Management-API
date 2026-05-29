from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ---------- Config ----------
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------- Product Model ----------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

# Create DB
with app.app_context():
    db.create_all()

# ---------- View Inventory ----------
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "stock": p.stock,
            "price": p.price
        }
        for p in products
    ])

# ---------- Add Product ----------
@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()

    product = Product(
        name=data["name"],
        stock=data["stock"],
        price=data["price"]
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product added"
    })

# ---------- Update Stock ----------
@app.route("/products/<int:product_id>/stock", methods=["PUT"])
def update_stock(product_id):
    data = request.get_json()

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    product.stock = data["stock"]

    db.session.commit()

    return jsonify({
        "message": "Stock updated"
    })

# ---------- Low Stock Alert ----------
@app.route("/low-stock", methods=["GET"])
def low_stock():
    products = Product.query.filter(
        Product.stock < 5
    ).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "stock": p.stock
        }
        for p in products
    ])

# ---------- Delete Product ----------
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted"
    })

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
