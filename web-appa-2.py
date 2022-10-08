from flask import Flask, render_template, request
from Klinika_way import take_zapis
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
app = Flask(__name__)

a = 'Офтальмолог'
target_name = 'Иванов И.И.'



#...
@app.route('/login/', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        
        user = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        
        direction = request.form.get('direction')  # запрос к данным формы
        doctor = request.form.get('doctor')
        
        time1 = request.form.get('time1')
        time2 = request.form.get('time2')
        
        data1 = request.form.get('calendar1')
        data2 = request.form.get('calendar2')
        '''
        user = 'kkk'
        email = 'aa@aa.ru'
        phone_number = '+7'
        direction = 'Офтальмолог'
        doctor = 'Иванов И.И.'
        data1 = '2020-02-12'
        data2 = '2020-02-15'
        time1 = '10:00'
        time2 = '17:00' 
        '''
        #print(user, email, phone_number, direction, doctor, data1, data2, time1, time2)
        Thread(target=take_zapis, args=(user, email, phone_number, direction, doctor, data1, data2, time1, time2)).start()

    return render_template('login.html')
#...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)