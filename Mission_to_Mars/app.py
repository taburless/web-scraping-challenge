import flask 
from flask_pymongo import PyMongo
import scrape_mars.py

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo()

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongodb.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert = True)
    return "Scraping Successful"

if __name__ == "__main__":
    app.run()