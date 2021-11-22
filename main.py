#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 18:54:46 2021

@author: krishna
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import bs4
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import math
import time


""""
The given data of a google scholar, i.e., revised.csv should be in the series form.
"""
URL = 'https://drive.google.com/file/d/1V--24_3-tvY6B2dgFGONT9BUrR7bVXe4/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+URL.split('/')[-2]
data= pd.read_csv(path)
# data=pd.read_csv('/Users/krishna/Documents/KPMG India/placement/insights/revised.csv')
columns=data.columns
google_scholar_list=data[columns[2]]



def get_source(url):

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def scrape_google(query):
    query = urllib.parse.quote_plus(query)
    while True:
        response = get_source("https://www.google.co.uk/search?q=" + query)
        if response is not None:
            break

    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links


def get_info(scholar_list):
    researcher_info=pd.DataFrame(columns=['Name', 'Affilation','H-index', 'Citations 2020', 'Total_citation', 'H-index_since_2016', 'Citation_since_2016', 'HomePage','Area of Research', 'Google_Scholar'])
    columns=researcher_info.columns
    researcher_google_scholar=scholar_list
    
    # print(researcher_google_scholar[54])
    
    start_time=time.time()
    total_time=0
    for index in range(0, len(researcher_google_scholar)):   
        if index==1:
            end_time=time.time()
            total_time=end_time-start_time
            
        substring='scholar'
        if type(researcher_google_scholar[index])!=str:
            flag=True
        else:
            flag=False

            
        if flag==False and substring in researcher_google_scholar[index]:   
            print(index, ':', len(researcher_google_scholar), ' time remaining is ', (len(researcher_google_scholar)-index)*total_time/60, ' min ')
            info_first=[]
            info_second=[]
            info_third=[]
            
            # r=requests.get('https://scholar.google.com/citations?user=pxzB3EwAAAAJ&hl=en')
            # r=requests.get('https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjN45nao5_0AhXHZCsKHVO0DVwQFnoECAUQAQ&url=https%3A%2F%2Fscholar.google.com.sg%2Fcitations%3Fuser%3D8FjY99sAAAAJ%26hl%3Den&usg=AOvVaw3yXEa03OHOn9TsDNJYyXSH')
            
            r=requests.get(researcher_google_scholar[index])
            soup=BeautifulSoup(r.content, 'html.parser')
            for info1 in soup.find_all('td', class_='gsc_rsb_std'):
                info_first.append(info1.text)
            
            if len(info_first)==0:
                print('Google scholar link is invalid')
                continue
            
            name= soup.find('div',id='gsc_prf_in')
            if name is None:
                name='NA'
            else:
                name=name.text
            
            
            affilation=soup.find('div', class_='gsc_prf_il')
            if affilation is None:
                affilation='NA'
            else:
                affilation=affilation.text
        
            for info2 in soup.find_all('a', class_='gsc_prf_inta gs_ibl'):
                # print('----')
                # print(info2.text)
                if info2 is None:
                    info_second=['NA']*10
                else:
                    info_second.append(info2.text)
            
            interest='/'.join(info_second)
                
                    
            homepage_links=scrape_google(name + ' homepage')
            substring1='translate'
            for homepage in homepage_links:
                if substring1 in homepage:
                    continue
                else:
                    homepage_embed=homepage
                    break
                
            
            for info3 in soup.find_all('span', class_='gsc_g_al'):
                # print(info3.text)
                info_third.append(info3.text)
            
            if len(info_third)==0:
                print('Google scholar link is invalid')
                continue
     
     
                    
            researcher_info=researcher_info.append({str(columns[4]):info_first[0],
                                                    str(columns[6]):info_first[1],
                                                    str(columns[2]):info_first[2],
                                                    str(columns[5]):info_first[3],
                                                    str(columns[0]):name,
                                                    str(columns[7]):homepage_embed,
                                                    str(columns[1]):affilation,
                                                    str(columns[8]):interest,
                                                    str(columns[9]):researcher_google_scholar[index],
                                                    str(columns[3]):info_third[len(info_third)-2]

                                                        }, ignore_index=True)
        
        
        else:
            continue
        
    return researcher_info

def area_of_interest(data):
    data=data_wos
    columns=data.columns
    
    interest=list(data[columns[8]])
    new_interest=[]
    count=0
    for text in interest:
        splited_text = text.split("/")
        for text1 in splited_text:
            count=count+1
            new_interest.append(text1)

    
    

if __name__=='__main__':
    data_wos=get_info(google_scholar_list)
    data_wos.to_csv('data.csv')
    



