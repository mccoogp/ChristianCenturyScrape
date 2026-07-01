from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chrome_options = Options()
#chrome_options.add_argument("--user-data-dir=/Users/parkermccoog/selenium-profile")
chrome_options.add_argument("--user-data-dir=/Users/parkermccoog/Library/Application Support/Google/Chrome/Default")
from webdriver_manager.chrome import ChromeDriverManager
service = Service(ChromeDriverManager().install())
import undetected_chromedriver as uc

# Initialize the driver

#driver = webdriver.Chrome(service=service, options=chrome_options)
driver = uc.Chrome(version_main=149)



wait = WebDriverWait(driver, 15)
df = pd.read_csv("CenturyArts.csv")
newdf = pd.read_csv("FinalCenturyArts.csv")

first = True
for num in range(len(df)):
    start = time.time()
    if pd.isna(newdf.at[num, 'Article Text']):
        url = df["link"][num]
        driver.get(url)

        if first:
            time.sleep(30)
            first = False
        else:
            time.sleep(1)

        title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text

        try:
            div_element = driver.find_element(By.CLASS_NAME, "post-date")
            publish_date = div_element.text.split("on")[1] if "on" in div_element.text else div_element.text
        except Exception as e:
            print(f"Could not find date: {e}")
            publish_date = "Not_Found"

        article = driver.find_element(By.TAG_NAME, "main")
        paragraphs = article.find_elements(By.TAG_NAME, "p")
        text = "\n\n".join([p.text for p in paragraphs if p.text.strip()])

        issue = "Not Found"
        author = "Not Found"
        try:
            div_element = driver.find_element(By.CLASS_NAME, "cc-content-header.l-container--mid")
            for elem in div_element.find_elements(By.TAG_NAME, "a"):
                href = elem.get_attribute("href")
                if href:
                    if "/issue/" in href:
                        issue = href.split("/")[-1]
                    if "/contributor/" in href:
                        author = href.split("/")[-1]
                    if "/archives/" in href:
                        issue = elem.get_attribute("text")
                        publish_date = elem.get_attribute("text")
        except Exception as e:
            print(f"Could not find author, issue: {e}")

        newdf.at[num, 'Article Text'] = text
        newdf.at[num, 'Article Title'] = title
        newdf.at[num, 'Date'] = publish_date
        newdf.at[num, 'Issue'] = issue
        newdf.at[num, 'Author'] = author

        if num % 10 == 0:
            newdf.to_csv("FinalCenturyArts.csv", index=False)

        print(num, time.time() - start, title, publish_date)

newdf.to_csv("FinalCenturyArts.csv", index=False)
driver.quit()