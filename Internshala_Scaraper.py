from flask import *
import json
import bs4
from urllib import request as req

app = Flask(__name__)


def Internshala_scraper(final_url, pages):
    page_no =1
    DataList = []
    while page_no <= pages:
        response = req.urlopen(final_url + str(page_no))
        soup = bs4.BeautifulSoup(response, "html.parser")
        internships = soup.findAll('h3', {'class': 'heading_4_5 profile'})

        for internship in internships[:10]:
            link = 'https://internshala.com/' + internship.findChildren("a",class_="view_detail_button")[0].get('href')
            Response = req.urlopen(link)
            Soup = bs4.BeautifulSoup(Response, "html.parser")
            Name = Soup.find('span', {'class': 'profile_on_detail_page'}).text.strip()
            Location = Soup.find('a', {'class': 'location_link view_detail_button'}).text.strip()
            Duration = Soup.find('div', {'class': 'other_detail_item_row'}).findChildren('div', {'class': 'other_detail_item'})[1].find('div', {'class': 'item_body'}).text.strip()
            Stipend = Soup.find('div', {'class': 'other_detail_item stipend_container'}).findChildren('div', {'class': 'item_body'})[0].find('span', {'class': 'stipend'}).text.strip()
            About = Soup.find('div', {'class': 'text-container about_company_text_container'}).text.strip()
            data = {
                'name': Name,
                'link': link,
                'location': Location,
                'duration': Duration,
                'stipend': Stipend,
                'about': About,
                    }
            DataList.append(data)
        page_no = page_no + 1
    
    return DataList


def URL(body, url):
    if body['Category']:
        Category = body['Category']
        url = url + "-" + Category.replace(" ", "-").lower() + "-internships"
    else:
        url = url + "-internships"
    if body['Location']:
        Location = body['Location']
        url = url + "-in-" + Location.replace(" ", "-").lower()
    if body['Stipend']:
        Stipend = body['Stipend']
        url = url + "/stipend-" + str(Stipend) 
    return url


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