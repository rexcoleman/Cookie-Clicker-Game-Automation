import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdb




chrome_driver_path = "/Users/rexcoleman/Development/Drivers/chromedriver_mac64"
driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/experiments/cookie/")

#Get cookie to click on cookie.
cookie = driver.find_element(by=By.ID, value="cookie")
cookie.click()

#Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]
print(item_ids)

timeout = time.time() + 5
five_min = time.time() + 60*5

while True:
    cookie.click()

    # Every 5 seconds:
    if time.time() > timeout:

        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            print(element_text)
            if price.text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        print(item_prices)

        # Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]
        print(cookie_upgrades)
        print(cookie_upgrades.items())
        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id
        print(affordable_upgrades)

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        print(to_purchase_id)

        item_to_purchase = driver.find_element(By.ID,to_purchase_id)
        item_to_purchase.click()

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

        # After 5 minutes stop the bot and check the cookies per second count.
        if time.time() > five_min:
            cookie_per_s = driver.find_element_by_id("cps").text
            print(cookie_per_s)
            break


pdb.set_trace()

