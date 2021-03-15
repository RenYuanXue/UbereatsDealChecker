from flask import Flask, render_template, request, url_for, redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.maximize_window()
    driver.get('https://www.ubereats.com')
    driver.quit()
    return render_template('result.html')

if __name__ == '__main__':
    app.run()