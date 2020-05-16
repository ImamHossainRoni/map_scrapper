from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import re, os
import requests

#cities = pd.read_csv("zip_code_database.csv",encoding="ISO-8859-1")
#cities = cities.drop({"Borough","Neighborhood"},1)
#ch = po[0].append([po[1],po[2],po[3],po[4],po[5],po[6],po[7],po[8]]).reset_index(drop=True)

places = ["WATER DAMAGE RESTORATION in "]

def run(city, country, keyword):
    global cities, places
    # start = int(input("Start Value :: "))
    # end = int(input("End Value :: "))
    # file_cities = input("Enter Cities/zipcode name file:: ")
    # file_keywords = input("Enter keywords name file:: ")
    # name_country = input("Enter country name:: ")
    #
    # cities = pd.read_csv(file_cities+".csv",encoding="utf8")
    # places = pd.read_csv(file_keywords+".csv",encoding="utf8")
    # places_data = places['keywords']
    city = city
    place = keyword
    name_country = country



    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3')
    chrome_options.add_argument("--headless")

    # for place in places_data[start:end]:
    #    for city in cities['Cities']:
    print(city)
    print(place)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://www.google.com/maps")
    driver.find_element_by_id("searchboxinput").clear()
    driver.find_element_by_id("searchboxinput").send_keys(str(place)+" " +str(city)+ " " + name_country)
    driver.find_element_by_id("searchbox-searchbutton").click()
    element_aval(driver,"section-result")
    results_scrape(driver,place,city)
    driver.quit()

row = 0
def results_scrape(driver,place,city):
    global row
    data = []
    while True:
        element_aval(driver,"section-result")
        elements = len(driver.find_elements_by_class_name('section-result'))
        for shop in range(elements):
            print(str(row)+" "+str(place)+" "+str(city))
            row += 1
            att_dict = {}
            element_aval(driver,"section-result")
            try:
                element = driver.find_elements_by_class_name("section-result")[shop]
                is_ad = element.get_attribute("data-result-ad-type")
                if is_ad:
                    pass
                else:
                    try:
                        element_click(element)
                        element_aval(driver,"section-hero-header-title-description")
                        att_dict['name'] = driver.find_element_by_class_name("section-hero-header-title-description").find_element_by_tag_name("h1").text if element_find(driver,"section-hero-header-title-description") else ""
                        att_dict['claimed_status'] = driver.find_element_by_xpath('//*[@data-section-id="mcta"]').text if element_xpath(driver,'//*[@data-section-id="mcta"]') else ""
                        att_dict['rating'] = driver.find_element_by_class_name("section-star-display").text if element_find(driver,"section-star-display") else ""
                        att_dict['category'] = driver.find_element_by_xpath('//*[@jsaction="pane.rating.category"]').text if element_xpath(driver,'//*[@jsaction="pane.rating.category"]') else ""
                        att_dict['reivews'] = str(driver.find_element_by_class_name('widget-pane-link').text)[1:-1] if element_find(driver, "widget-pane-link") else ""
                        att_dict['address'] = driver.find_element_by_xpath('//*[@data-section-id="ad"]').text if element_xpath(driver,'//*[@data-section-id="ad"]') else ""
                        att_dict['street_address'] = driver.find_element_by_xpath('//*[@data-section-id="ol"]').text if element_xpath(driver,'//*[@data-section-id="ol"]') else ""
                        att_dict['phone_no'] = driver.find_element_by_xpath('//*[@data-section-id="pn0"]').text if element_xpath(driver,'//*[@data-section-id="pn0"]') else ""
                        att_dict['website'] = driver.find_element_by_xpath('//*[@data-section-id="ap"]').text if element_xpath(driver,'//*[@data-section-id="ap"]') else ""
                        if(att_dict['website'] != ""):
                            att_dict['email'] = find_mail("http://"+att_dict['website'])
                        att_dict['timing'] = driver.find_element_by_class_name("section-info-hour-text").find_elements_by_tag_name("span")[1].text if element_find(driver,"section-info-hour-text") else ""
                        att_dict['image_link'] = driver.find_element_by_xpath('//*[@jsaction="pane.heroHeaderImage.click"]').find_element_by_tag_name('img').get_attribute("src") if element_xpath(driver,'//*[@jsaction="pane.heroHeaderImage.click"]') else ""
                        att_dict['longitude'], att_dict['latitude'] = str(re.search('!3d(.*)',driver.current_url).group(1)).split('!4d')
                        att_dict['URL'] = driver.current_url
                        att_dict['search_key'] = str(city)+" "+str(place) + " USA"
                        att_dict['price'] = driver.find_element_by_class_name('bRqcEmw6ZsI__price-row').find_element_by_tag_name('span').text if element_find(driver,'bRqcEmw6ZsI__price-row') else ""
                        data.append(att_dict)
                        driver.find_element_by_xpath('//*[@jsaction="pane.place.backToList"]').click()
                    except Exception:
                        save_to_excel(data,place)
                        data = []
                        driver.find_element_by_xpath('//*[@jsaction="pane.place.backToList"]').click()
                        pass

            except Exception:
                no_net()
                pass

        try:
            save_to_excel(data,place)
            data = []
            element_aval(driver,"section-result")
            driver.find_element_by_id("n7lv7yjyC35__section-pagination-button-next").click()
            next_page(driver)
            sleep(1)
        except Exception:
            no_net()
            break



def next_page(driver):
    sleep(1)
    while True:
        try:
            if driver.find_element_by_xpath('//*[@jsan="t-lAj0-0Yc4q0,7.section-refresh-overlay,7.noprint,5.top"]'):
                break
        except Exception:
            pass



def element_find(driver,class_name):
    try:
        if driver.find_element_by_class_name(class_name):
            return True
        else:
            return False
    except Exception:
        return False

def element_xpath(driver,xpath):
    try:
        if driver.find_element_by_xpath(xpath):
            return True
        else:
            return False
    except Exception:
        return False

def element_aval(driver,class_name):
    iter = 0
    while True:
        try:
            iter += 1
            if iter >= 1000:
                break
            if driver.find_element_by_class_name(class_name):
                break

        except Exception:
            pass

def element_click(driver):
    iter = 0
    while True:
        try:
            iter += 1
            if iter >= 1000:
                break
            driver.click()
            break

        except Exception:
            pass


def save_to_excel(data,place):
    df = pd.DataFrame(data)
    file_name = "Scrapped_data_"+"japan"+".csv"
    file_name = file_name.replace("*","")
    if os.path.exists(file_name):
    	df.to_csv(file_name,index=False,mode = 'a',header=False, encoding="utf8")
    else:
    	df.to_csv(file_name,index=False, encoding="utf8")

def no_net():
    print("might be no Internet")
    while  True:
        try:
            if requests.get("https://www.google.com/"):
                print("interent available")
                break
        except Exception:
            pass

def find_mail(url):
             try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

                source_code = requests.get(url, headers=headers, timeout=(10))
                curr = source_code.url

                original_curr = curr
                plain_text = source_code.text
                if '@' in plain_text:
                    match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
                else:
                    match = ""
                # Get from Contact Page
                if not match:
                    urls = [original_curr + '/contact/', original_curr + '/Contact/']
                    for cu in urls:
                        curr = cu
                        source_code = requests.get(url, headers=headers, timeout=(10))
                        plain_text = source_code.text
                        if '@' in plain_text:
                            match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
                            if match:
                                break
                        else:
                            match = ""
                    # Get from the url
                    if not match:

                        match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', original_curr)
                        # Load JavaScript of Page
                        if not match:
                            options = Options()
                            options.add_argument('--headless')
                            driver = webdriver.Chrome(options=options)
                            driver.get(original_curr)
                            plain_text = driver.page_source
                            if '@' in plain_text:
                                match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
                            else:
                                match = ""
                            if not match:
                                urls = [original_curr + '/contact/', original_curr + '/Contact/']
                                for cu in urls:
                                    driver.get(cu)
                                    plain_text = driver.page_source
                                    if '@' in plain_text:
                                        match = re.findall(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', plain_text)
                                        if match:
                                            break
                                    else:
                                        match = ""

                                driver.close()
                            else:
                                driver.close()

                match = list(set(match))
                email = ', '.join(match)
                if not email:
                    print ("no mail")
                else:
                    return email

             except:
                print("")
             return ""

