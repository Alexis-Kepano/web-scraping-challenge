from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
app = Flask(__name__)
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()
    print(mars_data)
    # Return template and data
    return render_template("index.html", planet=mars_data,hemisphere=mars_data['mars_hemispheres'],featured_imgs=mars_data['featured_image'])

@app.route("/scrape")
def scrape():
    # Run scrape function
    mars_data = scrape_mars.scrape_info()
    # Update Mongo database
    mongo.db.collection.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
