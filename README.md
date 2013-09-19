Capturist - for Web Content Acquisition
=======================================

Installation and Setup
----------------------

  1. Capturist is based on Python and uses BeautifulSoup and Selenium modules. Please make sure these modules are installed before using Capturist. You can use pip for installation:

       __pip install BeautifulSoup4__
     
       __pip install selenium__


  2. Current version support Firefox, Chrome and PhantomJS as operating browser. By default it uses Firefox. Please use __your_crawler.setConf(browser=="name_of_your_browser")__ for selection.


  3. For headless usage, please install PhantomJS (http://phantomjs.org/) and modify __phantomjs_path__ term in __crawler.py__.


  4. Auto proxy setting can be applied when executing run.py, by __'python run.py --proxy'__ in command line. The performance may be limited by the proxy if enabled.


Instruction
-----------


  1. __crawler.py__:

       A crawler class provides basic operations.


  2. __proxy_crawler.py__:

       A site crawler that acquires available proxy list from a proxy provider (http://hidemyass.com) for auto proxy setting of other crawlers.


  3. __storm8_crawler.py__:
 
       A site crawler with specific behaviors. For this example (http://storm8.com), it can do breath first search for pages of specific content, and capture game infomation.


  4. __run.py__:

       A script aiming to acquire information of all games on Storm8 (http://storm8.com). It will do a BFS first to find the game info page, then start capturing process in multithreads and save all the information to a file game_info.txt.
