import bs4
from urllib import request as req
from Web_scraper import db

def Flipkart_scraper(url, pages):
    page_no = 1
    DataList = []
    while page_no <= pages:
        response = req.urlopen(url + str(page_no))
        soup = bs4.BeautifulSoup(response)
        title = soup.findAll('div', {'class': '_4rR01T'})
        prices = soup.findAll('div', {'class': '_30jeq3 _1_WHN1'})
        link = soup.findAll('a', {'class': '_1fQZEK'})
        rate = soup.find_all('div', {'class': '_3LWZlK'})
        desc = soup.find_all('ul', {'class': '_1xgFaf'})
        for item in range(len(title)):
            description = []
            desc_elements = desc[item].findChildren('li', {'class': 'rgWa7D'})
            for d in desc_elements:
                description.append(d.text.strip())
            data = {
                'Title': title[item].text.strip(),
                'Price': prices[item].text.strip(),
                'Star_rating': rate[item].text.strip(),
                'Description': description,
                'Link': "https://www.flipkart.com" + link[item]['href'],
            }
            DataList.append(data)

        if db.internshala.count_documents({'URL': url + str(page_no)}) == 0:
            Data_db = {
                'URL': url + str(page_no),
                'payload': DataList
            }
            db.internshala.insert_one(Data_db)
        page_no = page_no + 1
    return DataList