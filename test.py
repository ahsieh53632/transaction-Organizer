import wikipedia
import re
import requests
import json
import datetime
import copy
import matplotlib.pyplot as plt
import timeit

start = timeit.timeit()
apiKey = '28838a88ae9fed2b8405e3d3d90b1513'

url = 'http://api.reimaginebanking.com/enterprise/bills?key=28838a88ae9fed2b8405e3d3d90b1513'
data = requests.get(url)
json_data = data.json()
total = []
copies = []
database = {}
categories = {'Food': ['\\sfood\\s', '\\srestaurant',
                       '\\sdrink\\s', '\\seat\\s', '\\stea\\s'],
              'Entertainment': ['\\sentertain', '\\svideo', '\\stheater',
                                '\\sgame', '\\sfun\\s', '\\sactivities',
                                '\\smovie', '\\sticket',
                                '\\sfilm', '\\stelevision'],
              'Gas': ['\\sfoil', '\\sgas'],
              'Retail': ['\\sretail', '\\ssport', '\\scloth', '\\sapparel',
                         '\\sfashion', '\\sluxury', 'commerce'],
              'Life': ['\\slandlord', '\\srent', '\\sinsurance',
                       '\\scar', '\\sPlane', '\\sAirlines', '\\sinvestment', '\\sbank']}
sorted = {'Food': [], 'Entertainment': [], 'Gas': [], 'Retail': [], 'Life': [], 'other': []}
max_data_num = 3000  # change this if you want, this is how much transactions you wanna sort

Food_sum = 0
Enter_sum = 0
Gas_sum = 0
Retail_sum = 0
Life_sum = 0
Other_sum = 0
Total_SUM = 0
flag = re.IGNORECASE


def get_list():
    for transaction in json_data["results"]:
        if transaction['status'] != 'cancelled':
            if 'payment_date' in transaction or 'recurring_date' in transaction:
                try:
                    total.append((transaction['payee'],transaction['payment_amount'],transaction['payment_date']))
                except Exception:
                    copies.append(transaction)

    for recur_transaction in copies:
        second = copy.deepcopy(recur_transaction)
        start_date = second['creation_date'].split("-")
        curr_date = str(datetime.date.today()).split("-")
    while int(start_date[0]) <= int(curr_date[0]):
        if int(start_date[1]) <= int(curr_date[1]):
            if int(start_date[2]) <= int(curr_date[2]):
                pay_date = str(start_date[0]) + '-' + str(start_date[1]) + '-' + str(recur_transaction['recurring_date'])
                total.append((second['payee'], second['payment_amount'], pay_date))
                if (int(start_date[1]) < 12):
                    start_date[1] = str(int(start_date[1]) + 1)
                else:
                    start_date[1] = str(1)
                    start_date[0] = str(int(start_date[0]) + 1)
            else:
                if (int(start_date[1]) < 12):
                    start_date[1] = str(int(start_date[1]) + 1)
                else:
                    start_date[1] = str(1)
                    start_date[0] = str(int(start_date[0]) + 1)
        else:
            start_date[0] = str(int(start_date[0]) + 1)
            start_date[1] = str(1)


def categorize(company_name):
    if (company_name in database):
        return database[company_name]
    # options = wikipedia.search(company_name, results=5)
    # checks if the company_name contains Inc in the end,
    #  inorder to make searching faster
    if(re.search("Inc\\.$ | Inc$", company_name) is None):
        choice = [company_name + " Inc."]
    # loop thorugh possible options, and search what categories
    # for choice in options:
        for cata in categories:
            for attri in categories[cata]:
                try:
                    look_up = wikipedia.summary(choice, sentences=5)
                    x = re.search(attri, look_up, flag)
                except Exception:
                    x = None
                if (x is not None):
                    database[company_name] = cata
                    return cata
    database[company_name] = 'other'
    return 'other'


def update_cat(name, replace_cat):
    database[name] = replace_cat


get_list()

for i in range(0, max_data_num):
    x = total[i]
    curr = x[0]
    cat = categorize(curr)
    print(cat)
    if (cat == 'Food'):
        if(isinstance(x[1], int) or isinstance(x[1], float)):
            Food_sum = x[1] + Food_sum
            sorted[cat].append(x)
            print(cat + ": " + "(" + x[0] + ", " + str(x[1]) + ", " + x[2] + ")")
    elif (cat == 'Entertainment'):
        if(isinstance(x[1], int) or isinstance(x[1], float)):
            Enter_sum = x[1] + Enter_sum
            sorted[cat].append(x)
            print(cat + ": " + "(" + x[0] + ", " + str(x[1]) + ", " + x[2] + ")")
    elif (cat == 'Gas'):
        if(isinstance(x[1], int) or isinstance(x[1], float)):
            Gas_sum = x[1] + Gas_sum
            sorted[cat].append(x)
            print(cat + ": " + "(" + x[0] + ", " + str(x[1]) + ", " + x[2] + ")")
    elif (cat == 'Retail'):
        if(isinstance(x[1], int) or isinstance(x[1], float)):
            Retail_sum = x[1] + Retail_sum
            sorted[cat].append(x)
            print(cat + ": " + "(" + x[0] + ", " + str(x[1]) + ", " + x[2] + ")")
    elif (cat == 'Life'):
        if(isinstance(x[1], int) or isinstance(x[1], float)):
            Life_sum = x[1] + Life_sum
            sorted[cat].append(x)
            print(cat + ": " + "(" + x[0] + ", " + str(x[1]) + ", " + x[2] + ")")
    elif (cat == 'other'):
        if(isinstance(x[1], int) or isinstance(x[1], float)):
            Other_sum = x[1] + Other_sum
            sorted[cat].append(x)
            print(cat + ": " + "(" + x[0] + ", " + str(x[1]) + ", " + x[2] + ")")
    else:
        raise Exception("!!!!SORTING ERROR !!!!!!!!")

print("--------------------------------------SUMMARY-------------------------------------")
print("Category: Food " + "|| Summary: " + str("%.2f" % Food_sum))
print("Category: Entertainment " + "|| Summary: " + str('%.2f' % Enter_sum))
print("Category: Gas " + "|| Summary: " + str("%.2f" % Gas_sum))
print("Category: Retail " + "|| Summary: " + str("%.2f" % Retail_sum))
print("Category: Life " + "|| Summary: " + str("%.2f" % Life_sum))
print("Category: Others " + "|| Summary: " + str("%.2f" % Other_sum))
Total_SUM = Food_sum + Enter_sum + Gas_sum + Retail_sum + Life_sum + Other_sum
print("-----------------------------------END-SUMMARY-------------------------------------")


# plot the graph
# labels
labels = 'Food', 'Entertainment', 'Gas', 'Retail', 'Life', 'Others'
sizes = [200 * Food_sum/Total_SUM, 200 * Enter_sum/Total_SUM, 200 * Gas_sum/Total_SUM,
         200 * Retail_sum/Total_SUM, 200 * Life_sum/Total_SUM, 200 * Other_sum/Total_SUM]
colors = ['gold', 'red', 'blue', 'yellow', 'pink', 'green', 'black']
explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1)  # explode 1st slice

end = timeit.timeit()
print(f"RUNNNNN TIME: {end-start}")
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.show()
