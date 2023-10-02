# Здесь будет код веб-приложения
# -*- coding: utf-8 -*-
""" Программа использует flask и запускает веб-сервер. 
При запросе к этому серверу он возвращает текст "Привет, Мир!" """
from flask import Flask, request, render_template, redirect, url_for, session
from random import shuffle, randint
from db_scripts import *
import os

def make_databases():
    main()

def quiz_form():
    q_list = get_quizes()
    return render_template('start.html', q_list=q_list)#<option value="nothing"></option>

def index():
    """ Функция возвращает текст документа """
    if request.method == 'GET':
        session["quiz_id"] = -1
        return quiz_form()
    if request.method == 'POST':
        session['quiz_id'] = request.form.get("quiz")
        session['total'] = 0
        session['correct'] = 0
        return redirect(url_for('test'))

#ВСЕ ЧТО СВЯЗАНО СО СТРАНИЦЕЙ test
def test_page(full_question):
    quiz_content_id, question, *answers = full_question[0]
    topic_name = get_quiz_name(session['quiz_id'])
    shuffle(answers)
    return render_template("test.html", quiz_content_id=quiz_content_id, question=question, answers=answers, topic_name=topic_name.lower())

def check_answer(true_answer):
    answer = request.form.get('answer')
    session['total'] += 1 
    if answer == true_answer:
        session['correct'] += 1

cnt = 0 #задаёт id вопроса
correct_answer = ""#запоминает правильный ответ в каждом новом вопросе
def test():
    global cnt, correct_answer
    if "quiz_id" not in session or session["quiz_id"] == -1:
        return redirect(url_for('index'))
    if request.method == "POST":
        check_answer(correct_answer)
    try:
        next_question = get_question_after(cnt, session['quiz_id'])
        correct_answer = next_question[0][2]
        cnt = next_question[0][0]
        return test_page(next_question)
    except:
        return redirect(url_for('result'))
        


def result():
    return render_template("result.html", total=session['total'], correct=session['correct'])


# Создаём объект веб-приложения:
folder = os.getcwd()
app = Flask(__name__, static_folder="folder", template_folder=folder)
app.config['JSON_AS_ASCII'] = False   # параметр - имя модуля для веб-приложения
                        # значение __name__ содержит корректное имя модуля для текущего файла 
                        # в нём будет значение "__main__", если модуль запускается непосредственно
                        # и другое имя, если модуль подключается
app.add_url_rule('/', 'index', index, methods = ['POST', 'GET'])
app.add_url_rule('/test', 'test', test, methods = ['POST', 'GET'])
app.add_url_rule('/result', 'result', result)   # создаёт правило для URL: 
                                        # при получении GET-запроса на адрес '/' на этом сайте
                                        # будет запускаться функция index (указана третьим параметром)
                                        # и её значение будет ответом на запрос.
                                        # Второй параметр - endpoint, "конечная точка", -
                                        # это строка, которая содержит имя данного правила. 
                                        # Обычно endpoint рекомендуют делать идентичным имени функции, 
                                        # но в сложных приложениях может быть несколько функций с одним именем в разных модулях, 
                                        # и для различения их в пределах всего сайта можно указывать разные endpoint.

app.config["SECRET_KEY"] = 'DontTellAboutThisKey'

if __name__ == "__main__":
    make_databases()
    # Запускаем веб-сервер:
    app.run()