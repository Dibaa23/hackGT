import openai

openai.api_key = "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"


def gpt_rec(purchases):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Could you help analyze these purchase and give me some recommendations?"},
            {"role": "user", "content": str(purchases)}
        ]
    )
    return response['choices'][0]['message']['content']


def gpt_inv(investments):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Could you help analyze these investments and give me some recommendations?"},
            {"role": "user", "content": str(investments)}
        ]
    )
    return response['choices'][0]['message']['content']


def calculate_score(needs, situational, wants):
    score = (needs - wants - (situational / 10)) / (needs + wants + situational)
    if score < 0:
        score = 0
    return score * 100


def analyze_expenses(list_of_purchases):
    purchase_dict = {"Dining": 0,
                     "Gas/Automotive": 0,
                     "Grocery": 0,
                     "Healthcare": 0,
                     "Lodging": 0,
                     "Merchandise": 0,
                     "Other": 0,
                     "Other Services": 0,
                     "Payment": 0}

    for purchase in list_of_purchases:
        for item in purchase_dict.keys():
            if purchase.type == item:
                purchase_dict[item] += purchase.amount

    purchase_dict["Dining"] /= 300
    purchase_dict["Gas/Automotive"] /= 250
    purchase_dict["Grocery"] /= 500
    purchase_dict["Healthcare"] /= 1000
    purchase_dict["Lodging"] /= 200
    purchase_dict["Merchandise"] /= 400
    purchase_dict["Other"] /= 200
    purchase_dict["Other Services"] /= 200
    purchase_dict["Payment"] /= 1000

    worst = max(purchase_dict, key=purchase_dict.get)

    return worst


def categorize_transaction(list_of_purchases):
    purchase_dict = {"Dining": 0,
                     "Gas/Automotive": 0,
                     "Grocery": 0,
                     "Healthcare": 0,
                     "Lodging": 0,
                     "Merchandise": 0,
                     "Other": 0,
                     "Other Services": 0,
                     "Payment": 0}

    for purchase in list_of_purchases:
        for item in purchase_dict.keys():
            if purchase.type == item:
                purchase_dict[item] += purchase.amount

    situational = 0
    needs = 0
    wants = 0
    situational += purchase_dict["Dining"]
    situational += purchase_dict["Gas/Automotive"]
    needs += purchase_dict["Grocery"]
    needs += purchase_dict["Healthcare"]
    wants += purchase_dict["Lodging"]
    wants += purchase_dict["Merchandise"]
    wants += purchase_dict["Other"]
    wants += purchase_dict["Other Services"]
    needs += purchase_dict["Payment"]
    total = needs + wants + situational

    return needs / total, wants / total, situational / total


def need_reminder(time):
    if time > 1000000:
        return True
    return False
