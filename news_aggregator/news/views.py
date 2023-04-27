import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

requests.packages.urllib3.disable_warnings()

def news_list(request):
	headlines = Headline.objects.all()[::-1]
	context = {
		'object_list': headlines,
	}
	return render(request, "news/home.html", context)

def scrape(request):
	session = requests.Session()
	session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
	url = "https://www.theonion.com/"

	content = session.get(url, verify=False).content
	breakpoint()
	soup = BSoup(content, "html.parser")
	News = soup.find_all('div', {"class":"sc-1pw4fyi-3"})
	breakpoint()
	for artcile in News:
		main = artcile.find_all('a')[0]
		breakpoint()
		#link = main['href']
		link = "https://www.theonion.com/tucker-carlson-exclusive-interview-1850375489"
		#image_src = str(main.find('img')['srcset']).split(" ")[-4]
		image_src = "https://i.kinja-img.com/gawker-media/image/upload/…r,q_60,w_965/92e810db9c01437cb5bf39e6a08f5ff1.jpg"
		#title = main['title']
		title = "The Onion’s Exclusive Interview With Tucker Carlson"
		new_headline = Headline()
		new_headline.title = title
		new_headline.url = link
		new_headline.image = image_src
		new_headline.save()
	return redirect("../")

