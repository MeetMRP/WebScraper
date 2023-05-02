from flask import *
from .Internshala import *

app = Flask(__name__)


@app.route('/internshala', methods = ['POST'])
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


if __name__ == '__main__':
    app.run(debug = True, port = 7777)