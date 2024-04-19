"""
This is the primary flask application file which is used to create a web application to interact with the MongoDB database.
Whie starting the application, it will connect to the MongoDB database and create a connection to the profile database.

The application will have two routes:
1. / - This route will display the existing records in the users collection of the profile database.
2. /update - This route will be used to update the existing records in the users collection of the profile database.

While starting docker container, you can use the following command:
docker run -d -p 8080:8080 -v d:/logs:/var/log --net testnet --name flaskapp flaskapp:2.0

This will connect to the mongo DB container and create a connection to the profile database.

"""

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import logging
import uuid

app = Flask(__name__)

# Configure logging
# when using locally, change the log_file path to local path like d:/logs/app.log
log_file = "/var/log/app.log"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# MongoDB connection string
# Replace 'test_database' with your database name, incase of running application outside docker container, 
# use localhost:27017 instead of mongo
mongo_uri = "mongodb://admin:apollo13@localhost:27017/" 
client = MongoClient(mongo_uri)
db = client.profile
collection = db.users


@app.route('/')
def index():
    contacts = collection.find_one()
    logging.info("Retrieved contacts: %s", contacts)
    return render_template('index.html', contacts=contacts)


@app.route('/update', methods=['POST'])
def update():
    name = request.form.get('name').strip()
    address = request.form.get('address').strip()
    company = request.form.get('company').strip()
    userid = request.form.get('userid').strip()
    
    uid = "None"
    item_details = collection.find({"userid": userid })
    for item in item_details:
        uid = item['userid']
    if uid != "None":
        logging.info(f"Updating existing user with unique: {uid}")
        collection.update_one({'userid': userid}, {'$set':{"name": name, "address": address, "company": company}}, upsert=True)
    else:
        # create a random UUID 
        userid = str(uuid.uuid4())
        logging.info(f"Creating new user with following details  - {userid}, {name}, {address}, {company} ")  
        collection.insert_one({'userid': userid, 'name': name, 'address': address, 'company': company})
        logging.info(f"New document inserted successfully! userid: {userid}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)