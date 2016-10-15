_author_ = 'Vivek'

from bs4 import BeautifulSoup

import mechanize
import csv
import sys
import urllib
import re
import os
import requests

path = "C:\dummyfolder"

if not os.path.exists(path):    # create folder is not existing
    os.makedirs(path)

url = "https://www.ffiec.gov/nicpubweb/nicweb/HCSGreaterThan10B.aspx"   # adding url
br = mechanize.Browser()    # initializing mechanize browser method
br.open(url)    # opening url
br.select_form(nr=0)

totallist = []
#rr = urllib.urlopen(url)

rr = requests.get(url).text
soup1 = BeautifulSoup(rr,'html.parser') # initializing soup1 with html data of webpage
data1 = []
total1 = []
header1 = True

bodytag1 = soup1.find_all("table", class_='datagrid')   # finding all table rows
for tag in bodytag1:
    cols = tag.find_all('tr')

for link in cols:   # looping through columns
    if(header1):
        a = link.find_all('th') # finding table header
    else:
        a=link.find_all('td')   # finding table data
    #data1.append(a[0].text)
    if(header1):
        data1.append(a[1].text) # appending data to list
    else:
        data1.append(a[1].find('a').text)
    data1.append(a[2].text)
    if(header1):
        data1.append(a[3].text)
    else:
        data1.append(re.sub("[^\d\.]", "", a[3].text))  # regex to remove $ and , from assert column data
    total1.append(data1)
    data1=[]
    header1 = False

with open('C:/dummyfolder/20160630.csv', 'w') as fff:   # creating first file
    writer = csv.writer(fff, lineterminator='\n')
    writer.writerows(total1)

for f in br.form.find_control('DateDropDown').get_items():  # finding all quarter names in the dropdown box
    totallist.append(f.name)

for quarters in totallist:  # looping through each quarter
    quarters = str(quarters)
    sys.stdout.write("Scraping Quarter "+quarters+"... ")
    sys.stdout.flush()
    br = mechanize.Browser()
    br.open(url)
    br.select_form(nr=0)
    br.form["DateDropDown"] = [''+quarters+'']  # targeting specific quarter data
    r = br.submit()
    soup = BeautifulSoup(r.read(), 'html.parser')

    data = []
    total = []
    header = True
    cols = []

    bodytag = soup.find_all("table", class_='datagrid')
    for tag in bodytag:
        cols = tag.find_all('tr')
    for link in cols:
        if (header):
            a = link.find_all('th')
        else:
            a = link.find_all('td')
        #data.append(a[0].text)

        if (header):
            data.append(a[1].text);
        else:
            data.append(a[1].find('a').text)
        data.append(a[2].text)
        if (header):
            data.append(a[3].text)
        else:
            data.append(re.sub("[^\d\.]", "", a[3].text))
        total.append(data)
        data = []
        header = False

        with open("C:/dummyfolder/"+quarters+".csv", "w") as f: # creating different quarter files
            writer = csv.writer(f,lineterminator='\n')  # lineterminate by a new line
            writer.writerows(total) # writing list data to csv
    print " File created."