import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

requests.packages.urllib3.disable_warnings()

def news_list(request):
        titles = set()
        unique_headlines = []
        headlines = Headline.objects.all()[::-1]
        for headline in headlines:
                if headline.title not in titles:
                        titles.add(headline.title)
                        unique_headlines.append(headline)
        context = {
		'object_list': unique_headlines,
	}
        return render(request, "news/home.html", context)

def scrape(request):
	session = requests.Session()
	session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
	url = "https://www.cnn.com/"

	content = session.get(url, verify=False).content
	soup = BSoup(content, "html.parser")
	articles = soup.find_all('div', {"class":"container_lead-package"})
	for article in articles:
                title = ""
                if article.find("div", class_="container__headline") is not None:
                        title = article.find("div", class_="container__headline").get_text()
                link = ""
                if article.find("a", class_="container__link") is not None:
                        link = url + article.find("a", class_="container__link")["href"]
                image_src = ""
                if article.find("img", class_="image__dam-img") is not None:
                        image_src = article.find("img", class_="image__dam-img")["src"]
                if title is not "":
                        new_headline = Headline()
                        new_headline.title = title
                        new_headline.url = link
                        new_headline.image = image_src
                        new_headline.save()
	return redirect("../")
