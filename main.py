import pymongo
import datetime

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

def add_purchase(car_id, customer_id, method):
    document = {
        'Car ID': car_id,
        'Customer ID': customer_id,
        'Method': method,
        'Date': datetime.datetime.now()
    }
    return purchases.insert_one(document)