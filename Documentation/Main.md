#Main

* This app uses Selenium (in Python) to scrape real estate websites

* The scraped data is mostly stored in a DB using Asp.NET but images are stored in folders.

* The data is collected as an interactive map in the browser using Javascript.

* The data can be filtered and sorted in various ways to visualise different information, these filters are modular so they can be hot-swapped, they're found under ScrapeSystem/FilterModules.

* The scraper has a main section but individual real estate websites get their own ScrapeModule since each web DOM is different. 