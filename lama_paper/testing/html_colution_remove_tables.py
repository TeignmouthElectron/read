# I got the html using the aspose-words library => try to find a new one
from bs4 import BeautifulSoup
import requests

soup = BeautifulSoup(open('test.html'), 'html.parser')

#To extract the tables from the html file
for table in soup.find_all('table'):
    table.extract()

y = soup.get_text()

# this is because of the library that I used uses Unicode for teh spaces \xa0
z = y.replace(u'\xa0',u' ')

z
