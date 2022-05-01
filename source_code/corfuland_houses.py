# -*- coding: utf-8 -*-

#import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver


# Save the base url of the site
base_url = 'http://www.corfuland.gr'
# Get a response of the listing page
url = 'http://www.corfuland.gr/el/mikres-aggelies-kerkyra/aggelies-enoikiasis-katoikiwn-stin-kerkyra'

# page = requests.get(url)

driver = webdriver.Firefox()
driver.get(url)

page = driver.page_source

# Create a BeautifulSoup object from the response
soup = BeautifulSoup(page, 'html.parser')

# Find every element with the tag <td> and the class "name"
# (You usually need to take a look at the site's code to know what to search for)
listings = soup.find_all('a', class_='title')
# Do the same for the class date_start
dates = soup.find_all('td', class_='date_start')

# print(type(listings))
# print(listings)
# print(soup)
# print(len(listings))
# print(len(dates))

# Create empty lists to save the data
listing_urls = []
listing_dates = []
listing_titles = []

# For every element in the listings and dates lists getthe url, the title
# and the date and append the to the corresponding list
for i, listing in enumerate(listings):
    # listing_url = base_url + listing_url['href']
    listing_url = base_url + listing['href']
    listing_title = listings[i].string
    # listing_title = listing.find('a')
    listing_date = dates[i].string

    listing_urls.append(listing_url)
    listing_dates.append(listing_date)
    listing_titles.append(listing_title)

# Search the log to see if there are any new houses
new_listings = []
with open('log.txt', 'r+', encoding="utf-8") as f:
    # Get the contents of log.txt
    log = f.read()
    # For every listing, see if its url is already in the file
    for i, url in enumerate(listing_urls):
        msg = str(listing_titles[i] + ", " + listing_dates[i] + ", " + url)
        # We only care about houses for rent
        if 'Ενοικιάζεται' in msg:
            if url not in log:
                new_listings.append(msg)
                f.write(msg + "\n")

# Send an email notifying you about the new houses
import smtplib, ssl

# Connection parameters
port = 465  # For SSL
smtp_server = "smtp.gmail.com"

# You can change the inputs to be hardcoded (or save them in a separate file for more safety)
# in order to automate the process
sender_email = input("Choose an email to send it from ")  # Enter your address
password = input("Enter your password to continue ")
receiver_email = input("Choose an email to send the mail to ")  # Enter receiver address
msg = """\
Subject: Νέα σπίτια

Τα νέα σπίτια προς ενοικίαση είναι:\n"""

# Append the new listings in the mail
for listing in new_listings:
    msg += listing + "\n"

# Force the msg to be encoded in utf-8 or there might be compatibility issues
msg = str(msg).encode('utf-8')

# Connect to the mailing server and send the mail
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg)