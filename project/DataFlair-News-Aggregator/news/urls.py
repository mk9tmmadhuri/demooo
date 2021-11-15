from django.urls import path
from news.views import chicagoReader, indiaToday, loginPage, logoutUser, losAngels, nbc, ndtvFunc, registerPage, republicTV, sanDeigo, statesMan,callSummarizeFunction,newYorkTimes

urlpatterns = [
	path('register/', registerPage, name="register"),
	path('login/', loginPage, name="login"),  
	path('logout/', logoutUser, name="logout"),
	path('', callSummarizeFunction, name="landing"),
	path('nytimes/', newYorkTimes, name="nytimes"),
	path('losAngels/', losAngels, name="losAngels"),
	path('sanDeigo/', sanDeigo, name="sanDeigo"),
	path('nbc/', nbc, name="nbc"),
	path('ndtv/', ndtvFunc, name="ndtv"),
	path('republic', republicTV, name="republic"),
	path('chicagoReader/', chicagoReader, name="chicagoReader"),
	path('indiaToday/', indiaToday, name="indiaToday"),
	path('statesMan/', statesMan, name="statesMan"),
]