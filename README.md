Capturist - A Web Content Acquisition Tool
==========================================

Installation and Setup
----------------------

  1. Capturist uses bs4 and selenium modules. Please make sure these modules are installed before using Capturist. You can use pip for installation:
       pip install BeautifulSoup4
       pip install selenium

  2. Current version support Firefox, Chrome and PhantomJS as operating browser. By default it uses Firefox. Please call your_crawler.setConf(browser=="name of browser") for selection.

  3. For headless usage, please install PhantomJS (http://phantomjs.org/) and modify __phantomjs_path__ term in crawler.py.

  4. Auto proxy setting can be applied when executing run.py, by 'python run.py --proxy' in command line. The performance may be limited by the proxy if enabled.

Introduction
------------

  1. crawler.py:
    A crawler class provides basic operations.

  2. proxy_crawler.py:
    A site crawler that acquires available proxy list from a proxy provider (http://hidemyass.com) for auto proxy setting of other crawlers.

  3. storm8_crawler.py:
    A site crawler with specific behaviors. For this example (http://storm8.com), it can do breath first search for pages of specific content, and capture game infomation.

  4. run.py:
    A script aiming to acquire information of all games on Storm8 (http://storm8.com). It will do a BFS first to find the game info page, then start capturing process in multithreads and save all the information to a file game_info.txt.
