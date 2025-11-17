from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
# Configure CORS to allow requests from frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Note: Using port 5001 by default to avoid macOS AirPlay Receiver conflict on port 5000

# In-memory data storage (replace with database in production)
users_db = {}
orders_db = {}
dishes_db = {}
bids_db = {}
reputation_db = {}
knowledge_base = {
    "menu": "You can browse our menu by clicking on the 'Menu' link in the navigation.",
    "order": "To place an order, add items to your cart from the menu page, then proceed to checkout.",
    "delivery": "Our delivery system uses a bidding model. Delivery staff can bid on orders.",
    "wallet": "You can deposit money to your wallet from the customer dashboard."
}

def initialize_mock_users():
    """Initialize mock users for testing each role"""
    mock_users = [
        {
            'id': 1,
            'name': 'John Customer',
            'email': 'customer@test.com',
            'password': 'customer123',
            'userType': 'customer',
            'phone': '555-0101',
            'walletBalance': 100.0,
            'isVIP': False,
            'approved': True,
            'createdAt': datetime.now().isoformat()
        },
        {
            'id': 2,
            'name': 'Jane VIP Customer',
            'email': 'vip@test.com',
            'password': 'vip123',
            'userType': 'customer',
            'phone': '555-0102',
            'walletBalance': 500.0,
            'isVIP': True,
            'approved': True,
            'createdAt': datetime.now().isoformat()
        },
        {
            'id': 3,
            'name': 'Chef Mario',
            'email': 'chef@test.com',
            'password': 'chef123',
            'userType': 'chef',
            'phone': '555-0201',
            'walletBalance': 0.0,
            'isVIP': False,
            'approved': True,
            'createdAt': datetime.now().isoformat()
        },
        {
            'id': 4,
            'name': 'Delivery Driver',
            'email': 'delivery@test.com',
            'password': 'delivery123',
            'userType': 'delivery',
            'phone': '555-0301',
            'walletBalance': 0.0,
            'isVIP': False,
            'approved': True,
            'createdAt': datetime.now().isoformat()
        },
        {
            'id': 5,
            'name': 'Manager Admin',
            'email': 'manager@test.com',
            'password': 'manager123',
            'userType': 'manager',
            'phone': '555-0401',
            'walletBalance': 0.0,
            'isVIP': False,
            'approved': True,
            'createdAt': datetime.now().isoformat()
        }
    ]
    
    for user in mock_users:
        users_db[user['id']] = user

def initialize_mock_orders():
    """Initialize mock orders for testing"""
    # Create a mock order for customer ID 1 (John Customer)
    mock_order = {
        'id': 1,
        'userId': 1,
        'items': [
            {
                'id': 1,
                'name': 'Margherita Pizza',
                'price': 12.99,
                'quantity': 2
            },
            {
                'id': 2,
                'name': 'Pepperoni Pizza',
                'price': 14.99,
                'quantity': 1
            },
            {
                'id': 3,
                'name': 'Caesar Salad',
                'price': 8.99,
                'quantity': 1
            }
        ],
        'subtotal': 49.96,
        'discount': 0.0,  # Customer is not VIP
        'total': 49.96,
        'status': 'Preparing',
        'createdAt': datetime.now().isoformat()
    }
    orders_db[mock_order['id']] = mock_order

# Initialize mock users on startup
initialize_mock_users()
# Initialize mock orders on startup
initialize_mock_orders()

@app.route('/')
def home():
    return jsonify({"message": "AI Slice API is running"})

# Authentication endpoints
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    user_id = len(users_db) + 1
    user = {
        'id': user_id,
        'name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password'),  # In production, hash this
        'userType': data.get('userType'),
        'phone': data.get('phone'),
        'walletBalance': 0.0,
        'isVIP': False,
        'createdAt': datetime.now().isoformat()
    }
    users_db[user_id] = user
    return jsonify({"success": True, "user": user}), 201

@app.route('/api/auth/signin', methods=['POST'])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    for user_id, user in users_db.items():
        if user['email'] == email and user['password'] == password:
            return jsonify({"success": True, "user": user}), 200
    
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

# Menu endpoints
@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify({"dishes": list(dishes_db.values())}), 200

@app.route('/api/menu', methods=['POST'])
def add_dish():
    data = request.json
    dish_id = len(dishes_db) + 1
    dish = {
        'id': dish_id,
        'name': data.get('name'),
        'chef': data.get('chef'),
        'price': data.get('price'),
        'description': data.get('description', ''),
        'available': data.get('available', True),
        'rating': data.get('rating', 0.0)
    }
    dishes_db[dish_id] = dish
    return jsonify({"success": True, "dish": dish}), 201

@app.route('/api/menu/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    if dish_id not in dishes_db:
        return jsonify({"success": False, "message": "Dish not found"}), 404
    
    data = request.json
    dishes_db[dish_id].update(data)
    return jsonify({"success": True, "dish": dishes_db[dish_id]}), 200

# Order endpoints
@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data.get('userId')
    
    if user_id not in users_db:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    user = users_db[user_id]
    total = data.get('total', 0)
    
    # Check wallet balance
    if total > user['walletBalance']:
        # Add warning to reputation
        if user_id not in reputation_db:
            reputation_db[user_id] = []
        reputation_db[user_id].append({
            'type': 'warning',
            'reason': 'Insufficient funds - order rejected',
            'date': datetime.now().isoformat()
        })
        return jsonify({
            "success": False,
            "message": "Order rejected - insufficient funds"
        }), 400
    
    # Apply VIP discount
    discount = 0
    if user.get('isVIP'):
        discount = total * 0.05
        total = total - discount
    
    # Deduct from wallet
    user['walletBalance'] -= total
    
    order_id = len(orders_db) + 1
    order = {
        'id': order_id,
        'userId': user_id,
        'items': data.get('items', []),
        'subtotal': data.get('subtotal', 0),
        'discount': discount,
        'total': total,
        'status': 'Placed',
        'createdAt': datetime.now().isoformat()
    }
    orders_db[order_id] = order
    
    return jsonify({"success": True, "order": order}), 201

@app.route('/api/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    user_orders = [order for order in orders_db.values() if order['userId'] == user_id]
    return jsonify({"orders": user_orders}), 200

# Bidding endpoints
@app.route('/api/bids', methods=['POST'])
def place_bid():
    data = request.json
    bid_id = len(bids_db) + 1
    bid = {
        'id': bid_id,
        'orderId': data.get('orderId'),
        'deliveryPersonId': data.get('deliveryPersonId'),
        'deliveryPerson': data.get('deliveryPerson'),
        'amount': data.get('amount'),
        'status': 'Pending',
        'createdAt': datetime.now().isoformat()
    }
    bids_db[bid_id] = bid
    return jsonify({"success": True, "bid": bid}), 201

@app.route('/api/bids/order/<int:order_id>', methods=['GET'])
def get_order_bids(order_id):
    order_bids = [bid for bid in bids_db.values() if bid['orderId'] == order_id]
    sorted_bids = sorted(order_bids, key=lambda x: x['amount'])
    return jsonify({"bids": sorted_bids}), 200

@app.route('/api/bids/assign', methods=['POST'])
def assign_delivery():
    data = request.json
    order_id = data.get('orderId')
    bid_id = data.get('bidId')
    manager_override = data.get('managerOverride', False)
    justification = data.get('justification', '')
    
    if manager_override and not justification:
        return jsonify({
            "success": False,
            "message": "Justification required for manager override"
        }), 400
    
    # Update bid status
    if bid_id in bids_db:
        bids_db[bid_id]['status'] = 'Won'
        # Update order status
        if order_id in orders_db:
            orders_db[order_id]['status'] = 'Assigned for Delivery'
            orders_db[order_id]['deliveryPersonId'] = bids_db[bid_id]['deliveryPersonId']
            if manager_override:
                orders_db[order_id]['managerOverride'] = True
                orders_db[order_id]['justification'] = justification
        
        return jsonify({"success": True, "message": "Delivery assigned"}), 200
    
    return jsonify({"success": False, "message": "Bid not found"}), 404

# AI Chat endpoints
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    question = data.get('question', '').lower()
    
    # Search local knowledge base
    answer = None
    from_local_kb = False
    
    for key, value in knowledge_base.items():
        if key in question:
            answer = value
            from_local_kb = True
            break
    
    # If no local answer, use LLM fallback (simulated)
    if not answer:
        answer = "I'm here to help! You can ask me about the menu, placing orders, delivery, wallet management, or any other questions about our platform."
        from_local_kb = False
    
    return jsonify({
        "answer": answer,
        "fromLocalKB": from_local_kb
    }), 200

@app.route('/api/ai/rate', methods=['POST'])
def rate_answer():
    data = request.json
    rating = data.get('rating', 0)
    
    if rating == 0:
        # Flag for manager review
        return jsonify({
            "success": True,
            "message": "Answer flagged for manager review"
        }), 200
    
    return jsonify({"success": True, "message": "Rating recorded"}), 200

# Wallet endpoints
@app.route('/api/wallet/deposit', methods=['POST'])
def deposit_money():
    data = request.json
    user_id = data.get('userId')
    amount = data.get('amount', 0)
    
    if user_id not in users_db:
        return jsonify({"success": False, "message": "User not found"}), 404
    
    users_db[user_id]['walletBalance'] += amount
    return jsonify({
        "success": True,
        "newBalance": users_db[user_id]['walletBalance']
    }), 200

# Reputation endpoints
@app.route('/api/reputation/user/<int:user_id>', methods=['GET'])
def get_user_reputation(user_id):
    reputation = reputation_db.get(user_id, [])
    return jsonify({"reputation": reputation}), 200

@app.route('/api/reputation/rating', methods=['POST'])
def submit_rating():
    data = request.json
    user_id = data.get('userId')
    rating_type = data.get('type')  # 'food' or 'delivery'
    rating = data.get('rating', 0)
    order_id = data.get('orderId')
    
    if user_id not in reputation_db:
        reputation_db[user_id] = []
    
    reputation_db[user_id].append({
        'type': rating_type,
        'rating': rating,
        'orderId': order_id,
        'date': datetime.now().isoformat()
    })
    
    return jsonify({"success": True}), 200

# Manager endpoints
@app.route('/api/manager/registrations', methods=['GET'])
def get_pending_registrations():
    # In production, filter by status
    pending = [user for user in users_db.values() if not user.get('approved', False)]
    return jsonify({"registrations": pending}), 200

@app.route('/api/manager/approve', methods=['POST'])
def approve_registration():
    data = request.json
    user_id = data.get('userId')
    
    if user_id in users_db:
        users_db[user_id]['approved'] = True
        return jsonify({"success": True}), 200
    
    return jsonify({"success": False, "message": "User not found"}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))  # Default to 5002 to avoid macOS AirPlay conflict (port 5000) and other services
    app.run(debug=True, port=port)

