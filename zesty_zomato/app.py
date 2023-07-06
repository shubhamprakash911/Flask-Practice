from flask import Flask, request, jsonify,render_template
# import json
from pymongo import MongoClient
# from bson.objectid import ObjectId

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

app = Flask(__name__)


client = MongoClient("mongodb+srv://shubham:shubham@cluster0.lsxduhy.mongodb.net/flaskDB?retryWrites=true&w=majority")
db = client['flaskDB']
menu_collection = db["menu"]
orders_collection = db["orders"]



# # Load menu data from JSON file
# def load_menu():
#     with open('menu.json', 'r') as file:
#         return json.load(file)

# # Save menu data to JSON file
# def save_menu(menu):
#     with open('menu.json', 'w') as file:
#         json.dump(menu, file,indent=4)

# # Load order data from JSON file
# def load_orders():
#     with open('orders.json', 'r') as file:
#         return json.load(file)

# # Save order data to JSON file
# def save_orders(orders):
#     with open('orders.json', 'w') as file:
#         json.dump(orders, file,indent=4)




# Load menu data from MongoDB collection
def load_menu():
    return list(menu_collection.find({},{'_id':0}))

# Save menu data to MongoDB collection
def save_menu(menu):
    menu_collection.delete_many({})  # Clear existing data
    menu_collection.insert_many(menu)

# Load order data from MongoDB collection
def load_orders():
    return list(orders_collection.find({},{'_id':0}))

# Save order data to MongoDB collection
def save_orders(orders):
    orders_collection.delete_many({})  # Clear existing data
    orders_collection.insert_many(orders)



# chatbot code
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)


def get_Chat_response(text):

    # Let's chat for 5 lines
    for step in range(5):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    

# chatbot code end

@app.route('/')
def index():
   return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


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
@app.route('/menu', methods=['PUT'])
def update_dish_availability():

    menu = load_menu()
    dish_id=int(request.json['id'])

    for dish in menu:
        if dish['id'] == dish_id:
            dish['availability'] = 'no' if dish['availability'] =='yes' else 'yes'
            print(dish)
            save_menu(menu)
            return jsonify({'message': 'Dish availability updated successfully'})

    return jsonify({'message': 'Dish not found'})

# Remove a dish from the menu
@app.route('/menu', methods=['DELETE'])
def remove_dish():
    menu = load_menu()
    dish_id=int(request.json['id'])

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
@app.route('/orders', methods=['PUT'])
def update_order_status():
    orders = load_orders()
    order_id=int(request.json['order_id'])
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
    # return render_template("admin.html",orders=jsonify(orders))

if __name__ == '__main__':
    app.run(debug=True)
