from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

app = Flask(__name__)

# Use flask pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# conn = "mongodb://localhost:27017"
# client = pymongo.MongoClient(conn)

# db = client.mars_db
# collection = db.mars

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    # mars = db.collection.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = db.collection
    #mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)

    return "Scraping Successful!"

if __name__=="__main__":
    app.run(debug=True)
