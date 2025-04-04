from flask import Flask, render_template, request, jsonify
import json
import random
from pymongo import MongoClient

app = Flask(__name__)

# Specify encoding as 'utf-8' when opening the JSON file
with open("intent.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

client = MongoClient("mongodb://localhost:27017")  
db_webscraping = client["WebScrapingDB"]  
db_zepto = client["ZeptoDB"]  

bigbasket_collection = db_webscraping["BigBasket"]
zepto_products_collection = db_zepto["ZeptoProducts"]  

conversation_state = {}

# ... rest of your code ...

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_id = request.remote_addr  
    user_input = request.form["msg"].strip().lower()

    if user_input in ["hi", "hello"]:
        return "Hello! How can I assist you today? Choose: <br>1. Compare Price <br>2. Product Info <br>3. Bulk Product Comparison"
    if user_input in ["bye", "goodbye"]:
        return "Goodbye! Have a great day!"

    if user_id in conversation_state:
        state = conversation_state[user_id]
        if state["step"] == "awaiting_product":
            return handle_product_request(user_id, user_input)
        elif state["step"] == "awaiting_quantity":
            return handle_quantity_request(user_id, user_input)
        elif state["step"] == "awaiting_product_info":
            return handle_product_info_request(user_id, user_input)
        elif state["step"] == "awaiting_bulk_products":
            return handle_bulk_products_request(user_id, user_input)
        elif state["step"] == "awaiting_bulk_quantity":
            return handle_bulk_quantity_request(user_id, user_input)

    if user_input == "1":
        conversation_state[user_id] = {"step": "awaiting_product"}
        return "Which product would you like to compare prices for?"
    if user_input == "2":
        conversation_state[user_id] = {"step": "awaiting_product_info"}
        return "Which product info do you need?"
    if user_input == "3":
        conversation_state[user_id] = {"step": "awaiting_bulk_products"}
        return "Please enter the product names separated by commas."

    return "Invalid choice. Please select 1, 2, or 3."

def handle_product_request(user_id, product_name):
    if not product_name.replace(" ", "").isalnum():
        return "Invalid product name. Please enter a valid product name."
    
    zepto_product = zepto_products_collection.find_one({"Name": {"$regex": product_name, "$options": "i"}})
    bigbasket_product = bigbasket_collection.find_one({"Name": {"$regex": product_name, "$options": "i"}})
    
    response = []
    product_data = {}

    if zepto_product:
        zepto_price = float(zepto_product["Price"].replace("₹", ""))
        response.append(f"🛒 Zepto: {zepto_product['Name']} - ₹{zepto_price}")
        product_data["zepto_price"] = zepto_price
    else:
        response.append("Zepto: Not Available")
        product_data["zepto_price"] = None

    if bigbasket_product:
        bigbasket_price = float(bigbasket_product["Price"].replace("₹", ""))
        response.append(f"🛒 BigBasket: {bigbasket_product['Name']} - ₹{bigbasket_price}")
        product_data["bigbasket_price"] = bigbasket_price
    else:
        response.append("BigBasket: Not Available")
        product_data["bigbasket_price"] = None
    
    if not zepto_product and not bigbasket_product:
        conversation_state.pop(user_id, None)
        return "Sorry, this product is not available on Zepto or BigBasket."
    
    response.append("How many kilograms do you need?")
    conversation_state[user_id] = {"step": "awaiting_quantity", "product_data": product_data}
    return "<br>".join(response)

def handle_quantity_request(user_id, quantity_input):
    try:
        quantity = float(quantity_input)
        if quantity <= 0:
            return "Invalid quantity. Please enter a valid number greater than 0."
        
        product_data = conversation_state[user_id]["product_data"]
        zepto_total = product_data["zepto_price"] * quantity if product_data["zepto_price"] else None
        bigbasket_total = product_data["bigbasket_price"] * quantity if product_data["bigbasket_price"] else None
        
        response = []
        if zepto_total is not None:
            response.append(f"Zepto Total: ₹{zepto_total:.2f}")
        if bigbasket_total is not None:
            response.append(f"BigBasket Total: ₹{bigbasket_total:.2f}")
        
        if zepto_total and bigbasket_total:
            if zepto_total > bigbasket_total:
                response.append("BigBasket offers a better price!")
            elif zepto_total < bigbasket_total:
                response.append("Zepto offers a better price!")
            else:
                response.append("Both have the same price!")
        
        conversation_state.pop(user_id, None)
        return "<br>".join(response)
    except ValueError:
        return "Invalid input. Please enter a numeric value for the quantity."

def handle_product_info_request(user_id, product_name):
    product = zepto_products_collection.find_one({"Name": {"$regex": product_name, "$options": "i"}})
    
    if not product:
        product = bigbasket_collection.find_one({"Name": {"$regex": product_name, "$options": "i"}})
    
    if product:
        response = f"Product: {product['Name']}<br>Price: {product['Price']}<br>Discount: {product.get('Discount', 'No Discount Available')}"
        return response
    else:
        return "Sorry, product info not available."

def handle_bulk_products_request(user_id, products_input):
    product_names = [p.strip() for p in products_input.split(",")]
    response = []
    
    # Store the product names in the conversation state for the next step
    conversation_state[user_id] = {"step": "awaiting_bulk_quantity", "product_names": product_names}
    return "Please enter the quantity for each product separated by commas."

def handle_bulk_quantity_request(user_id, quantities_input):
    quantities = [float(q.strip()) for q in quantities_input.split(",")]
    product_names = conversation_state[user_id]["product_names"]
    
    if len(product_names) != len(quantities):
        return "The number of quantities does not match the number of products. Please try again."
    
    response = []
    
    for product_name, quantity in zip(product_names, quantities):
        if quantity <= 0:
            response.append(f"Invalid quantity for {product_name}. Please enter a valid number greater than 0.")
            continue
        
        zepto_product = zepto_products_collection.find_one({"Name": {"$regex": product_name, "$options": "i"}})
        bigbasket_product = bigbasket_collection.find_one({"Name": {"$regex": product_name, "$options": "i"}})
        
        zepto_total = float(zepto_product["Price"].replace("₹", "")) * quantity if zepto_product else None
        bigbasket_total = float(bigbasket_product["Price"].replace("₹", "")) * quantity if bigbasket_product else None
        
        if zepto_product and bigbasket_product:
            best_price = min(zepto_total, bigbasket_total)
            response.append(f"{product_name}: Best Price ₹{best_price:.2f}")
        elif zepto_product:
            response.append(f"{product_name}: Zepto ₹{zepto_product['Price']} for {quantity} kg")
        elif bigbasket_product:
            response.append(f"{product_name}: BigBasket ₹{bigbasket_product['Price']} for {quantity} kg")
        else:
            response.append(f"{product_name}: Not Available")
    
    conversation_state.pop(user_id, None)
    return "<br>".join(response)

if __name__ == '__main__':
    app.run(debug=True)