# app.py
from flask import Flask, jsonify, request, render_template
import utils
import Goal

app = Flask(__name__)
savings = 1000
purchases = []
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


@app.route('score', methods=['calculate'])
def calculate_score():
    needs, wants, situational = utils.categorize_transaction(purchases)
    return jsonify({"score": utils.calculate_score(needs, situational, wants)})


@app.route('expenses', methods=['analyze'])
def analyze_expenses():
    return jsonify({"message": utils.analyze_expenses(purchases)})


@app.route('transactions', methods=['categorize'])
def categorize_transactions():
    needs, wants, situational = utils.categorize_transaction(purchases)
    return jsonify({"needs": needs, "wants": wants, "situational": situational})


@app.route('reminder', methods=['remind'])
def remind():
    data = request.json
    time = data['time']
    return jsonify({"time": time})


if __name__ == "__main__":
    app.run(debug=True)
