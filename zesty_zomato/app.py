from flask import Flask, request, jsonify,render_template
import json

app = Flask(__name__)

# Load menu data from JSON file
def load_menu():
    with open('menu.json', 'r') as file:
        return json.load(file)

# Save menu data to JSON file
def save_menu(menu):
    with open('menu.json', 'w') as file:
        json.dump(menu, file,indent=4)

# Load order data from JSON file
def load_orders():
    with open('orders.json', 'r') as file:
        return json.load(file)

# Save order data to JSON file
def save_orders(orders):
    with open('orders.json', 'w') as file:
        json.dump(orders, file,indent=4)


@app.route('/')
def index():
   return render_template('index.html')


# Get all dishes from the menu
@app.route('/menu', methods=['GET'])
def get_menu():
    menu = load_menu()
    return jsonify(menu)

# Add a new dish to the menu
@app.route('/menu', methods=['POST'])
def add_dish():
    menu = load_menu()
    dish = request.json

    # Assign a new dish ID
    dish_id = len(menu) + 1
    dish['id'] = dish_id

    menu.append(dish)
    save_menu(menu)

    return jsonify({'message': 'Dish added successfully'})

# Update the availability of a dish
@app.route('/menu/<int:dish_id>', methods=['PUT'])
def update_dish_availability(dish_id):
    menu = load_menu()

    for dish in menu:
        if dish['id'] == dish_id:
            dish['availability'] = request.json['availability']
            save_menu(menu)
            return jsonify({'message': 'Dish availability updated successfully'})

    return jsonify({'message': 'Dish not found'})

# Remove a dish from the menu
@app.route('/menu/<int:dish_id>', methods=['DELETE'])
def remove_dish(dish_id):
    menu = load_menu()

    for dish in menu:
        if dish['id'] == dish_id:
            menu.remove(dish)
            save_menu(menu)
            return jsonify({'message': 'Dish removed successfully'})

    return jsonify({'message': 'Dish not found'})

# Take a new order
@app.route('/orders', methods=['POST'])
def take_order():
    menu = load_menu()
    orders = load_orders()
    order = request.json

    # Assign a new order ID
    order_id = len(orders) + 1
    order['id'] = order_id

    # Check if each dish is available
    for dish_id in order['dishes']:
        dish_available = False
        for dish in menu:
            if dish['id'] == dish_id and dish['availability'] == 'yes':
                dish_available = True
                break
        if not dish_available:
            return jsonify({'message': 'One or more dishes are not available'})

    order['status'] = 'received'
    orders.append(order)
    save_orders(orders)

    return jsonify({'message': 'Order taken successfully'})

# Update the status of an order
@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    orders = load_orders()

    for order in orders:
        if order['id'] == order_id:
            order['status'] = request.json['status']
            save_orders(orders)
            return jsonify({'message': 'Order status updated successfully'})

    return jsonify({'message': 'Order not found'})

# Get all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = load_orders()
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)
