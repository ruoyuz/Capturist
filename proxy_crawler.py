from crawler import *
from bs4 import BeautifulSoup
import re

class proxyCrawler(Crawler):
  proxy_list = []

  def __init__(self):
    Crawler.__init__(self)
    self.task_link = "http://hidemyass.com/proxy-list/" # proxy source site

  def getProxy(self,line):
    soup = line
    item_set = soup.find_all('td')
    blacklist = self.getBlacklist(item_set[1].span.style.get_text())
    item_set[1].span.style.extract()
    
    # filter the content for correct IP address according to blacklist
    for black in blacklist:
      for item in item_set[1].find_all(attrs={'class':black}):
	item.extract()
    for item in item_set[1].find_all(attrs={'style':'display:none'}):
      item.extract()
    
    p_ip = item_set[1].get_text().encode('ascii','ignore')

    p_port = item_set[2].get_text()[1:].encode('ascii','ignore')
    p_type = {'HTTP':'http','HTTPS':'https','socks4/5':'socks5'}[item_set[6].get_text()]
    p_country = item_set[3].get_text()[1:].encode('ascii','ignore')

    return {'ip':p_ip,'port':p_port,'type':p_type,'country':p_country}
  
  def getBlacklist(self,style):
    blacklist = []
    for s in re.findall(r'\.{1}[\w-]+\{display:none\}',style):
      blacklist += [s[1:-14]]
    return blacklist

  def getList(self):
    if not self.isRunning():
      self.get(self.task_link)
    self.updateFilter()
    time.sleep(1)
    soup = BeautifulSoup(self.driver.page_source)
    for line in soup.tbody.find_all('tr'):
      proxy = self.getProxy(line)
      if proxy in self.proxy_list:
	break
      self.proxy_list += [proxy]
    return self.proxy_list

  def removeProxy(self,proxy):
    if proxy in self.proxy_list:
      self.proxy_list.remove(proxy)

  def updateFilter(self):
    # define browser operations to filter the proxy provided by website
    checks = [self.driver.find_element_by_id('allCountries'),
              self.driver.find_element_by_id('allPorts'),
              self.driver.find_element_by_xpath("//input[@name='pr[]'][@value='0']"),
              self.driver.find_element_by_xpath("//input[@name='a[]'][@value='0']"),
              self.driver.find_element_by_xpath("//input[@name='a[]'][@value='1']"),
              self.driver.find_element_by_xpath("//input[@name='a[]'][@value='2']"),
              self.driver.find_element_by_xpath("//input[@name='a[]'][@value='3']"),
              self.driver.find_element_by_xpath("//input[@name='a[]'][@value='4']"),
              self.driver.find_element_by_xpath("//input[@name='sp[]'][@value='3']"),
              self.driver.find_element_by_xpath("//input[@name='ct[]'][@value='3']")]
    unchecks = [self.driver.find_element_by_name('pl'),
                self.driver.find_element_by_xpath("//input[@name='pr[]'][@value='1']"),
                self.driver.find_element_by_xpath("//input[@name='pr[]'][@value='2']"),
                self.driver.find_element_by_xpath("//input[@name='sp[]'][@value='1']"),
                self.driver.find_element_by_xpath("//input[@name='sp[]'][@value='2']"),
                self.driver.find_element_by_xpath("//input[@name='ct[]'][@value='1']"),
                self.driver.find_element_by_xpath("//input[@name='ct[]'][@value='2']")]
    for item in checks:
      if not item.is_selected():
        item.click()
    for item in unchecks:
      if item.is_selected():
	item.click()
    update = self.driver.find_element_by_id('updateresults')
    update.click()

def main(args):
  cub = proxyCrawler()
  cub.getList()
  for line in cub.proxy_list:
    print line
  cub.stop()
  print 'Done.'

if __name__=='__main__':
  main(sys.argv[1:])
    
