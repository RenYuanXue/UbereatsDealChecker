from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def get_all_restaurants(driver, my_location, category = 'Deals', promotion = 'Buy 1, Get 1 Free'):
    '''
    None = get_to_page(driver, my_location, category = 'Deals')
    
    Perform a series of simulated clicks on website to get to desired Uber Eats page.
    
    @param driver: WebDriver
        WebDriver object from Selenium.
    @param my_location: str
        User location input on ubereats.com.
    @param category: str
        The category user want to check.
    '''
    # Wait 10 seconds maximum to locate the web elements.
    location_pos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="location-typeahead-home-input"]')
        )
    )
    find_food_pos = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/div[1]/div[2]/div/div[1]/button')
        )
    )
    
    # Perform series of actions to type my location in the text box
    # and redirect to the new page.
    actions = ActionChains(driver)
    actions.send_keys_to_element(location_pos, my_location)
    actions.pause(1)
    actions.click(find_food_pos)
    actions.perform()
    
    # If the category can be found in the pre_defined dictionary,
    # use the value in the dictionary as xpath.
    if category == 'Deals':
        nav_pos = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'nav'))
        )
        deals_pos = nav_pos.find_element_by_tag_name("li")
        deals_pos.click()
    else:
        search_pos = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'search-suggestions-typeahead-input'))
        )
        actions = ActionChains(driver)
        actions.send_keys_to_element(search_pos, category)
        actions.key_down(Keys.ENTER).key_up(Keys.ENTER)
        actions.perform()
    
    # Use the fact that all restaurants have only one figure to find number of restaurants in the page.
    figures = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.TAG_NAME, 'figure'))
    )
    
    num_of_restaurants = min(10, len(figures))
    restaurants = []
    
    for i in range(num_of_restaurants):
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//*[@id="main-content"]/div/div/div/div/div[2]/div[{0}]'.format(i + 1)
            ), ' ')
        )
        item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="main-content"]/div/div/div/div/div[2]/div[{0}]'.format(i + 1))
            )
        )
        item_info = item.text.split('\n')
        link_info = item.find_element_by_tag_name('a')
        link = link_info.get_attribute('href')
        
        if rewards(item_info[0], promotion):
            restaurant_info = {'name': item_info[1], 'deal': item_info[0], 'fee': find_delivery_fee(item_info), 
                               'time': find_delivery_time(item_info), 'promotion_items': {}, 'link': link}
            restaurants.append(restaurant_info)
            
    return restaurants


def get_items(driver, restaurants, selected_promotion):
    for res in restaurants:
        current_url = res['link']
        driver.get(current_url)
        try:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, '//*[@id="main-content"]/div[3]/ul/li[1]/h2/span'
                ), ' ')
            )
            deal_pos = driver.find_element_by_xpath('//*[@id="main-content"]/div[3]/ul/li[1]/h2/span')
            current_deal = deal_pos.text 
        except:
            res['promotion_items'] = {'Found None' : ""}
            continue
        
        if current_deal == selected_promotion:
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element(
                    (By.XPATH, '//*[@id="main-content"]/div[3]/ul/li[1]/ul'
                ), ' ')
            )
            grid = driver.find_element_by_xpath('//*[@id="main-content"]/div[3]/ul/li[1]/ul')
            list_of_items = grid.find_elements_by_tag_name('li')
            for each_item in list_of_items:
                text = each_item.text
                price_idx = text.find('$')
                item = text[:price_idx - 1]
                price = text[price_idx:]
                res['promotion_items'][item] = price

    return restaurants


def find_delivery_time(list_of_info):
    time = 'Not Found'
    for info in list_of_info:
        if "min" in info:
            time = info
    return time

def find_delivery_fee(list_of_info):
    fee = 'Not Found'
    for info in list_of_info:
        if "Delivery Fee" in info:
            fee = info
    return fee

def rewards(current_promotion, target_promotion):
    if current_promotion == target_promotion:
        return True
    else:
        return False