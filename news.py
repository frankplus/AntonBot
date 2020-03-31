import requests

newsapi_key = "e49b250beb4b4dda944498542fd55491"

def get_latest_news(query = None):

    if query:
        url = 'http://newsapi.org/v2/everything?q={}&sortBy=relevancy&apiKey={}'.format(query, newsapi_key)
    else:
        url = 'http://newsapi.org/v2/top-headlines?country=it&sortBy=publishedAt&apiKey={}'.format(newsapi_key)
        
    r = requests.get(url)
    data = r.json()
    if data["status"] == "ok" and data["totalResults"] > 0:
        article = data["articles"][0]
        info = '{} - {}'.format(article["url"], article["description"])
        return info
    else:
        return "I haven't found anything"