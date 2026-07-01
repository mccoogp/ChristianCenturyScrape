        
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd



chrome_options = Options()
chrome_options.add_argument("--user-data-dir=/Users/parkermccoog/selenium-profile")
chrome_options.add_argument("--headless=new")
service = Service()

print("Starting script", flush=True)
driver = webdriver.Chrome(service=service, options=chrome_options)


while True:
    df = pd.read_csv("Century/CenturyArts.csv")
    article_links = set()
    bad = []
    exit = False
    for i in range(int(len(df)/20), 1309):
        count = 0
        current = []
        url = f"https://www.christiancentury.org/articles?page={i}"
        print("Link:", url, len(df))
        driver.get(url)
        time.sleep(1)
        html_content = driver.page_source
        n = 0

        for num in range(20):
            if exit == True:
                break
            start = time.time()
            texttofind = "list-title"
            while html_content[n:n+len(texttofind)] != texttofind:
                n+=1
                if time.time() - start > 5:
                    exit = True
                    print("exit")
                    break
            if exit == True:
                break
            n+=len(texttofind)
            texttofind = "href="
            while html_content[n:n+len(texttofind)] != texttofind:
                n+=1
                if time.time() - start > 5:
                    exit = True
                    print("exit")
                    break
            if exit == True:
                break
            n+=len(texttofind)+1
            href = "https://www.christiancentury.org"
            while html_content[n] != ">":
                href += html_content[n]
                n +=1 
                if time.time() - start > 5:
                    exit = True
                    print("exit")
                    break
            if exit == True:
                break 
            href = href[:len(href)-1]  
            article_links.add((href))
            df.loc[len(df)] = {"link" : href, "Year": None, "Date": None, "Title": None, "Text": None}
            count += 1
            current.append('"' + href + '",')

        if exit == True:
            break
        if count != 20:
            bad.append((url, count))
            for n in current:
                print(n)
            print(bad)
        if i % 2 == 0:
            print("Loaded")
            df.to_csv('Century/CenturyArts.csv', index = False)


