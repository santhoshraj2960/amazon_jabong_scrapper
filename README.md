# scrapy_python

Python scrapper scripts written using Scrapy framework to scrape data from Amazon and Jabong rearding fashion and clothing. This is a very old script written in 2016. Pretty sure the website structure should have been changed. 

Since I had this repo committed inside my other github account(https://github.com/santhosh2960) for which I lost access, I wanted to commit it from my new account.

The script scrapes data such as 
1. Title of the listed products
2. Sizes available for those products
3. Links to the other relevenet products recommended by Amazor or Jabong
4. Prices and Sellers available for the product
5. Description of the product such as colour, texture, etc
6. The complete sub category of the product such as (Fashion -> Men's Fashion -> T-shirts -> Round neck -> Full sleeve)
7. The scipt then saves the data into a Json file. ex: https://raw.githubusercontent.com/santhoshraj2960/amazon_jabong_scrapper/jabong_scrapper/jabong_scrapper/jabong_scrapper/jabong_items13.json

Requirements:
1) Scrapy 1.7
2) Python 2.7
3) Regex 3.7
4) A list of proxy ips

