from flask import Flask, jsonify, request

app = Flask(__name__)

from products import products

# Ruta de prueba para verificar si la API está en funcionamiento:
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

# Rutas para obtener información sobre productos:
@app.route('/products')
def getProducts():
    # devolver jsonify(products)
    return jsonify({'products': products})


@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productsFound = [
        product for product in products if product['name'] == product_name.lower()]
    if (len(productsFound) > 0):
        return jsonify({'product': productsFound[0]})
    return jsonify({'message': 'Product Not found'})

# Ruta para agregar nuevos productos (operación POST):
@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        'name': request.json['name'],
        'price': request.json['price'],
        'quantity': 10
    }
    products.append(new_product)
    return jsonify({'products': products})

# Ruta para editar un producto existente (operación PUT):
@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound) > 0):
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            'message': 'Product Updated',
            'product': productsFound[0]
        })
    return jsonify({'message': 'Product Not found'})

# Ruta para eliminar un producto (operación DELETE):
@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            'message': 'Product Deleted',
            'products': products
        })
#Iniciar la aplicación:

if __name__ == '__main__':
    app.run(debug=True, port=4000)