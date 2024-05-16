import sqlite3
import csv
import telebot

bot = telebot.TeleBot('7057127739:AAGVR8az4AFZPd5F8jQ7Jt_ZTXW9zKu0vFs')
@bot.message_handler(content_types=['text'])
def get_find_family(message):
    bot.send_message(message.from_user.id,'Впишите фамилию искомого студента:')
    bot.register_next_step_handler(message, getout_Student)
def getout_Student(message):
    global family
    family = str(message.text)
    print(family)
    con = sqlite3.connect('botic.db')
    cur = con.cursor()
    with open('Groups.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['name']:
                cur.execute('insert into groups(grname) values (?)', (row['name'],))
    with open('Students.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['family'] and row['name'] and row['patronymic'] and row['birthday'] and row['idgroup']:
                cur.execute('insert into students(family, stname, patronymic, birthday, idgroup) values (?,?,?,?,?)',
                            (row['family'], row['name'], row['patronymic'], row['birthday'], row['idgroup']))
    try:
        cur.execute(
            '''select family, stname, patronymic, birthday, groups.grname from students inner join groups on students.idgroup = groups.id where family = ?''',
            (family,))
        records = cur.fetchall()
        print(records)

        for i in records:
            outInfo = 'Фамилия: ' + str(i[0]) + '\n' + 'Имя: ' + str(i[1]) + '\n' + 'Отчество: ' + str(i[2]) + '\n' + 'День рождения: ' + str(i[3]) + '\n' + 'Группа студента: ' + str(i[4])
        bot.send_message(message.from_user.id, outInfo)
    except:
        bot.send_message(message.from_user.id, 'Студент не найден')


bot.polling(none_stop=True)

