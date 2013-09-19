import sys,time
from selenium import webdriver

class Crawler(object):
  name = ''
  driver = None
  browser = ''
  task_link = ''  # current task
  __service_args__ = None # addons and proxy for browser
  __phantomjs_path__ = "" # path to phantomjs
  __is_running__ = False

  def __init__(self):
    self.browser='Firefox'
    self.name = 'Ichiro'

  def setName(self,new_name):
    self.name = new_name

  def get(self,link):
    self.run()
    self.driver.get(link)
    self.task_link = link
    return self.driver.page_source

  def setConfig(self,browser=None,proxy={}):
    if browser:
      self.browser=browser;
    
    if self.browser=='Firefox':
      self.__service_args__ = webdriver.FirefoxProfile()
      if proxy:
        self.__service_args__.set_preference("network.proxy.type",1)
        self.__service_args__.set_preference("network.proxy.http",proxy['ip'])
        self.__service_args__.set_preference("network.proxy.http_port",proxy['port'])
      self.__service_args__.update_preferences()

    elif self.browser=='PhantomJS':
      if proxy:
	self.__service_args__ = ['--proxy='+proxy['ip']+':'+proxy['port'],'--proxy-type='+proxy['type']]

    elif self.browser=='Chrome':
      self.__service_args__ = webdriver.chrome.options.Options()
      if proxy:
        self.__service_args__.add_argument("--proxy-server=%s" % proxy['ip']+':'+proxy['port'])

    else:
      raise Exception("Browser type could not be identified.")

  def run(self):
    if self.__is_running__:
      return True

    if self.browser=='Firefox':
      self.driver = webdriver.Firefox(firefox_profile=self.__service_args__)
      self.__is_running__ = True
    elif self.browser=='PhantomJS':
      self.driver = webdriver.PhantomJS(self.__phantomjs_path__, service_args=self.__service_args__)
      self.__is_running__ = True
    elif self.browser=='Chrome':
      self.driver = webdriver.Chrome(chrome_options=self.__service_args__)
      self.__is_running__ = True
    else:
      self.__is_running__ = False
      raise Exception("Crawler could not be started, Check browser settings.")

    return self.__is_running__

  def stop(self):
    if not self.__is_running__:
      return True

    self.driver.quit()
    self.__is_running__ = False
    return True

  def isRunning(self):
    return self.__is_running__

def main(argv):
  link = argv[0]
  cub = Crawler()
  cub.get(link)
  time.sleep(1)
  cub.driver.refresh()
  time.sleep(1)
  cub.driver.save_screenshot("crawler_screenshot.png")
  cub.stop()
  print 'Done.'

if __name__=='__main__':
  main(sys.argv[1:])
