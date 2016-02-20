import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import threading
import json

subject_names = {}
subject_regex = re.compile("[A-Z]{2}[0-9]+?")
ugSubjectsUrl = 'https://erp.iitkgp.ernet.in/ERPWebServices/curricula/'
ugSubjectsUrlEnd = 'specialisationList.jsp?stuType=UG'
proxies = {
  "http": "http://10.3.100.207:8080",
  "https": "https://10.3.100.207:8080",
}
visited_links = set()
executor = ThreadPoolExecutor(max_workers=20)
futures = []
elective_futures = []

def parsePage(url):
    if url in visited_links:
        return
    else:
        visited_links.add(url)
    r = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(r.text)
    rows = soup.findAll('tr')
    for row in rows:
        tds = row.findAll('td')
        if len(tds) < 4:
            continue
        if "DEPTH" in tds[1].get_text():
            code = tds[2].get_text().strip()
            name = tds[3].get_text().strip()
            credit = tds[5].get_text().strip()
            subject_names[code] = [name, credit]
        elif "ELECTIVE" in tds[1].get_text():
            link = tds[1].find("a")["href"]
            elective_futures.append(
                executor.submit(partial(parsePage, ugSubjectsUrl + link)))
            
        elif subject_regex.match(tds[1].get_text()):
            code = tds[1].get_text().strip()
            name = tds[2].get_text().strip()
            credit = tds[4].get_text().strip()
            subject_names[code] = [name, credit]

response = requests.get(ugSubjectsUrl+ugSubjectsUrlEnd,proxies=proxies)
soup = BeautifulSoup(response.text)
links = soup.findAll('a')
for link in links:
    futures.append(
        executor.submit(partial(parsePage, ugSubjectsUrl + link["href"])))
for f in futures:
    f.result()
for f in elective_futures:
    f.result()
with open('result.json', 'w') as f:
    json.dump(subject_names, f)
