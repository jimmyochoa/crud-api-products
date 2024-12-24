from flask import Flask,request,jsonify

from models.product import Product

app= Flask(__name__)

products = []

@app.route('/products', methods=["POST"])
def create_product ():
    data= request.get_json()

    if "name" not in data or "description" not in data or "price" not in data:
        return jsonify({"error":"Please, fill all the fields"}), 400
    
    for product in products:
        if product.name == data["name"]:
            return jsonify({"error": f"Product with name: {data["name"]} already exists!"})

    product_id = len(products) + 1
    product = Product(
        product_id= product_id,
        name = data["name"],
        description= data["description"],
        price= data["price"]
    )

    products.append(product)

    return jsonify({
        "product_id": product.product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "enabled": product.enabled
    }), 201

@app.route("/products", methods=["GET"])
def get_products():
    response = [{
        "product_id": p.product_id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
    } for p in products]
    return jsonify(response)

@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    # Check if the product exists
    response = [{
        "product_id": p.product_id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
    } for p in products if p.product_id == id]

    if not response:
        return jsonify({"error": f"Product with id: {id} was not found"}), 404

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)