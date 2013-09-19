from threading import Thread
from Queue import Queue
from time import sleep
from proxy_crawler import *
from storm8_crawler import *

linkQ = Queue() # Queue for task links
crawlerQ = Queue() # Queue for working crawlers
infoQ = Queue() # Queue for captured game info
NUM = 2 # number of threads to use
storm8 = "http://www.storm8.com" # target site address

def maskCrawler(crawler,proxy_list):
  # automatic proxy loading
  if proxy_list:
    crawler.setConfig(browser='Chrome',proxy=proxy_list.pop())
    return crawler
  else:
    raise Exception("No proxy available.")

def saveGameInfo(game_info):
  # save to a text file
  f = open("game_info.txt","w+")
  for game in game_info:
    for key in ['name','studio','categories','link','claim','intro']:
      f.write(key+':'+'\n')
      for item in game[key]:
	f.write(item.encode('ascii','ignore')+'\n')
      f.write('\n')
    f.write('applink'+':'+'\n')
    for plat in game['applink']:
      f.write('-'+plat.encode('ascii','ignore')+': '+game['applink'][plat]+'\n')
    f.write('\n\n')
  f.close()
  print "File game_info.txt saved."


def collectGameInfo():
  # task to do in multithreads
  while True:
    worker = crawlerQ.get()
    if not worker:
      pass
    else:
      link = linkQ.get()
      infoQ.put(worker.getGame(link))
      time.sleep(1) # second
      if linkQ.empty():
	worker.stop()
      else:
        crawlerQ.put(worker)
      linkQ.task_done()

def main(args):
  use_proxy = False
  if args and args[0]=="--proxy":
    print "Proxy enabled."
    use_proxy = True
  
  if use_proxy:
    # get proxy list
    print "Acuiring proxy list."
    proxy_catcher = proxyCrawler()
    proxy_list = proxy_catcher.getList()
    proxy_list.reverse()
    proxy_catcher.stop()
    for p in proxy_list:
      print p

  if use_proxy:
    explorer = maskCrawler(storm8Crawler(),proxy_list)
  else:
    explorer = storm8Crawler()
  print "Start BFS search for information page."
  info_page = explorer.siteBFS(storm8)
  for link in explorer.getLinks(info_page):
    linkQ.put(link)
  explorer.stop()


  # fork queue of NUM thread
  for i in range(NUM):
    t = Thread(target=collectGameInfo)
    t.setDaemon(True)
    t.start()

  print "Task queue loaded."
  
  # assign crawlers
  for i in range(NUM):
    if use_proxy:
      worker = maskCrawler(storm8Crawler(),proxy_list)
    else:
      worker = storm8Crawler()
    crawlerQ.put(worker)

  print "Crawlers ready. Capturing."

  # waiting for all jobs done
  linkQ.join()

  game_info = []
  while not infoQ.empty():
    game_info += [infoQ.get()]

  saveGameInfo(game_info)

  print "Done."

if __name__=='__main__':
  main(sys.argv[1:])
