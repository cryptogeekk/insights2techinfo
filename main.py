#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 14:02:28 2021

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

insights_url='https://insights2techinfo.com/highly-cited-researchers-list/'


def get_researcher_list(url):
    tables=pd.read_html(insights_url)
    researcher_list=tables[0]
    researcher_list=researcher_list.drop(['S.No'], axis=1)
    return researcher_list


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

# temp_link=get_researcher_list(insights_url)


def get_info():
    researcher_info=pd.DataFrame(columns=['Name', 'Affilation','H-index', 'Citations 2020', 'Total_citation', 'H-index_since_2016', 'Citation_since_2016', 'HomePage','Area of Research', 'Google_Scholar'])
    
    researchers_list=get_researcher_list(insights_url)
    columns=researcher_info.columns
    columns1=researchers_list.columns
    researcher_google_scholar=researchers_list[columns1[1]]
    
    # print(researcher_google_scholar[54])
    
    for index in range(0, len(researcher_google_scholar)):
        substring='scholar'
        if substring in researcher_google_scholar[index]:   
            print(index, ':', len(researcher_google_scholar))
            info_first=[]
            info_second=[]
            info_third=[]
            # r=requests.get('https://scholar.google.com/citations?user=pxzB3EwAAAAJ&hl=en')
            r=requests.get(researcher_google_scholar[index])
            soup=BeautifulSoup(r.content, 'html5lib')
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
        
            for info2 in soup.find_all('div', class_='gsc_prf_il'):
                if info2 is None:
                    info_second=['NA']*10
                else:
                    info_second.append(info2.text)
                    
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
                                                    str(columns[8]):info_second[2],
                                                    str(columns[9]):researcher_google_scholar[index],
                                                    str(columns[3]):info_third[len(info_third)-2]

                                                        }, ignore_index=True)
        
        
        else:
            continue
        
    return researcher_info
    

if __name__=='__main__':
    data=get_info()
    data.to_csv('data.csv')


        




















# researchers_list=get_researcher_list(insights_url)
# columns=researchers_list.columns
# researcher_google_scholar=researcher_list[columns[1]]

# first_url=researcher_google_scholar[1]
# r=requests.get(first_url)
# print(r.content)

# from bs4 import BeautifulSoup
# soup=BeautifulSoup(r.content, 'html5lib')
# # print(soup.prettify())
# # print(soup.get_text())

# all_text=soup.prettify()
# match=soup.find('div', class_='gsc_rsb_s gsc_prf_pnl')
# citation_all=soup.find_all('td', class_='gsc_rsb_std')
# h_index=soup.find('td', class_='gsc_rsb_std')

# name= soup.find('div',id='gsc_prf_in')
# print(name.text)

# for info in soup.find_all('td', class_='gsc_rsb_std'):
#     print(info.text)

# print(citation.text)
# print(h_index.text)

# gsc_rsb_std
# print(match)


# text= "c++ linear search program"
# url = 'https://google.com/search?q=' + text
  
# # Fetch the URL data using requests.get(url),
# # store it in a variable, request_result.
# request_result=requests.get( url )
  
# # Creating soup from the fetched request
# soup = bs4.BeautifulSoup(request_result.text,"html.parser")
# filter=soup.find_all("h3")
# for i in range(0,len(filter)):
#     print(filter[i].get_text())



# names=list(researcher_info['Name'])
# for name in names:
#     homepage_embed='homepage'
#     print(name)
#     homepage_links=scrape_google(name + ' homepage')
#     # print('homepage')
#     substring1='translate'
#     for homepage in homepage_links:
#         print(homepage)
#         if substring1 in homepage:
#             continue
#         else:
#             homepage_embed=homepage
#             print(homepage_embed)
#             break

# homepage_links=scrape_google(names[0]+'homepage')
# substring1='translate'
# for homepage in homepage_links:
#     if substring1 in homepage:
#         print('True')
    
# substring1 in homepage_links[1]



# researcher_info.to_csv('researcher_info')
