import csv
#from django.urls import reverse
#import logging
import statistics
#from email.mime import image
#from multiprocessing import context
from sqlite3 import Row
from tkinter import Image
from urllib import request

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from django.conf import settings
#from .forms import CsvBulkUploadForm
from django.conf.urls.static import static
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
#dataset=pd.read_csv("test.csv")
from scipy.stats import norm

#%matplotlib inline
import datavisual.static.datavisual.csvfiles as csv

from .forms import CsvForm
from .models import Csv

# Create your views here.

def upload_file_view(request):
    if request.method=="POST":
        global xaxis
        global yaxis
        xaxis=request.POST.get('xaxis','default')
        yaxis=request.POST.get('yaxis','default')
    
    
    success_message = None
    
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        success_message= "Uploaded sucessfully"
        
    read=Csv.objects.last().file_name.path
    global dataset
    dataset=pd.read_csv(read)
    columns=dataset.columns.to_list()    
    context = {
        'form': form,
        'success_message': success_message,
        'columns':columns
        
    }
    return render(request, 'datavisual/index.html',context)



def histogram(request):
    upload_file_view(request)
    upload_file_view(request)
    fig, ax = plt.subplots(1,2)
    ax[0].hist(x=dataset[xaxis], bins = 1000)
    ax[0].set_xlabel(xaxis)
   
    ax[1].hist(x=dataset[yaxis], bins = 1000)
    ax[1].set_xlabel(yaxis)
    plt.title("Histograms for " + xaxis+ " and " + yaxis)
    df=plt.show()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
   

def scatter(request):
    upload_file_view(request)
    upload_file_view(request)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis) 
    plt.scatter(x=dataset[xaxis], y=dataset[yaxis])
    plt.title("Relation between "+xaxis+" and "+yaxis)
    graph=plt.show()

    content2={
       'df': graph, 
    }
    return render(request, 'datavisual/upload_csv.html', content2)

#function to view first five rows in the dataset
def first5(request):
    upload_file_view(request)
    df=dataset.head().to_html()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    
    
#function to view first five rows in the dataset
def last5(request):
    upload_file_view(request)
    df=dataset.tail().to_html()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    

#function to view the description of the dataset
def modelStats(request):
    upload_file_view(request)
    stats=dataset.describe().to_html()
    content2={
        'df':stats
    }
    return render(request, 'datavisual/upload_csv.html', content2) 

def normalDistCurve(request):
    upload_file_view(request)
    upload_file_view(request)
    #fig, ax = plt.subplots(1,2)
    mean = statistics.mean(dataset[xaxis])
    sd = statistics.stdev(dataset[xaxis])
    #mean1 = statistics.mean(dataset[yaxis])
    #sd1 = statistics.stdev(dataset[yaxis])
    plt.xlabel(xaxis)
    
    plt.plot(dataset[xaxis], norm.pdf(dataset[xaxis], mean, sd))
    #ax[1].plot(dataset[yaxis], norm.pdf(dataset[yaxis], mean1, sd1))
    plt.title("Normal distribution sketch for "+xaxis)
    df=plt.show()
    #df=sns.displot(dataset['Revenue (Millions)'])
    
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    #return HttpResponse("<h1>View normal distribution curve here</h1>")

def description(request):
    upload_file_view(request)
    df=dataset.head(dataset.shape[0]).to_html()
    #df=dataset.sort_values(by='Rank',ascending=True).value_counts(sort=True,ascending=True).to_frame().to_html()
    content={
       'df': df,
       
    }
    return render(request, 'datavisual/upload_csv.html', content)
    #return HttpResponse("<h1>View description here</h1>")          





