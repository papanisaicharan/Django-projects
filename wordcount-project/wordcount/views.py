from django.http import HttpResponse
from django.shortcuts import render
import operator

def homePage(request):
    return render(request, 'home.html', {'test': "Hello my dear"})

def eggs(request):
    return HttpResponse("<h1>Eggs</h1>")

def about(request):
    return render(request, 'about.html')

def count(request):
    fulltext = request.GET['fulltext']
    count = len(fulltext.split(" "))
    worddictionary = {}
    for word in fulltext.split():
        if word not in worddictionary.keys():
            worddictionary[word] = 1
        else:
            worddictionary[word] += 1
    sortedWords = sorted(worddictionary.items(), key = lambda x : x[1])
    return render(request, 'count.html', {'fulltext': fulltext, 'count': count, 'frequency': sortedWords })
