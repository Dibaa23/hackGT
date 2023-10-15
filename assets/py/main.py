# app.py
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

import utils
import Goal

app = Flask(__name__)
savings = 1000
purchases = [("Dining", 25.00),            # Breakfast at Local Café,
    ("Dining", 40.00),            # Friday Night Dinner at Italian Restaurant,
    ("Gas/Automotive", 35.00),    # Weekly Gas Fill-Up,
    ("Grocery", 100.00),          # Weekly Grocery Shopping,
    ("Healthcare", 50.00),        # Prescription Medication,
    ("Lodging", 150.00),          # Weekend Getaway Hotel Stay,
    ("Merchandise", 80.00),       # Online Clothes Shopping,
    ("Other", 30.00),             # Monthly Streaming Subscription,
    ("Other Services", 100.00),   # Haircut and Salon Service,
    ("Payment", 1200.00),         # Monthly Rent Payment,

    ("Dining", 12.00),            # Coffee and Sandwich at Local Café,
    ("Dining", 50.00),            # Saturday Night Dinner at Sushi Restaurant,
    ("Gas/Automotive", 35.00),    # Weekly Gas Fill-Up,
    ("Grocery", 95.00),           # Weekly Grocery Shopping,
    ("Healthcare", 25.00),        # Over-the-counter Medication,
    ("Merchandise", 60.00),       # Shoes from Department Store,
    ("Other", 10.00),             # Monthly Magazine Subscription,
    ("Other Services", 60.00),    # House Cleaning Service,
    ("Payment", 100.00),          # Utility Bill,

    ("Dining", 10.00),            # Coffee and Muffin at Local Café,
    ("Gas/Automotive", 40.00),    # Weekly Gas Fill-Up,
    ("Grocery", 110.00),          # Weekly Grocery Shopping,
    ("Lodging", 180.00),          # Hotel for Friend's Wedding,
    ("Merchandise", 20.00),       # Book from Local Bookstore,
    ("Other Services", 50.00),    # Manicure and Pedicure,
    ("Payment", 50.00),           # Cell Phone Bill,

    ("Dining", 15.00),            # Salad and Juice at Health Food Restaurant,
    ("Gas/Automotive", 38.00),    # Weekly Gas Fill-Up,
    ("Grocery", 85.00),           # Weekly Grocery Shopping,
    ("Merchandise", 40.00),       # Kitchen Appliance from Online Store,
    ("Other", 15.00),             # Monthly Music Streaming Subscription,
    ("Payment", 60.00)           # Internet Bill
]
investments = []
goals = Goal.Goals(savings)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add():
    data = request.json
    a = data['a']
    b = data['b']
    return jsonify({"result": a + b})


@app.route('/goal', methods=['update_savings'])
def update_savings():
    goals.savings = savings

@app.route('/savings', methods=['get'])
def get_savings():
    return jsonify({"savings": savings})

@app.route('/goal', methods=['contribute'])
def contribute():
    data = request.json
    goal = data['goal']
    amt = data['amt']
    if amt > 0:
        return jsonify({"message": goals.contribute(goal, amt)})
    else:
        return jsonify({"message": goals.decontribute(goal, -amt)})


@app.route('/goal', methods=['add_goal'])
def add_goal():
    data = request.json
    goal = data['goal']
    amt = data['amt']
    return jsonify({"message": goals.add_goal(goal, amt)})


@app.route('/goal', methods=['remove_goal'])
def remove_goal():
    data = request.json
    goal = data['goal']
    goals.remove_goal(goal)


@app.route('/goal', methods=['change_total'])
def change_total():
    data = request.json
    goal = data['goal']
    total = data['total']
    return jsonify({"message": goals.change_total(goal, total)})


@app.route('/gpt', methods=['purchase'])
def gpt_rec():
    return jsonify({"message": utils.gpt_rec(purchases)})


@app.route('/gpt', methods=['investment'])
def gpt_inv():
    return jsonify({"message": utils.gpt_rec(investments)})


@app.route('/score', methods=['calculate'])
def calculate_score():
    needs, wants, situational = utils.categorize_transaction(purchases)
    return jsonify({"score": utils.calculate_score(needs, situational, wants)})


@app.route('/expenses', methods=['analyze'])
def analyze_expenses():
    return jsonify({"message": utils.analyze_expenses(purchases)})


@app.route('/transactions', methods=['GET'])
def categorize_transactions():
    needs, wants, situational = utils.categorize_transaction(purchases)
    return jsonify({"needs": needs, "wants": wants, "situational": situational})


@app.route('/reminder', methods=['remind'])
def remind():
    data = request.json
    time = data['time']
    return jsonify({"time": time})

CORS(app)
if __name__ == "__main__":
    app.run(debug=True)
    

