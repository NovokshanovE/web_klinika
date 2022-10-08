from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
#driver = webdriver.Chrome(ChromeDriverManager().install())

driver.implicitly_wait(10)

#----------------------------------------------------------------------------------------------------------
def specialty_selection(a):
    #print(driver.find_elements_by_tag_name("h3"))
    way_elem = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH, f'*//h3[contains(text(), "{a}")]')))
    way_elem.click()
    driver.switch_to.frame(driver.find_element_by_xpath('.//iframe'))
    #print(driver.find_elements_by_tag_name("button"))
    driver.find_element_by_tag_name("button").click()
    #driver.switch_to.default_content()

#----------------------------------------------------------------------------------------------------------
def doctor_choice(target_name):
    #driver.switch_to.frame(driver.find_element_by_xpath('.//iframe'))
    dropdown_menu = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH, './/span[@data-hook="dropdown-select-label"]'
    )))
    dropdown_menu.click()
    target_elem = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH, f'.//li[contains(text(), "{target_name}")]'
    )))
    target_elem.click()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

# ----------------------------------------------------------------------------------------------------------
def time_choice(time_start, time_finish):
    try:
        elem = driver.find_elements_by_xpath('.//div//span[@class="ng-binding" and not(@data-hook)]')
    except:
        return 0
    print(elem)
    if len(elem) > 0:
        for i in elem:
            if time_start <= i.text <= time_finish:
                i.click()
                return 1
        return 0
    else:
        return 0

#----------------------------------------------------------------------------------------------------------
def data_choice(data_start, data_finish, time_start, time_finish):
    elem = driver.find_elements_by_xpath('.//td//td[@data-date]')
    #print(elem[0].get_attribute('data-date'))

    for i in range(len(elem)):
        elem[i] = elem[i].get_attribute('data-date')
    elem = sorted(list(set(elem)))
    for i in elem:
        print(i)
        if data_start <= i <= data_finish:
            dropdown_menu = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
                By.XPATH,
                f'*//td[@data-date="{i}"]'
            )))
            dropdown_menu.click()

            if time_choice(time_start, time_finish):
                break
            target_elem = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
                By.XPATH, f'.//div[contains(text(), "Показать месяц")]'
            )))
            target_elem.click()

#----------------------------------------------------------------------------------------------------------
def go_to_registration():
    dropdown_menu = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH, '/html/body/main/div/bks-app/div/div[1]/boost-calendar-page/div[2]/boost-visitor-sidebar/section/div[1]/div/button/boost-next-step-label/span'
    )))
    dropdown_menu.click()

#----------------------------------------------------------------------------------------------------------
def reception_registration(user, email, phone_number):
    elem_2 = driver.find_elements_by_tag_name('input')
    
    elem_2[0].send_keys(user)
    elem_2[1].send_keys(email)
    elem_2[2].send_keys(phone_number)

    button = driver.find_element_by_xpath('.//div[@class="sidebar"]//span[@data-hook="next-step-label"]')
    button.click()
#----------------------------------------------------------------------------------------------------------

def take_zapis(user, email, phone_number,direction, doctor, data_start, data_finish, time_start, time_finish):
    while True:
        try:
            driver.get('https://zhenyanovokshanov1.wixsite.com/klinika/blank-5')
            specialty_selection(direction)
            doctor_choice(doctor)
            data_choice(data_start, data_finish, time_start, time_finish)

            go_to_registration()
            reception_registration(user, email, phone_number)

        except:
            print('Время занято')
        else:
            print("OK")
            break
        time.sleep(10)
    #driver.quit()

