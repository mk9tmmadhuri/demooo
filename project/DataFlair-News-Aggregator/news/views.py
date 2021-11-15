
import requests
import os
from bs4 import BeautifulSoup as BSoup
from news.forms import CreateUserForm
from news.models import Headline
import nltk
from newspaper import Article

from django.shortcuts import render, redirect 
from django.http import HttpResponse,request
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

requests.packages.urllib3.disable_warnings()


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			print(form)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'news/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('/')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'news/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


#--------------------------------------------------------------------------


#1 Los Angels News

@login_required(login_url='login')
def losAngels(request):
	losAngels_r = requests.get("https://losangeles.cbslocal.com/category/news/")
	losAngels_soup = BSoup(losAngels_r.content, 'html.parser')
	sectionData = losAngels_soup.find("div", attrs={'class':'block-content-wrapper and-list layout-catalog aspect-ratio-16-9 enable-type-icons'})
	anchors = sectionData.findAll('a', attrs={'class':'cbs-thumbnail-link'})
	final_data = []
	try:
		for i in anchors:
			temp = {}
			temp['url'] = i['href']
			url = i['href']
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			temp['summary'] = article.summary
			imageSection = i.find('div', attrs={'class':'thumbnail-wrapper'})
			temp['image'] = imageSection.find('img')['data-src']
			titleSection = i.find('div', attrs={'class':'title-wrapper'})
			temp['title'] = titleSection.find('strong',attrs={'class':'title'}).text
			splittedArticle = article.summary.split(' ')[:45]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			final_data.append(temp)
	except:
		print("error")
	return render(request, "news/losAngels.html", {'final_data':final_data})

#2 Times of San Deigo

@login_required(login_url='login')
def sanDeigo(request):
	chi_r = requests.get("https://timesofsandiego.com/archives-2/")
	chi_soup = BSoup(chi_r.content, 'html.parser')
	sectionData = chi_soup.findAll("article", attrs={'class':'has-post-thumbnail'})
	#print(sectionData)
	final_data = []

	try:
		for i in sectionData:
			temp = {}
			url = i.find('a')['href']
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			temp['summary'] = article.summary
			temp['image'] = i.find('amp-img')['src']
			temp['url'] = url
			temp['title'] = i.find('h2', attrs={'class':'entry-title'}).text
			splittedArticle = article.summary.split(' ')[:40]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			final_data.append(temp)
	except:
		print("error")
	return render(request, "news/sanDeigo.html", {'final_data':final_data})


#3. NBC News
@login_required(login_url='login')
def nbc(request):
	ny_r = requests.get("https://www.nbcnews.com/us-news")
	ny_soup = BSoup(ny_r.content, 'html.parser')
	sectionData = ny_soup.findAll("div", attrs={'class':'wide-tease-item__wrapper'})
	#print(sectionData)
	final_data = []

	try:
		for i in sectionData:
			temp = {}
			url = i.find('a',attrs={'class':'wide-tease-item__image-wrapper'})['href']
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			temp['summary'] = article.summary
			outerDiv = i.find('div', attrs={'class':'wide-tease-item__info-wrapper'})
			innerH2 = outerDiv.find('h2',attrs={'class':'wide-tease-item__headline'})
			temp['url'] = url
			temp['image'] = i.find('img')['src']
			temp['title'] = innerH2.text
			splittedArticle = article.summary.split(' ')[:40]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			final_data.append(temp)
	except:
		print("error")
	return render(request, "news/nbc.html", {'final_data':final_data})


#4. times of india
@login_required(login_url='login')
def callSummarizeFunction(request):
	toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
	toi_soup = BSoup(toi_r.content, 'html.parser')
	#print("toi_soup")
	#print(toi_soup)
	toi_data = toi_soup.findAll("div", {'class':'brief_box'})
	#finalJSON = summarizeFunc(toi_data)
	final_data = []
	nltk.download('punkt')
	try:
		for div in toi_data:
			temp = {}
			url = 'https://timesofindia.indiatimes.com/'+div.find('a')['href']
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			temp['summary'] = article.summary
			splittedArticle = article.summary.split(' ')[:40]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			temp['url'] = url
			temp['image'] = div.find('img')['data-src']
			temp['title'] = div.find('img')['alt']
			final_data.append(temp)
		print(final_data)
		#return final_data
	except:
		print("error occred")
	return render(request, "news/landing.html", {'final_data':final_data})




#5. New York Times
@login_required(login_url='login')
def newYorkTimes(request):
	ny_r = requests.get("https://www.nytimes.com/section/us")
	ny_soup = BSoup(ny_r.content, 'html.parser')
	sectionData = ny_soup.find(id='stream-panel')
	getLatestNewsData = sectionData.findAll('li')
	nltk.download('punkt')
	newYorkData = []

	for div in getLatestNewsData:
		temp = {}
		url='https://www.nytimes.com/'+div.find('a')['href']
		article = Article(url)
		article.download()
		article.parse()
		article.nlp()
		temp['summary'] = article.summary
		temp['url'] = url
		temp['image'] = div.find('img')['src']
		temp['title'] = div.find('h2').text
		splittedArticle = article.summary.split(' ')[:40]
		temp['shortSummary'] = ' '.join(splittedArticle) 
		newYorkData.append(temp)

	return render(request, "news/nytimes.html", {'final_data':newYorkData})



#6. NDTV
@login_required(login_url='login')
def ndtvFunc(request):
	ndtv_r = requests.get("https://www.ndtv.com/")
	ndtv_soup = BSoup(ndtv_r.content, 'html.parser')
	ndtv_data = ndtv_soup.findAll("ul")
		#finalJSON = summarizeFunc(toi_data)
	final_data = []
	nltk.download('punkt')

	try:
		for div in ndtv_data:
			temp = {}
			temp['url'] = 'https://www.ndtv.com/ '+div.find('a')['href']
			url = div.find('a')['href']
			print(url)
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			temp['image'] = div.find('img')['src']
			temp['title'] = div.find('a',{'class':'item-title'}).text
			temp['summary'] = article.summary
			splittedArticle = article.summary.split(' ')[:40]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			final_data.append(temp)
	except:
		print("error")

	return render(request, "news/ndtv.html", {'final_data':final_data})




#7. republic tv
@login_required(login_url='login')
def republicTV(request):
	republic_r = requests.get("https://www.republicworld.com/")
	republic_soup = BSoup(republic_r.content, 'html.parser')
	republic_data = republic_soup.findAll("div", {"class":"bdrTop-dddddd"})

	final_data = []
	nltk.download('punkt')

	try:
		for div in republic_data:
			temp = {}
			url = div.find('a')['href']
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			temp['summary'] = article.summary
			temp['url'] = url
			temp['image'] = div.find('img')['src']
			temp['title'] = div.find('h2').text.strip()
			splittedArticle = article.summary.split(' ')[:40]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			final_data.append(temp)
	except:
		print("error")

	return render(request, "news/republic.html", {'final_data':final_data})



#8. Chicago Reader
@login_required(login_url='login')
def chicagoReader(request):

	chi_r = requests.get("https://chicagoreader.com/news-politics/")
	chi_soup = BSoup(chi_r.content, 'html.parser')
	sectionData = chi_soup.findAll("article", attrs={'class':'has-post-thumbnail'})
	#print(sectionData)
	final_data = []

	try:
		for i in sectionData:
			temp = {}
			url = i.find('a')['href']
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			temp['summary'] = article.summary
			temp['image'] = i.find('amp-img')['src']
			temp['url'] = url
			temp['title'] = i.find('h2', attrs={'class':'entry-title'}).text
			splittedArticle = article.summary.split(' ')[:55]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			final_data.append(temp)
	except:
		print("error")
	return render(request, "news/chicagoReader.html", {'final_data':final_data})


#9. india today
@login_required(login_url='login')
def indiaToday(request):
	india_today_r = requests.get("https://www.indiatoday.in/india")
	india_today_soup = BSoup(india_today_r.content, 'html.parser')
	india_today_data = india_today_soup.findAll("div", {"class":"catagory-listing"})
	final_data = []
	nltk.download('punkt')

	try:
		for div in india_today_data:
			temp = {}
			url = 'https://www.indiatoday.in/'+div.find('a')['href']
			temp['url'] = url
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			splittedArticle = article.summary.split(' ')[:40]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			temp['image'] = div.find('img')['src']
			temp['title'] = div.find('h2')['title']
			temp['summary'] = article.summary
			final_data.append(temp)
	except:
		print("error")

	return render(request, "news/indiaToday.html", {'final_data':final_data})



#10. States Man
@login_required(login_url='login')
def statesMan(request):
	toi_r = requests.get("https://www.thestatesman.com/")
	toi_soup = BSoup(toi_r.content, 'html.parser')
	toi_data = toi_soup.findAll("ul")
	final_data = []
	nltk.download('punkt')
	toi_sliced = toi_data[5:]

	try:
		for div in toi_sliced:
			temp = {}
			url = div.find('a')['href']
			print(url)
			article = Article(url)
			article.download()
			article.parse()
			article.nlp()
			splittedArticle = article.summary.split(' ')[:40]
			temp['shortSummary'] = ' '.join(splittedArticle) 
			temp['summary'] = article.summary
			temp['url'] = url
			temp['image'] = div.find('img')['src']
		
			if div.find('img').text == '':
				temp['title'] = div.find('img')['alt']
			else:
				temp['title'] = div.find('img').text

			final_data.append(temp)
	except:
		print("error")
	return render(request, "news/statesMan.html", {'final_data':final_data})