from django.shortcuts import render
from django.http import HttpResponse
from scraper.apps import Scraper
def init(request):
	return HttpResponse("<!--> " + Scraper.get_teams() + " ")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")