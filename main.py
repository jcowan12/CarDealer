import pymongo
import datetime
import csv
import pprint

printer = pprint.PrettyPrinter()

with open("credentials.txt", "r") as f:
    user, password = f.read().splitlines()

client = pymongo.MongoClient('mongodb+srv://'+user+':'+password+'@dealership.xcq8qr9.mongodb.net/?retryWrites=true&w=majority')

# database ->> collection ->> docs (mongo structure)
db = client['dealership']

# collections
cars = db['cars']
customers = db['customers']
purchases = db['purchases']

# add car doc into cars collection
def add_cars(make, model, year, engine_HP, msrp):
    document = {
        'Make': make,
        'Model': model, 
        'Year': year,
        'Engine HP': engine_HP,
        'MSRP': msrp,
        'Date Added': datetime.datetime.now()
    }
    return cars.insert_one(document)

# add customer doc into customer collection
def add_customer(first_name, last_name, dob):
    document = {
        'First Name': first_name, 
        'Last Name': last_name,
        'Date of Birth': dob,
        'Date Added': datetime.datetime.now()
    }
    return customers.insert_one(document)

# add purchase to purchases collection
def add_purchase(car_id, customer_id, method):
    document = {
        'Car ID': car_id,
        'Customer ID': customer_id,
        'Method': method,
        'Date': datetime.datetime.now()
    }
    return purchases.insert_one(document)

# adds car data to mongo collection 
# def add_car_data(filename):
#     with open(filename, 'r') as file:
#         columns = file.readline().split(',')
#         file = csv.reader(file)
#         columns_needed = ['Make', 'Model', 'Year', 'Engine HP', 'Vehicle Size', 'Vehicle Style', 'MSRP']
#         indexs = list(filter(lambda x: columns[x].strip() in columns_needed , [i for i in range(len(columns))]))
#         number_columns = {"MSRP", "Year", "Engine HP"}

#         documents = []
#         for row in file:
#             document = {}
#             for count, index in enumerate(indexs):
#                 data = row[index]
#                 if columns_needed[count] in number_columns:
#                     try:
#                         data = float(data)
#                     except:
#                         continue
#                 document[columns_needed[count]] = data

#             documents.append(document)
        
#         cars.insert_many(documents)

# add_car_data('cars.csv')

# Queries

# less than 30k
result = cars.find({'MSRP': {'$lte': 30000}})
# printer.pprint(list(result))

# count number of cars
result = cars.count_documents({})

# older than 2000
result = cars.count_documents({'Year': {'$lt': 2000}})

# average price of all brands
result = cars.aggregate([
    {'$group':{
        '_id': '$Make',
        'count': {'$sum': 1},
        'average price': {'$avg': '$MSRP'}
    }
    }
])

# most expensive car
result = cars.find({}).sort([('MSRP', -1)]).limit(1)

# average price of hondas newer than 2000 by model
result = cars.aggregate([
    {
        '$match': {
            'Make': {'$eq': 'Honda'},
            'Year': {'$gt': 2000}
        }
    },
    {
        '$group': {
            '_id': '$Model',
            'average price': {'$avg': '$MSRP'}
        }
    }
])

def get_customer_info():
    print('type in your info')
    first_name = input('first name: ')
    last_name = input('last name: ')
    return first_name, last_name

first, last = get_customer_info()
customer_and_purchases = list(customers.aggregate([
    {
        '$match': {'First Name': first, 'Last Name': last}
    },
    {
        '$lookup': {
            'from': 'purchases',
            'localField': '_id', 
            'foreignField': 'Customer ID',
            'as': 'Purchases'
        }
    }
]))

# two customers with same name
for i, customer in enumerate(customer_and_purchases):
    print(f"{i+1}. {customer['First Name']} {customer['Last Name']}, {customer['Date of Birth']}")

# select user
selection = input('Select customer number: ')
customer = customer_and_purchases[int(selection) - 1]

print(f"Customer has purchased {len(customer['Purchases'])} cars")
for i, entry in enumerate(customer['Purchases']):
    car_id = entry['Car ID']
    car = cars.find_one({'_id': car_id})
    print(f'{i+1}. {car}')