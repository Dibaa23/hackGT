import openai
import math

openai.api_key = "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"

# Asks purchases question to ChatGPT for advice - DONE
def gpt_rec(purchases):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": \
             "Could you help analyze these purchases and give me some recommendations? Type the string in a format best suitable for textContent HTML and make it 50 words and in one paragraph."},
            {"role": "user", "content": str(purchases)}
        ]
    )
    return response['choices'][0]['message']['content']

# Asks investments question to ChatGPT for advice - DONE
def gpt_inv(investments):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": \
             "Could you help analyze these investments and give me some recommendations?"},
            {"role": "user", "content": str(investments)}
        ]
    )
    return response['choices'][0]['message']['content']

# Minimum calculator - DONE
def minimum(num1, num2):
    if num1 <= num2:
        return num1
    else:
        return num2

# Income int function - DONE
def income_int_funct(net_income):
    income_int = 0
    if net_income < 20000:
        income_int = 0
    elif net_income < 30000:
        income_int = 1
    elif net_income < 40000:
        income_int = 2
    elif net_income < 50000:
        income_int = 3
    elif net_income < 60000:
        income_int = 4
    elif net_income < 70000:
        income_int = 5
    elif net_income < 80000:
        income_int = 6
    elif net_income < 90000:
        income_int = 7
    elif net_income < 100000:
        income_int = 8
    else:
        income_int = 9

    return income_int

# Returns target percents for situational, wants + situational weight factor for score equation - DONE
def need_sit_want_percents_specific(net_income):
    income_int = income_int_funct(net_income)
    finance_list = [[0.15, 0.1], [0.15, 0.12], [0.15, 0.12], [0.18, 0.15], [0.18, 0.15], [0.18, 0.17], [0.18, 0.17], [0.2, 0.18], [0.2, 0.18], [0.2, 0.2]]
    constant_list = [0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75]

    return [finance_list[income_int], constant_list[income_int]]

# Calculates score - DONE
def calculate_score(purchase_dict, net_income):
    list_of_finance_constants = need_sit_want_percents_specific(net_income)
    constant = list_of_finance_constants[1]
    target_situational = list_of_finance_constants[0][0]
    target_wants = list_of_finance_constants[0][1]

    nsw_list = three_expense_categories(purchase_dict)
    nsw_list = [x / sum(nsw_list) for x in nsw_list]
    situational = nsw_list[1]
    wants = nsw_list[2]

    score = minimum((1 - constant * (situational - target_situational) - (wants - target_wants)) * 100, 100)
    return score

# Calculates percentages of needs, wants, & situational based on purchases types - DONE
def categorize_transaction(list_of_purchases, purchase_dict = {"Dining": 0, "Gas/Automotive": 0, "Grocery": 0, \
                                                               "Healthcare": 0, "Lodging": 0, "Merchandise": 0, "Other": 0, \
                                                                "Other Services": 0, "Payment": 0}):
    for purchase in list_of_purchases:
        for item in purchase_dict.keys():
            if purchase[0] == item:
                purchase_dict[item] += purchase[1]

    return purchase_dict

# Counts of main 3, and percentages of main 3 as percent of total expenses - DONE
def three_expense_categories(purchase_dict):
    needs = purchase_dict["Grocery"] + purchase_dict["Healthcare"] + purchase_dict["Payment"]
    situational = purchase_dict["Dining"] + purchase_dict["Gas/Automotive"] + 0.25 * purchase_dict["Other"]
    wants = 0.75 * purchase_dict["Other"] + purchase_dict["Lodging"] + purchase_dict["Merchandise"] + purchase_dict["Other Services"]

    return [needs, situational, wants]

# Counts of all categories as percent of total expenses - DONE
def all_expense_categories(purchase_dict):
    grocery = purchase_dict["Grocery"]
    health = purchase_dict["Healthcare"]
    payment = purchase_dict["Payment"]
    dining = purchase_dict["Dining"]
    gas_auto = purchase_dict["Gas/Automotive"]
    other = purchase_dict["Other"]
    lodging = purchase_dict["Lodging"]
    merch = purchase_dict["Merchandise"]
    other_servs = purchase_dict["Other Services"]

    return [grocery, health, payment, dining, gas_auto, other, lodging, merch, other_servs]

# Percentages of sub-categories as percent of needs - DONE
def nested_needs_percentages(purchase_dict):
    all_catg_list = all_expense_categories(purchase_dict)[0:3]
    needs_percent_list = [x / sum(all_catg_list) for x in all_catg_list]

    return needs_percent_list

# Percentages of sub-categories as percent of situational - DONE
def nested_situational_percentages(purchase_dict):
    all_catg_list = all_expense_categories(purchase_dict)[3:6]
    all_catg_list = [all_catg_list[0], all_catg_list[1], 0.25 * all_catg_list[2]]
    situational_percent_list = [x / sum(all_catg_list) for x in all_catg_list]

    return situational_percent_list

# Percentages of sub-categories as percent of wants - DONE
def nested_wants_percentages(purchase_dict):
    all_catg_list = all_expense_categories(purchase_dict)[5:]
    all_catg_list = [0.75 * all_catg_list[0], all_catg_list[1], all_catg_list[2], all_catg_list[3]]
    wants_percent_list = [x / sum(all_catg_list) for x in all_catg_list]

    return wants_percent_list

# Difference in spending (actual v. expected) - DONE
def expected_actual_spending(purchase_dict, month_income, net_income):
    nsw_list = three_expense_categories(purchase_dict)
    nsw_value_income_list = [x / sum(nsw_list) * month_income for x in nsw_list]

    list_of_financial_constraints = need_sit_want_percents_specific(net_income)
    situational_percent = list_of_financial_constraints[0][0]
    wants_percent = list_of_financial_constraints[0][1]
    needs_percent = 1 - situational_percent - wants_percent

    return [nsw_value_income_list[0], nsw_value_income_list[1], nsw_value_income_list[2], \
            needs_percent * month_income, situational_percent * month_income, wants_percent * month_income]

# Analyzes expenses - DONE
def analyze_expenses(purchase_dict, net_income):
    nsw_list = three_expense_categories(purchase_dict)
    nsw_percent_list = [x / sum(nsw_list) for x in nsw_list]

    list_of_finance_constants = need_sit_want_percents_specific(net_income)

    exceeded_bools_list = [False, False]
    diff_in_sit_wants_list = [0, 0]

    for i in range(1, len(nsw_percent_list)):
        if nsw_percent_list[i] > list_of_finance_constants[0][i - 1]:
            exceeded_bools_list[i - 1] = True
            diff_in_sit_wants_list[i - 1] = nsw_percent_list[i] - list_of_finance_constants[0][i - 1]

    situational_diff = math.ceil(diff_in_sit_wants_list[0] * 100)
    wants_diff = math.ceil(diff_in_sit_wants_list[1] * 100)

    worst = 0
    indicator = ""

    if exceeded_bools_list[0] and situational_diff > wants_diff:
        worst = situational_diff
        indicator = "Situational"
    elif exceeded_bools_list[1] and wants_diff > situational_diff:
        worst = wants_diff
        indicator = "Wants"
    
    if indicator == "Situational":
        return f'Your expenses are higher than expected by {worst} percent. \
            Please try and reduce your areas of spending in Dining, Gas/Automotive, and Other.'

    if indicator == "Wants":
        return f'Your expenses are higher than expected by {worst} percent. \
            Please try and reduce your areas of spending in Lodging, Merchandice, Other, and Other Services.'


# How often to send opted-in reminder to pay bills - DONE
def need_reminder(time, week_factor = 1):
    if time > 60 * 60 * 24 * 7 * week_factor:
        return True
    return False


'''
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
            if purchase[0] == item: #type
                purchase_dict[item] += purchase[1] #amount

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
'''