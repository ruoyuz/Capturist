from crawler import *
import re, random, os, pickle, codecs, urlparse
from bs4 import BeautifulSoup

class storm8Crawler(Crawler):
  info_pattern = "<h2>All Games</h2>" # pattern for valid info page
  visit = [] # links to visit
  visited = [] # links visited
  
  def siteBFS(self,link):
    # do a BFS to find the info page
    self.visited.append(link)
    if link in self.visit:
      self.visit.remove(link)
    source = self.get(link)
    match_obj = re.search(self.info_pattern, source, re.M|re.I)
    if match_obj:
      print "Pattern found on:",link
      return link
    else:
      soup = BeautifulSoup(source)
      for item in soup.find_all(href=re.compile("^(?:(?!http).)*$")):
        l = urlparse.urljoin(link, item.get('href'))
        if not (l in self.visit or l in self.visited):
          self.visit.append(l)
      if not self.visit:
	print "No pattern found in the whole site."
	return None
      else:
	print "No pattern found. Visiting next link."
	return self.siteBFS(self.visit[0])

  def getLinks(self,link):
    # extract links to individual games
    self.get(link)
    items = self.driver.find_elements_by_css_selector('.col.gameInfo')
    print "Found list items:", len(items)
    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1) # seconds
    while len(self.driver.find_elements_by_css_selector('.col.gameInfo')) > len(items):
        items = self.driver.find_elements_by_css_selector('.col.gameInfo')
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	print "Found list items:", len(items)
        time.sleep(1)

    links = []
    soup = BeautifulSoup(self.driver.page_source)
    for item in soup.find_all('h2'):
      if item.a:
	l = urlparse.urljoin(self.task_link, item.a.get('href'))
      if not l in links:
	links += [l]
    print "Found",len(links),"games."
    return links

  def getGame(self,link):
    # get game information
    soup = BeautifulSoup(self.get(link))
    if not soup.find("div",{"id":"gameDetail"}):
      print "Invalid game page."
      return None
    name = soup.find("div",{"class":"detailContent"}).h1.get_text()
    claim = soup.find("div",{"class":"detailContent"}).h2.get_text()
    intro = soup.find("div",{"class":"detailContent"}).p.get_text()
    studio = soup.find("div",{"class":"details"}).find('p',{'class':'studio'}).get_text()[8:]
    categ = [tag.get_text() for tag in soup.find("div",{"class":"details"}).find('p',{'class':'tags'}).find_all('a')]
    applink = {}
    for avail in soup.find('div',{'class':'detailContent'}).find('div',{'class':'platforms large'}).ul.find_all('li'):
      applink[avail.get('class')[0]] = avail.a.get('href')
    
    print name,"is acquired."
    return {'name':[name],
            'studio':[studio],
	    'categories':categ,
            'claim':[claim],
	    'intro':[intro],
	    'link':[link],
	    'applink':applink}

def main(argv):
  cub = storm8Crawler()
  print cub.getGame(argv[0])
  cub.stop()
  return

if __name__=="__main__":
  main(sys.argv[1:])
