'''
    Script to calculate branch-rank of a KGPian

    Instructions for pre-requisites installation at https://github.com/Demfier/Get-branch-rank

    HOW TO USE:
    1. Run the script in your terminal as:
    >> python get_branch_rank.py
    2. Enter your roll number and then wait for some time, you will get your rank.
'''

import requests
from bs4 import BeautifulSoup

# For disabling the InsecurePlatForm warnings
#import requests.packages.urllib3
#import urllib3
#urllib3.disable_warnings()

DEBUG = True
VERBOSE = False

import sys

BASE_URL = 'https://erp.iitkgp.ernet.in/StudentPerformance/view_performance.jsp?rollno='


def get_cg(url):
    '''returns CGPA of a student given his/her profile link or returns appropriate
        error otherwise
    '''

    cgpa = ''
    try:
        r = requests.Session()
        r.mount("https://", requests.adapters.HTTPAdapter(max_retries=2))
        response = r.get(url)
        response.raise_for_status()
    except requests.Timeout:
        print('error: timed out for', url[len(BASE_URL):])
        return 0
    except requests.ConnectionError:
        print('error: connection problem for', url[len(BASE_URL):])
        return 0
    except requests.HTTPError:
        print('error: invalid HTTP response for', url[len(BASE_URL):])
        return 0
    except requests.exceptions.ChunkedEncodingError as e:
        print('error: ChunkedEncodingError', url[len(BASE_URL):])
        return 0
    soup = BeautifulSoup(response.text.replace('&nbsp', ''), 'lxml')
    tds = soup.find_all('td')
    for idx, td in enumerate(tds):
        if td.text.strip() == 'CGPA':
            cgpa = tds[idx + 1].text
            return cgpa


def get_rank(cg_list, mycg):
    '''
    Given list of CGPA obtained by the script and mycg from student roll number,
    returns rank of the student
    '''
    sorted_list = []
    rank = 1
    for stud in cg_list:
        cg = stud.values()[0]
        # check for existent cg
        if bool(cg) and float(cg) > float(mycg):
            rank += 1
    return rank


def check_roll_and_return_cg(rollno):
    '''Validates the given roll number and return CGPA if found valid'''
    if (DEBUG):
        print "We are going to get your CGPA now"
    mycg = ''
    url = BASE_URL + rollno
    # print url
    try:
        r = requests.Session()
        r.mount("https://", requests.adapters.HTTPAdapter(max_retries=2))
        response = r.get(url)
        if DEBUG:
            print "We were able to fetch your CGPA"
        response.raise_for_status()
    except requests.Timeout:
        print('error: timed out', url)
        return 0
    except requests.ConnectionError:
        print('error: connection problem', url)
        return 0
    except requests.HTTPError:
        print('error: invalid HTTP response', url)
        return 0
    except requests.exceptions.ChunkedEncodingError as e:
        print('error: ChunkedEncodingError', url)
        return 0

    soup = BeautifulSoup(response.text.replace('&nbsp', ''), 'lxml')
    tds = soup.find_all('td')
    for idx, td in enumerate(tds):
        if td.text.strip() == 'CGPA':
            mycg = tds[idx + 1].text
            if DEBUG:
                print "Your CGPA was found to be %s" % mycg
            return mycg

if __name__ == '__main__':
    rollno = raw_input('Enter your roll number: ')
    rollno = rollno.replace(' ', '').upper()
    print 'Okay, sit tight. We will figure out your rank now!'
    mycg = check_roll_and_return_cg(rollno)
    if not mycg or mycg == '':
        print 'Oh! There seems to be an issue. Try again later, please'
        sys.exit(0)
    cg_list = []
    # varialble to keep track of invalid roll numbers
    invalid_roll_count = 0
    # the final two digits of a roll number
    index = 1

    if DEBUG:
        print "We will now find the CGPA of all the students in your course: "

    # if no roll number found for 5 times continuously I'll assume the branch's student list has ended
    while invalid_roll_count < 6:
        cg_json = {}

        # roll number genrated by the script
        dynamic_roll = rollno[:-2]
        if index < 10:
            dynamic_roll += '0' + str(index)
        else:
            dynamic_roll += str(index)
        # print dynamic_roll
        url = BASE_URL + dynamic_roll
        if dynamic_roll == rollno:
            pass
        cgpa = get_cg(url)
        if not bool(cgpa):
            invalid_roll_count += 1
            # print 'invalid_roll_count', invalid_roll_count
            index += 1
            continue

        if DEBUG:
            print "CGPA of %s is %s" %(dynamic_roll, cgpa)

        if VERBOSE:
            print url
        invalid_roll_count = 0
        index += 1
        cg_json[dynamic_roll] = cgpa
        cg_list.append(cg_json)
    if VERBOSE:
        print cg_list
    print 'Your CGPA: ', mycg
    final_rank = get_rank(cg_list, mycg)
    print 'Your branch rank is %d out of %d students in your course' % \
    (final_rank, len(cg_list))
