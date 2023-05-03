from flask import *

from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/web_Scrapper"
db = PyMongo(app).db

from Internshala import *

@app.route('/internshala', methods = ['POST', 'GET'])
def ScrapperApi():
    if request.method == 'POST':
        pages = 1
        url = "https://internshala.com/internships/work-from-home"
        body = request.json
        if body:
            final_url = URL(body, url)
        else:
            final_url = url
        final_url = final_url + "/page-"

        DataList = Internshala_scraper(final_url, pages)
        return render_template('index.html', DataList = DataList, body = body)
    if request.method == 'GET':
        data = db.internshala.find_one({'URL': 'https://internshala.com/internships/work-from-home-internships/page-1'})
        DataList = data['payload']
        # return jsonify('hi')
        body = {}
        return render_template('index.html', DataList = DataList, body = body)

if __name__ == '__main__':
    app.run(debug = True, port = 7777)