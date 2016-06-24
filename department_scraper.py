import requests
from bs4 import BeautifulSoup
import sys
import json

url="http://iitkgp.ac.in"
departmentNames=[]

#get the response
response=requests.get(url)
if response.status_code is not 200:
	print "Network error"
	sys.exit()

soup=BeautifulSoup(response.text,"lxml")
#refine the response by getting only the div "tabb1"
refined_response=soup.find("div",{"id":"tabb1"})
soup1=BeautifulSoup(str(refined_response),"lxml")
#get the department names from the links
for link in soup1.findAll("a"):
	departmentNames.append(link.string)

with open('result.json', 'w') as f:
    json.dump(departmentNames, f)

