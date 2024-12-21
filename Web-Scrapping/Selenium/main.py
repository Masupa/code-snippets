import time
from selenium import webdriver
from selenium.webdriver.common.by import By


# Initiative instance of Chrome Webdrive
chrome_driver = webdriver.Chrome()

# Navigate to URL
URL = "https://quotes.toscrape.com/"
chrome_driver.get(URL)

# Wait for page to load
time.sleep(10)

# Interact with page
title_element = chrome_driver.find_element(By.LINK_TEXT, "Quotes to Scrape")
print(title_element.text)

# Note: Find elements finds all HTML elements that match the given search parameter
quotes = chrome_driver.find_elements(By.CLASS_NAME, "quote")
for quote in quotes:
    quote_text = quote.find_element(By.CLASS_NAME, "text")
    author = quote.find_element(By.CLASS_NAME, "author")

    tags_list = []
    tags = chrome_driver.find_elements(By.CLASS_NAME, "tags")
    for tag in tags:
        tags_list.append(tag.find_element(By.CLASS_NAME, "tag").text)

    print(f"Quote: {quote_text.text}")
    print(f"Author: {author.text}")
    print(f"Tags: {tags_list}")
    print(" ")

chrome_driver.close()
