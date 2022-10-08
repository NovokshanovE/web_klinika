import time
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from email_send import send_massege

WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)


driver.implicitly_wait(20)


# ----------------------------------------------------------------------------------------------------------
def selection_specialty(a):
    specialty_necessary = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH, f'*//h3[contains(text(), "{a}")]')))
    specialty_necessary.click()
    driver.switch_to.frame(driver.find_element_by_xpath('.//iframe'))

    time.sleep(2)
    next_page_doctor_choice = driver.find_element_by_tag_name("button")
    next_page_doctor_choice.click()



# ----------------------------------------------------------------------------------------------------------
def choice_doctor(doctor_name):

    doctor_dropdown_menu = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH, './/span[@data-hook="dropdown-select-label"]'
    )))
    doctor_dropdown_menu.click()
    doctor_necessary = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH, f'.//li[contains(text(), "{doctor_name}")]'
    )))
    doctor_necessary.click()





# ----------------------------------------------------------------------------------------------------------
def choice_time(time_start, time_finish):
    try:
        elements_of_time = driver.find_elements_by_xpath('.//div//span[@class="ng-binding" and not(@data-hook)]')
    except:
        return 0

    if len(elements_of_time) > 0:
        for element_of_time in elements_of_time:
            if time_start <= element_of_time.text <= time_finish:
                element_of_time.click()
                return element_of_time
        return 0
    else:
        return 0


# ----------------------------------------------------------------------------------------------------------
def choice_data(data_start, data_finish, time_start, time_finish):
    data_today = str(datetime.date.today())
    elem_data = [data_today]
    time = 0
    if data_start > data_finish:
        data_start, data_finish = data_finish, data_start
    if time_start > time_finish:
        time_start, time_finish = time_finish, time_start
    while  elem_data[-1] <= data_finish:
        elem_data = driver.find_elements_by_xpath('.//td//td[@data-date]')

        for i in range(len(elem_data)):
            elem_data[i] =  elem_data[i].get_attribute('data-date')
        elem_data = sorted(list(set(elem_data)))

        for data in  elem_data:
            if data_start <= data <= data_finish:
                data_possible = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
                    By.XPATH, f'*//td[@data-date="{data}"]'
                )))
                data_possible.click()

                time = choice_time(time_start, time_finish)
                if time:
                    break
                show_month = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
                    By.XPATH, f'.//div[contains(text(), "Показать месяц")]'
                )))
                show_month.click()
        else:
            driver.find_element_by_xpath('*//button [@aria-label = "next month"]').click()

        if time:
            break
    return data, time.text


# ----------------------------------------------------------------------------------------------------------
def go_to_registration():
    page_reistration = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((
        By.XPATH,
        '/html/body/main/div/bks-app/div/div[1]/boost-calendar-page/div[2]/boost-visitor-sidebar/section/div[1]/div/button/boost-next-step-label/span'
    )))
    page_reistration.click()


# ----------------------------------------------------------------------------------------------------------
def enter_user_data(user, email, phone_number):
    fields = driver.find_elements_by_tag_name('input')

    fields[0].send_keys(user)
    fields[1].send_keys(email)
    fields[2].send_keys(phone_number)

    completion_registration = driver.find_element_by_xpath('.//div[@class="sidebar"]//span[@data-hook="next-step-label"]')
    completion_registration.click()


# ----------------------------------------------------------------------------------------------------------

def write_to_doctor(user, email, phone_number, direction, doctor, data_start, data_finish, time_start, time_finish):
    while True:
        try:
            driver.get('https://zhenyanovokshanov1.wixsite.com/klinika/blank-5')
        except:
            print('Ошибка: не удалось перейти на сайт.')
        try:
            selection_specialty(direction)
        except:
            print('Ошибка: не удалось найти направление')
        try:
            choice_doctor(doctor)
        except:
            print('Ошибка: не удалось найти доктора')
        try:
            data_send, time_send = choice_data(data_start, data_finish, time_start, time_finish)
            go_to_registration()
        except:
            print('Ошибка: не удалось найти подходящее время. Проявите терпение, Вы в очереди!')
        try:
            enter_user_data(user, email, phone_number)

        except:

            print('Ошибка: похоже, что вы преодолели все препятствия, но не одолели последнего босса')
        else:
            print("Регистрация прошла успешно!")
            send_massege(email, time_send, data_send, user, doctor)
            break
        time.sleep(10)
    # driver.quit()
