from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

import time
import datetime
import re

def get_month_number(month_name):
    month_mapping = {
        "Januar": "01",
        "Februar": "02",
        "März": "03",
        "April": "04",
        "Mai": "05",
        "Juni": "06",
        "Juli": "07",
        "August": "08",
        "September": "09",
        "Oktober": "10",
        "November": "11",
        "Dezember": "12"
    }

    return month_mapping.get(month_name, "Invalid Month")

def format_time(time_str):
    # Extract the first date from the time string
    year = time_str.split(' ')[-1]

    first_date_array = time_str.split('-')[0].split(' ')

    # Check if the first date has a comma, thats the common pattern for signle day events
    if '-' in time_str:
        #month is in second to last and day folloed by dot is in third to last
        month_name = first_date_array[-2]
        month_number = get_month_number(month_name)
        day = first_date_array[-3][:-1]
    else:
        #month is in second to last and day folloed by dot is in third to last
        month_name = first_date_array[-2]
        month_number = get_month_number(month_name)
        day = first_date_array[-3][:-1]

    # Format the parsed time as "YYYYMMDD"
    formatted_time = f'{year}{month_number}{day}'

    return formatted_time

def format_title(title_text):
    # Use regular expression to remove leading number and associated chars
    formatted_title = re.sub(r'^\d+[:.\s-]*', '', title_text)
    return formatted_title.strip()


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'")
    driver = webdriver.Chrome(options=options)

    subdomain = "runme"
    base_url = "https://www.runme.de"

    url = f'{base_url}/laufkalender/deutschland/'
    default_race_type = "road"

    option_order = ["trailrun"]

    #race_collection = RaceCollection()

    driver.get(url)
    
    # Wait for the cookie agreement button and click it if it appears within 3 seconds
    try:
        cookie_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-primary.btn-order.accept-agreement"))
        )
        cookie_button.click()
        print("Clicked cookie agreement button")
    except:
        print("Cookie agreement button not found or clickable")

    # Wait for the consent button and click it if it appears within 3 seconds
    try:
        consent_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button"))
        )
        consent_button.click()
        print("Clicked consent button")
    except:
        print("Consent button not found or clickable")

    data_directory = {}
    # Wait for the event headers to appear
    for option in option_order:
        print(f"Checking for {option}")
        if option == "trailrun" or option == "mountainrun":
            url = f'{base_url}/tags/{option}/'
            driver.get(url)
            # Find the parent element with id "filter_dropdowns"
            parent_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'filter_dropdowns')))
            
            # Find the third child of the parent element (using 0-based indexing)
            third_child = parent_element.find_elements(By.TAG_NAME, "div")[2]
            third_child.click()

            # Find the input third child element
            input_element = third_child.find_element(By.TAG_NAME, "input")

            # Find the ul element and the second li element that corresponds to DE
            ul = third_child.find_element(By.TAG_NAME, "ul")
            li_de = ul.find_elements(By.TAG_NAME, "li")[1]
            a = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(li_de.find_element(By.TAG_NAME, "a"))
            )
            a.click()

            # Set the value of the input element to "DE"
            #driver.execute_script("arguments[0].value = 'DE';", input_element)

            # Verify that the input value has been updated to "DE"
            input_value = input_element.get_attribute('value')
            if input_value == 'DE':
                print("Input value successfully changed to 'DE'")
            else:
                print("Input value did not change to 'DE'")
                exit()

            # Find and click the button with class "btn btn-primary btn-block filter_search"
            search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-primary.btn-block.filter_search')))
            search_button.click()

            #scroll_distance=500
            #for i in range(10):
            #    driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            #    time.sleep(1)
            
        else:
            url = f'{base_url}/laufkalender/deutschland/'
            driver.get(url)
            # Find the parent element with id "filter_dropdowns"
            parent_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'filter_dropdowns')))

            # Find the third child of the parent element (using 0-based indexing)
            third_child = parent_element.find_elements(By.TAG_NAME, "div")[2]
            third_child.click()

            # Find the ul element and the second li element that corresponds to Laufen
            ul = third_child.find_element(By.TAG_NAME, "ul")
            li_laufen = ul.find_elements(By.TAG_NAME, "li")[1]
            a = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(li_laufen.find_element(By.TAG_NAME, "a"))
            )
            a.click()

            # Find the third child of the parent element (using 0-based indexing)
            second_child = parent_element.find_elements(By.TAG_NAME, "div")[1]
            second_child.click()

            # Find the input third child element
            input_element = second_child.find_element(By.TAG_NAME, "input")

            # Find the ul element and the second li element that corresponds to Laufen
            ul = second_child.find_element(By.TAG_NAME, "ul")
            options_mapping = {
                "r_5": 2,
                "r_10s": 3,
                "r_21s": 8,
                "r_42s": 13,
                "r_42": 14,
                "r_42p": 18
            }
            #get corresponding option from drop down
            li_laufen = ul.find_elements(By.TAG_NAME, "li")[options_mapping[option]]
            a = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(li_laufen.find_element(By.TAG_NAME, "a"))
            )
            a.click()

            # Verify that the input value has been updated to "DE"
            input_value = input_element.get_attribute('value')
            if input_value == option:
                print(f"Input value successfully changed to {option}")
            else:
                print(f"Input value did not changed to {option}")
                exit()
            # Find and click the button with class "btn btn-primary btn-block filter_search"
            search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-primary.btn-block.filter_search')))
            search_button.click()

        try:
            time.sleep(2)
            event_headers = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "event-header.regular"))
            )

            for header in event_headers:
                try:
                    time_element = header.find_element(By.CSS_SELECTOR, ':first-child')
                    proper_date = format_time(time_element.text)

                    if not proper_date.isdigit() or len(proper_date) != 8:
                        print("Proper date is not in the format yyyymmdd")
                        continue
                except Exception as e:
                    print("No time element found")
                    continue
                
                try:
                    title_element = header.find_element(By.CLASS_NAME, "event-header__title")
                    name = format_title(title_element.text)
                    print("Title:", name)
                except Exception as e:
                    print("No title element found")
                    continue

                # Find and print href attributes of child anchor elements
                try:
                    anchor_elements = title_element.find_elements(By.TAG_NAME, "a")
                    for anchor in anchor_elements:
                        href = anchor.get_attribute("href")
                        print("Anchor Href:", href)
                except Exception as e:
                    print("No anchor elements found")

                # Find and print inner text of li elements under the nav with class event-header__competitions
                competitions_nav = None
                try:
                    competitions_nav = header.find_element(By.CLASS_NAME, "event-header__competitions")
                except Exception as e:
                    print("No competitions_nav element found")
                print("Competitions Nav:", competitions_nav)
                distances = []
                distance_str = ""
                try:
                    if competitions_nav:
                        li_elements = competitions_nav.find_elements(By.TAG_NAME, "li")
                        distances = []
                        distance_str = ""
                        for li in li_elements:
                            distance_item = li.text
                            # Convert the list to a comma-separated string
                            distance_str += f"{distance_item}, "
                            try:
                                if "KM" in distance_item or "km" in distance_item or "k" in distance_item or "K" in distance_item:
                                    # Split distance_item on " " to separate potential number and distance unit
                                    parts = distance_item.split()
                                    #checks if first part is a number, if not it will run remaining checks
                                    if parts[0].isdigit():
                                        distances.append(int(parts[0])*1000)
                                        break
                                    for i in range(len(parts)):
                                        part = parts[i]
                                        if "," in part or "." in part:
                                            distance_item = distance_item.split(",")[0] #get first digit if fraction
                                            distances.append(int(distance_item)*1000)
                                            break #should not break here, this will cause the loop to only run once when it finds decimals but it should run for all elements
                                        elif part[-1] in ['k', 'K', 'm', 'M']:
                                            # Extract the number and multiply it by 1000
                                            reduced_part = part[:-1].replace(",", "").replace(".", "").replace("km", "").replace("KM", "").replace("K", "").replace("k", "")
                                            reduced_parts = parts[i-1].replace(",", "").replace(".", "").replace("km", "").replace("KM", "").replace("K", "").replace("k", "")
                                            if reduced_part.isdigit():
                                                distances.append(int(float(reduced_part)*1000))
                                            elif reduced_parts.isdigit():
                                                distances.append(int(float(reduced_parts)*1000))
                                elif distance_item in ["Halvmaraton", "Half Marathon"]:
                                    distances.append(21097)
                                elif distance_item in ["Maraton", "Marathon"]:
                                    distances.append(42195)
                                elif "MILES" in distance_item:
                                    try:
                                        for match in re.findall(r"(\d+)\s*KM", distance_item):
                                            distances.append(int(match)*1609)
                                    except:
                                        pass
                                else:
                                    try:
                                        distances.append(int(distance_item)*1000)
                                    except:
                                        pass
                            except:
                                print(f"Error parsing distance {distance_item}")
                except Exception as e:
                    print("couldnt map distances, error: {e}")
                #mappig out backyard ultras
                if name.find("ackyard") != -1:
                    distances = "backyard"
                    race_type = "backyard"
                elif option == "trailrun" or option == "mountainrun":
                    race_type = "trail"
                else:
                    race_type = default_race_type
                distance_str = distance_str[:-2] #remove last comma and space
                print("Distance String:", distance_str)
                # Find place"
                place_element = None
                try:
                    place_element = header.find_element(By.CLASS_NAME, "distance-promo.f-16.pb-5")
                except Exception as e:
                    print("No competitions_nav element found")
                if place_element:
                    place = place_element.text.split("-")[0]
                    print("Distance Promo Text:", place)

                # Populate the data_directory with data_id and inner_text
                if distance_str != "" and name is not None:
                    key = f'{name}_{proper_date}'
                    if key not in data_directory:
                        data_directory[key] = {
                            "option": option,
                            "name": name,
                            "proper_date": proper_date,
                            "distance_str": distance_str,
                            "distances": distances,
                            "place": place,
                            "href": href,
                            "race_type": race_type
                        }      
            print("Finished crawling " + url)
            driver.save_screenshot("screenshot.png")
        except Exception as e:
            print("Error:", e)

    print(data_directory)
    


    # For each data_id, navigate to the detail page and check for the desired element
    for data_id in data_directory.keys():

        name = data_directory[data_id]["name"]

        print(f"---------------------Checking {name}---------------------")
        proper_date = data_directory[data_id]["proper_date"]
        race_type = data_directory[data_id]["race_type"]
        distance_str = data_directory[data_id]["distance_str"]
        distances = data_directory[data_id]["distances"]
        place = data_directory[data_id]["place"]
        detail_url = data_directory[data_id]["href"]
        driver.get(detail_url)

        # Check if the detail page contains an anchor with class "referer-link"
        website = ""
        website_ai_fallback = name
        referer_link = None
        try:
            referer_link = driver.find_element(By.CLASS_NAME, "referer-link")
        except Exception as e:
            print(f"No referer-link found for {name}")

        if referer_link:
            website_href = referer_link.get_attribute("href")
            website = website_href
            print(f"Website found for {name}: {website_href}")
        else:
            print(f"No website found for {name}")
        print("---------------------")


    # Close the browser
    driver.quit()    

if __name__ == "__main__":
    main()

