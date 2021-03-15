import datetime
import random

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from requests_html import HTMLSession, AsyncHTMLSession
from selenium.webdriver.chrome.options import Options
import time

import send_sms
import config

ps5_url = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'

def get_page_session():
    session = HTMLSession()
    base_session = session.get(ps5_url)
    return base_session


def check_can_buy(base_session):
    buy_btn = base_session.html.find('button', containing='Add to Cart')
    if len(buy_btn) != 0:
        return True
    return False

def perform_purchase(ps5_url):
    driver = webdriver.Chrome()
    driver.get(ps5_url)
    driver.delete_all_cookies()
    driver.implicitly_wait(5)

    # add ps5 to cart
    btn = driver.find_elements_by_class_name("add-to-cart-button")
    if btn is not None:
        btn[0].click()
        print('Added to Cart')

    # go to cart
    driver.get('https://www.bestbuy.com/cart')

    # start checkout
    checkout_btn = driver.find_element_by_xpath('//button[text()="Checkout"]')
    if checkout_btn is not None:
        checkout_btn.click()
        print('Continue to Checkout')

    guest_button = driver.find_element_by_xpath('//button[text()="Continue as Guest"]')
    if guest_button is not None:
        guest_button.click()
        print('Continued to Checkout as Guest')

    # fill in shipping info
    driver.find_element_by_id('consolidatedAddresses.ui_address_2.firstName').send_keys(config.FIRST_NAME)
    driver.find_element_by_id('consolidatedAddresses.ui_address_2.lastName').send_keys(config.LAST_NAME)
    driver.find_element_by_id('consolidatedAddresses.ui_address_2.street').send_keys(config.ADDRESS)
    driver.find_element_by_id('consolidatedAddresses.ui_address_2.city').send_keys(config.CITY)
    driver.find_element_by_id('consolidatedAddresses.ui_address_2.zipcode').send_keys(config.ZIPCODE)
    driver.find_element_by_id('consolidatedAddresses.ui_address_2.state').send_keys(config.STATE)

    # fill in contact info i.e. email address and phone number
    driver.find_element_by_id('user.emailAddress').send_keys(config.EMAIL)
    driver.find_element_by_id('user.phone').send_keys(config.PHONE)

    # continue to payment info
    payment_btn = driver.find_elements_by_class_name('button--continue')
    if payment_btn is not None:
        payment_btn[0].click()
        print('continued to payment info')

    driver.find_element_by_id('optimized-cc-card-number').send_keys(config.CREDIT_CARD)
    purchase_btn = driver.find_elements_by_class_name('btn-primary')
    if purchase_btn is not None:
        purchase_btn[0].click()
        print('PURCHASED PS5')
        driver.save_screenshot(str(datetime.datetime.now()) + '-PS5-Order-Confirmation-Screenshot.png')
        time.sleep(10)
    else:
        print('Failed to Find Place Order Button')
    driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    purchased_ps5 = False
    while not purchased_ps5:
        session = get_page_session()

        if check_can_buy(session):
            send_sms.send_sms('The PS5 is instock and Bot is attempting to purchase.')
            try:
                perform_purchase(ps5_url)
                purchased_ps5 = True
            except selenium.common.exceptions.NoSuchElementException:
                print('An error occured while trying to purchase the PS5.'
                      'Visit this link:' + ps5_url)
                send_sms.send_sms('An error occured while trying to purchase the PS5.' +
                                  'Visit this link:' + ps5_url)
        else:
            print('Not for sale')
        time.sleep(0.1)

    if purchased_ps5:
        send_sms.send_sms('The PS5 was successfully purchased')
