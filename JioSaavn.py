from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

driver = webdriver.Chrome()

driver.maximize_window()

try:
    driver.get("https://www.jiosaavn.com/artist/s.-p.-balasubrahmanyam-songs/Ix5AC5h7LSg_")
    
    load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/main/section[1]/p/button"))
            )
    language_dropdown = driver.find_element(By.ID, "header_language_menu")
    language_dropdown.click()
    time.sleep(1)

    all_language_items = driver.find_elements(By.CSS_SELECTOR, ".o-list-select__item")
    for item in all_language_items:
        if not "selected" in item.get_attribute("class"):
            item.click()

    update_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Update')]")
    update_button.click()
    time.sleep(2)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        try:
            load_more_button = driver.find_element(By.XPATH, "//p[@class='u-align-center']/button[contains(text(), 'Load more')]")

            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//p[@class='u-align-center']/button[contains(text(), 'Load more')]")))

            try:
                player = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.ID, "player"))
                )
                if player.is_displayed():
                    driver.execute_script("arguments[0].style.display='none';", player)
                    time.sleep(1)
            except:
                pass

            load_more_button.click()
            time.sleep(2)
        except Exception as e:
            print("Load more button not found or not clickable, scrolling...")
        
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)  

        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height 

    song_elements = driver.find_elements(By.XPATH, "//a[@class='u-color-js-gray' and @href]")
    song_links = [element.get_attribute("href") for element in song_elements]
    song_links = song_links[:-2]
    
    aditya_music_count = 0

    for song_link in song_links:
        driver.get(song_link)
        time.sleep(2)

        try:
            copyright_info_element = driver.find_element(By.XPATH, "//p[contains(@class, 'u-color-js-gray u-ellipsis@lg u-visible@lg')]")
            copyright_info = copyright_info_element.text

            if re.search(r'aditya music', copyright_info, re.IGNORECASE):
                aditya_music_count += 1
        except Exception as e:
            print(f"Could not find copyright info for {song_link}: {e}")

finally:
    driver.quit()

print(aditya_music_count)