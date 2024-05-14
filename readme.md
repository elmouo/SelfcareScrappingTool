# Web Scraping Tool

This Python script is designed for web scraping purposes, specifically tailored to extract data from the [Belfius/ slefcare Q&A (fr)](https://www.belfius.be/webapps/fr/selfcare/belfius/) webpages. It utilizes Selenium and BeautifulSoup libraries to navigate through web pages, extract relevant information, and save it locally.

## Features

- Extracts frequently asked questions (FAQs) and category-wise questions from the Belfius website.
- Cleans HTML content by removing unwanted elements.
- Organizes extracted data into a structured folder hierarchy.
- Supports headless browsing for efficient data extraction.

## Folder Structure

The extracted data is organized in the following structure:

```
├── DestinationFolder/                  # Root folder for extracted data
│   ├── FAQ/                       # Folder for frequently asked questions
│   │   ├── index.html             # HTML file containing FAQ section
│   │   ├── FAQ_Page_1.html        # HTML file for FAQ question 1
│   │   ├── FAQ_Page_2.html        # HTML file for FAQ question 2
│   │   └── ...                    

│   ├── Fraud_question1/     
    ├── Fraud_question2/  
    ├── ....    
    ├── Credit_subcategory1_question1 
    ├── Credit_subcategory1_question1    
    ├── ....              
│   ├── 

```

## Dependencies

- [Python 3.x](https://www.python.org/)
- [Selenium](https://pypi.org/project/selenium/): Selenium is a powerful framework for automating web browsers.
It provides a set of libraries and APIs for interacting with web elements, navigating through web pages, and executing JavaScript on web pages.
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Chrome WebDriver](https://chromedriver.chromium.org/downloads/version-selection) installed and added to your system PATH: ChromeDriver acts as a bridge between your Selenium WebDriver tests and the Chrome browser.
It starts a Chrome browser instance and sends commands to it via WebDriver's wire protocol.

