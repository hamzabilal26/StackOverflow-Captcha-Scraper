from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import openpyxl
from lxml import html
from solveRecaptcha import solveRecaptcha
import requests




#Inputs Here......
#pages are 7 for tag1 and 9 for tag 2

tag1 = "https://stackoverflow.com/search?q=%5Bpuppet%5D+ssl"
tag2 = "https://stackoverflow.com/search?q=%5Bansible%5D+ssl"
filename = "Test"
total_pages = 9

wb = openpyxl.Workbook()
ws = wb.active
ws.append(['Question Url', 'Title', 'Question', 'Answer 1', 'Answer 2', 'Answer 3', 'Meta Link 1', 'Meta Link 2',
           'Meta Link 3', 'Meta Link 4'])


options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument('--lang=en_US')

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

# change tag1 or tag2 here....
url = tag2
driver.get(url)



def captcha_fun():
    result = solveRecaptcha(
        "6Lfmm70ZAAAAADvPzM6OhZ8Adi40-78E-aYfc1ZS",
        url
    )

    code = result['code']

    print(code)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'g-recaptcha-response'))
    )

    driver.execute_script(
        "document.getElementById('g-recaptcha-response').innerHTML = " + "'" + code + "'")

    driver.execute_script("___grecaptcha_cfg.clients['0']['W']['W']['callback']('%s')" % code)

# Scraping Starts Here.............

def scraper():


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@title='Show 50 items per page']"))
    )

    btn50 = driver.find_element(By.XPATH, "//a[@title='Show 50 items per page']").click()

    driver.implicitly_wait(3000)


    i = 1
    total_urls = []
    while i < total_pages:
        links = driver.find_elements(By.XPATH, "//h3[@class='s-post-summary--content-title']/a")
        for each in links:
            url = each.get_attribute("href")
            total_urls.append(url)
        # total_urls.append(links)
        driver.implicitly_wait(3000)

        driver.find_element(By.XPATH, "//a[@rel='next']").click()
        i += 1

    links = driver.find_elements(By.XPATH, "//h3[@class='s-post-summary--content-title']/a")
    for each in links:
        url = each.get_attribute("href")
        total_urls.append(url)

    print(len(total_urls))



    for each_url in total_urls:
        print(each_url)
        response = requests.get(each_url)
        print(response.status_code)
        data = html.fromstring(response.content)
        try:
            title = data.xpath("//h1/a[@class='question-hyperlink']/text()")[0]
            print(title)
        except Exception as e:
            print("Error getting the page....")
            title = 'Not Found'

        try:
            question_p = data.xpath("//div[@class='postcell post-layout--right']/div[@class='s-prose js-post-body']/p/text()")
            # print(question_p)
            question = ''.join(question_p)
            print(question)

        except Exception as e:
            print("Question detail not found")
            question = 'Question Details not found'

        answer_list = []
        try:
            answer_p = data.xpath("//div[@class='answercell post-layout--right']/div[@class='s-prose js-post-body']")
            for each in answer_p:
                ans = each.xpath("./p//text()")
                ans1 = ','.join(ans)
                # print(ans1)
                answer_list.append(ans1)
        except Exception as e:
            print("Answer not found")

        try:
            answer_1 = answer_list[0]
        except:
            answer_1 = "Answer not found"
        try:
            answer_2 = answer_list[1]
        except:
            answer_2 = "Answer 2 not found"
        try:
            answer_3 = answer_list[2]
        except:
            answer_3 = "Answer 3 not found"

        print(answer_1)
        print(answer_2)
        print(answer_3)

        links_list = []
        try:
            links_p = data.xpath("//div[@class='answercell post-layout--right']/div[@class='s-prose js-post-body']")


            for each in links_p:
                ans = each.xpath("./p//a/@href")
                link = ','.join(ans)
                # print(ans1)
                links_list.append(link)
        except Exception as e:
            print("Links not found")

        try:
            link1 = links_list[0]
        except:
            link1 = "No link found"

        try:
            link2 = links_list[1]
        except:
            link2 = "No link found"

        try:
            link3 = links_list[2]
        except:
            link3 = "No link found"

        try:
            link4 = links_list[3]
        except:
            link4 = "No link found"

        print(link1)
        print(link2)
        print(link3)
        print(link4)

        this_row = [each_url, title, question, answer_1, answer_2, answer_3, link1, link2, link3, link4]
        ws.append(this_row)

    time.sleep(20)
    wb.save(f"{filename}.xlsx")

if __name__ == '__main__':
    try:
        captcha = driver.find_element(By.XPATH, "//textarea[@id='g-recaptcha-response']")
        captcha_fun()
        scraper()
    except:
        scraper()

