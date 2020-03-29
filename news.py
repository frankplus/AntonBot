import requests

def get_latest_news(query = None):

    if query:
        url = 'http://newsapi.org/v2/everything?q={}&sortBy=relevancy&apiKey=e49b250beb4b4dda944498542fd55491'.format(query)
    else:
        url = 'http://newsapi.org/v2/top-headlines?country=it&sortBy=publishedAt&apiKey=e49b250beb4b4dda944498542fd55491'
        
    r = requests.get(url)
    data = r.json()
    if data["status"] == "ok" and data["totalResults"] > 0:
        article = data["articles"][0]
        info = '{} - {}'.format(article["url"], article["description"])
        return info
    else:
        return "I haven't found anything"