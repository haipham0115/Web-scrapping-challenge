from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_DB"
# mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")

# connect to mongoDB with conn and client:
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# create or connect (if already exist) to databse mars_BD
db = client.mars_DB


@app.route("/")
def home():
    # connect/ create to mars_scraped_info collection inside the mars_DB. And find 1 record
    mars_info = db.mars_scraped_info.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    # listings = mongo.db.listings

    # call the scrape fundtion in scrape_mars.py
    mars_scrape_dictionary = scrape_mars.scrape()

    # update the collection with the all the scraped data
    db.mars_scraped_info.update({}, mars_scrape_dictionary, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)


















