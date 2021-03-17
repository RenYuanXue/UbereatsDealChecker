import os
from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from common.restaurant import *
from common.scrapper import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods = ['Get', 'POST'])
def homeRedirect():
    input_address = request.form['Address']
    selected_category = request.form['Category']
    selected_promotion = request.form['Promotion']
    return redirect(url_for('result', 
                            input_address = input_address, 
                            selected_category = selected_category, 
                            selected_promotion = selected_promotion))

@app.route('/result/<input_address>/<selected_category>/<selected_promotion>')
def result(input_address, selected_category, selected_promotion):
    try:

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    

        driver.maximize_window()
        driver.get('https://www.ubereats.com')

        listed_restaurants = get_all_restaurants(driver, input_address, 
                                                 selected_category, selected_promotion)
    except:
         redirect(url_for('home'))
    finally:
        driver.quit()

    listed_restaurants = listed_restaurants[:10]
    listed_restaurants = get_items(listed_restaurants, selected_promotion)

    return render_template('result.html', listed_restaurants = listed_restaurants)

if __name__ == '__main__':
    app.run(debug = True)