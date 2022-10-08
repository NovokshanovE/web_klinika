from flask import Flask, render_template, request
from Klinika_way import write_to_doctor
from threading import Thread


app = Flask(__name__)

directions = ['Офтальмолог', 'Дерматология', 'Лучевая диагностика', 'Женское здоровье',
                  'Ортопедия', 'Аптечная служба', 'Экстренная помощь', 'Внутренние болезни', 'Лечение ран',]
doctors_names = ['Иванов И.И.', 'Петров П.П.',]
# ...
@app.route('/login/', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')

        direction = request.form.get('direction')

        direction = directions[int(direction[-1]) - 1]
        # запрос к данным формы
        doctor = request.form.get('doctor')

        doctor = doctors_names[int(doctor[-1]) - 1]

        time1 = request.form.get('time1')
        time2 = request.form.get('time2')

        data1 = request.form.get('calendar1')
        data2 = request.form.get('calendar2')

        print(user, email, phone_number, direction, doctor, data1, data2, time1, time2)
        Thread(target=write_to_doctor, args=(user, email, phone_number, direction, doctor, data1, data2, time1, time2)).start()

    return render_template('login.html')


# ...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4567)