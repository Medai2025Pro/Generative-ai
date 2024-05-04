from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def search_google_web_automation(query, num_results=3):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    url = f"http://www.google.com/search?q={query}"
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "yuRUbf"))
        )
    except:
        print("Timeout or Element not found")
        driver.quit()
        return []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    search = soup.find_all("div", class_="yuRUbf")

    results = []
    for index, h in enumerate(search[:num_results]):
        title = h.a.h3.text
        link = h.a.get("href")
        domain = urlparse(link).netloc
        results.append(
            {
                "title": title,
                "url": link,
                "domain": domain,
                "rank": index + 1,
            }
        )

    driver.quit()
    return results



