import os
import re
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm  # Import tqdm for the progress bar

def remove_elements(html_content):
    """
    Removes unwanted elements from HTML content using BeautifulSoup.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    for element_id in ["onetrust-banner-sdk", "bandeau", "standaloneSearchbox", "onetrust-consent-sdk"]:
        element = soup.find("div", id=element_id)
        if element:
            element.decompose()
    header_elements = soup.find_all(["header", "div"], class_="header")
    for header_element in header_elements:
        header_element.decompose()
    return str(soup)

def clean_filename(filename, max_length=100):
    """
    Cleans the filename by replacing illegal characters and truncating it if necessary.
    """
    invalid_chars = r'[<>:"/\\|?*]'
    cleaned_filename = re.sub(invalid_chars, "_", filename)
    # Remove additional characters not allowed in Windows filenames
    cleaned_filename = re.sub(r'[:]', "", cleaned_filename)
    # Truncate filename if it exceeds max_length
    if len(cleaned_filename) > max_length:
        cleaned_filename = cleaned_filename[:max_length]
    return cleaned_filename

def extract_qa(href_url, text_content, folder_path, driver, category_name, section_name=""):
    for href, text in zip(href_url, text_content):
        if href and urlparse(href).scheme in ["http", "https"]:
            page_title = text
            if page_title:
                page_name = f"{category_name}_{section_name}_{clean_filename(page_title)}.html"
            else:
                page_name = "Page_Title_Unavailable.html"
            page_file_path = os.path.join(folder_path, page_name)
            
            # Check if the file already exists
            if os.path.exists(page_file_path):
                print(f"Skipping existing file: {page_file_path}")
                continue

            driver.get(href)
            time.sleep(5)
            page_html = remove_elements(driver.page_source)
            with open(page_file_path, "w", encoding="utf-8") as f:
                f.write(page_html)

def extract_faq_questions(driver, folder_path):
    """
    Extracts FAQ questions and saves their HTML content (home page).
    """
    faq_section = "FAQ"
    faq_folder = os.path.join(folder_path, faq_section)
    os.makedirs(faq_folder, exist_ok=True)
    
    home_html = remove_elements(driver.page_source)
    category_file_path = os.path.join(faq_folder, "index.html")
    with open(category_file_path, "w", encoding="utf-8") as f:
        f.write(home_html)
    
    section_faq = driver.find_elements(By.CSS_SELECTOR, "div.most-asked-question.ng-scope")
    faq_urls = [section.find_element(By.TAG_NAME, "a").get_attribute("href") for section in section_faq]
    faq_text = [section.find_element(By.TAG_NAME, "a").text for section in section_faq]
    
    extract_qa(faq_urls, faq_text, faq_folder, driver, "FAQ")

def extract_category_questions(driver, categories_urls, categories_text, folder_path):
    """
    Extracts questions from category pages and saves their HTML content.
    """
    dump_folder = os.path.join(folder_path, "Selfcare")
    os.makedirs(dump_folder, exist_ok=True)
    
    # Wrap categories_urls and categories_text with tqdm for a progress bar
    for category_href, category_text in tqdm(zip(categories_urls, categories_text), total=len(categories_urls), desc="Categories"):
        category_name = clean_filename(category_text.strip())
        print(category_name)
        driver.get(category_href)
        time.sleep(5)

        category_html = remove_elements(driver.page_source)

        question_links = driver.find_elements(By.CSS_SELECTOR, "div.sublevel a")
        
        if not question_links:
            sections = driver.find_elements(By.CSS_SELECTOR, "section.subject.ng-scope")
            href_sections = []
            href_sections_names = []
            for section in sections:
                href_element = section.find_element(By.CSS_SELECTOR, "h2 a")
                href_sections.append(href_element.get_attribute("href"))
                href_sections_names.append(href_element.get_attribute("text"))
                
            for href, section_name in zip(href_sections, href_sections_names):
                section_name_cleaned = clean_filename(section_name.strip())
                print(href)
                driver.get(href)
                time.sleep(5)
                question_links = driver.find_elements(By.CSS_SELECTOR, "div.sublevel a")
                question_urls = [link.get_attribute("href") for link in question_links]
                question_text = [link.text.strip() for link in question_links]

                extract_qa(question_urls, question_text, dump_folder, driver, category_name, section_name_cleaned)
        else:
            question_urls = [link.get_attribute("href") for link in question_links]
            question_text = [link.text.strip() for link in question_links]
            section_name = ""

            extract_qa(question_urls, question_text, dump_folder, driver, category_name, section_name)

def parse_and_save_site(url, folder_path):
    """
    Parses the site, extracts categories and FAQ questions, and saves HTML content.
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.cookies": 2}
    )

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    # Extract FAQ questions
    #extract_faq_questions(driver, folder_path)

    # Extract categories
    categories = driver.find_elements(By.CSS_SELECTOR, "ul.linkList.categories a")
    categories_urls = [link.get_attribute("href") for link in categories]
    categories_text = [link.text.strip() for link in categories]
    
    # Extract and save questions from category pages
    extract_category_questions(driver, categories_urls, categories_text, folder_path)

    driver.quit()

url = "https://www.belfius.be/webapps/fr/selfcare/belfius/"
folder_path = "selfcare_dump"
parse_and_save_site(url, folder_path)
