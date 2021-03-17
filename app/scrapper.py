from lxml import html
import requests
from app.restaurant import *
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
    
    # Wait until all elements are present in the list of restaurants.
    list_of_restaurants = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="main-content"]/div/div/div[2]/div/div[2]')
        )
    )
    list_of_restaurants = list_of_restaurants[0]
    
    # Use the fact that all restaurants have only one figure to find number of restaurants in the page.
    figures = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.TAG_NAME, 'figure'))
    )
    
    num_of_restaurants = len(figures)
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
        
        if RestaurantInfo.is_satisfied(item_info):
            restaurants.append(RestaurantInfo(item_info, link))
            
    return restaurants

def get_items(restaurants, selected_promotion):
    for res in restaurants:
        current_url = res.link
        r = requests.get(current_url)
        tree = html.fromstring(r.content)
        current_deal = tree.xpath('//*[@id="main-content"]/div[3]/ul/li[1]/h2/span/text()')
        if current_deal == []:
            res.promotion_items = {'None Found' : ' '}
            continue
        if current_deal[0] == selected_promotion:
            grid = tree.xpath('//*[@id="main-content"]/div[3]/ul/li[1]/ul')[0]
            list_of_items = grid.getchildren()
            for each_item in list_of_items:
                text = each_item.text_content()
                price_idx = text.find('$')
                item = text[:price_idx]
                price = text[price_idx:]
                res.promotion_items[item] = price
    return restaurants