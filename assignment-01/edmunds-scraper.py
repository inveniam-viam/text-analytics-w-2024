#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup # documentation available at : www.crummy.com/software/BeautifulSoup/bs4/doc/
#import unicodedata # works with string encoding of the data

entries: list = []
entry: list = []
urlnumber: int = 2 # Give the page number to start with


while urlnumber < 100: # Give the page number to end with

    url: str = f"https://forums.edmunds.com/discussion/7526/general/x/midsize-sedans-2-0/p{urlnumber}"

    try:
        r = requests.get(url, timeout = 10) # Sending a request to access the page
    except requests.exceptions.RequestException as e:
        print("Error message:",e)
        break

    data = r.text
    
    soup = BeautifulSoup(data, 'lxml') # Getting the page source into the soup
    
    for div in soup.find_all('div'):
        entry: list = []
        if(div.get('class') is not None and div.get('class')[0] == 'Comment'): # A single post is referred to as a comment. Each comment is a block denoted in a div tag which has a class called comment.
            ps = div.find_all('p') # gets all the tags called p to a variable ps
            aas = div.find_all('a') # gets all the tags called a to a variable aas
            spans = div.find_all('span')
            times = div.find_all('time') # used to extract the time tag which gives the iDate of the post

            concat_str: str = ''
            for strings in aas[1].contents: # prints the contents that is between the tag start and end
                if strings != "<br>" or strings != "<br/>": # breaks in post which we need to work around
                    concat_str = (concat_str + ' '+ strings).encode("utf-8").strip() # the format extracted is a unicode - we need a uniform structure to work with the strings
            entry.append(concat_str)

            concat_str: str = ''
            for strings in times[0].contents:
                if strings != "<br>" or strings != "<br/>":
                    concat_str = (concat_str + ' '+ strings).encode('iso-8859-1').strip()
            entry.append(concat_str)

            for div in div.find_all('div'):
                if (div.get('class') is not None and div.get('class')[0] == 'Message'): # extracting the div tag with the class attribute as message
                    blockquotes = []
                    x = div.get_text()
                    for bl in div.find_all('blockquote'):
                        blockquotes.append(bl.get_text()) # block quote is used to get the quote made by a person. get_text helps to eliminate the hyperlinks and pulls out only the data.
                        bl.decompose()
                    # Encoding the text to ascii code by replacing the non-ascii characters
                    ascii_encoding = div.get_text().replace("\n"," ").replace("<br/>","").encode('ascii','replace')
                    # Convert the ASCII encoding to Latin1 encoding
                    latin1_encoding = ascii_encoding.decode('ascii').encode('iso-8859-1')
                    # Append the encoding bytes to output list
                    entry.append(latin1_encoding)

                    for bl in blockquotes:
                        ascii_encoding = bl.replace("\n"," ").replace("<br/>","").encode('ascii','replace')
                        latin1_encoding = ascii_encoding.decode('ascii').encode('iso-8859-1')
                        entry.append(latin1_encoding)

            entries.append(entry)
      
    urlnumber += 1

# Convert a list of byte to list a of string     
stringlist=[[x.decode('iso-8859-1') for x in entry] for entry in entries]
# Save the list to a csv file
with open('edmunds_extraction.csv', 'w') as output:
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerows(stringlist)

print("Wrote to edmunds_extraction.csv")
