import urllib2
from bs4 import BeautifulSoup

url = 'http://www.smogon.com/bw/moves/'

usock = urllib2.urlopen(url)
data = usock.read()
usock.close()

#soup = BeautifulSoup(data)

#table = soup.find('table')

#headers  = [header.text for header in table.find_all('th')]

#rows = []

#for row in table.find_all('tr'):
    #rows.append([val.text.encode('utf8').strip() for val in row.find_all('td')])