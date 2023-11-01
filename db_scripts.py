import sqlite3
from questions_quizes import *

db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor#, db_name
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' удаляет все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

# make db of all questions
def create_question(list_questions):
    open()
    question = """CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong_1 VARCHAR,
        wrong_2 VARCHAR,
        wrong_3 VARCHAR);"""
    do(question)

    cursor.executemany("""INSERT INTO question
    (question, answer, wrong_1, wrong_2, wrong_3)
    VALUES (?, ?, ?, ?, ?)""", list_questions)
    do(question)
    close()

#make db of all quizes
def create_quiz(quizes):
    open()
    quiz = """CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY,
        name VARCHAR);"""
    
    do(quiz)

    cursor.executemany("""INSERT INTO quiz
    (name)
    VALUES (?)""", quizes)
    do(quiz)
    close()


def create_content_quiz(quizes, list_questions):
    open()
    quiz_content = """CREATE TABLE IF NOT EXISTS quiz_content(
    id INTEGER PRIMARY KEY,
    quiz_id INTEGER,
    question_id INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz (id),
    FOREIGN KEY (question_id) REFERENCES question (id));"""
    
    do(quiz_content)

    query = """INSERT INTO quiz_content (quiz_id, question_id)
    VALUES (?, ?)"""
    id_memory = 0
    #МОЙ СПОСОБ СОЗДАНИЯ ДБ НЕ ИСПОЛЬЗУЯ КОНСОЛЬ
    for i in range(1, len(quizes) + 1):
        quiz_id = i
        for j in range(len(list_questions_QuizContent)):
            if len(list_questions_QuizContent[j]) == 2:
                a = list_questions_QuizContent.pop(j)
                del list_questions_QuizContent[0:j]
                break
            id_memory += 1
            question_id = id_memory
            cursor.execute(query, [quiz_id, question_id])            
            conn.commit()
    close()

    #CПОСОБ СОЗДАНИЯ ДБ С ПОМОЩЬЮ КОНСОЛИ
    # while input("Добавлять связь? y/n: ") != "n":
    #     quiz_id = int(input("id викторины: "))
    #     question = int(input("id вопроса: "))
    #     cursor.execute(query, [quiz_id, question])
    #     conn.commit()




#function that return next_question of choosen topic   
def get_question_after(question_id=0, quiz_id=1):
    open()
    cursor.execute("SELECT quiz_content.id, question.question, question.answer, question.wrong_1, question.wrong_2, question.wrong_3 FROM quiz_content, question WHERE quiz_content.question_id == question.id AND quiz_content.quiz_id == (?) AND quiz_content.id > (?) ORDER BY quiz_content.id", [quiz_id, question_id])
    result = cursor.fetchall()
    close()
    return result

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    close()

#function that gives list of quizes to user
def get_quizes():
    open()
    cursor.execute('SELECT * FROM quiz ORDER BY id')
    quiz_list = cursor.fetchall()
    close()
    return quiz_list

#function that determines which quiz was chosen(needed to deermine the background-image of the test)
def get_quiz_name(id):
    open()
    cursor.execute('SELECT quiz.name FROM quiz WHERE quiz.id == (?)', id)
    name = cursor.fetchall()
    close()
    return name[0][0]

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')
    
def main():
    list_questions = all_questions
    list_questions_Quiz_Content = list_questions_QuizContent
    quizes = all_quizes
    clear_db()
    create_question(list_questions)
    create_quiz(quizes)
    create_content_quiz(quizes, list_questions_QuizContent)
    open()
    cursor.execute("SELECT * FROM question")

if __name__ == "__main__":
    main()
    #print(get_question_after(1, 2))



#СВЯЗЬ quiz_content
#1 1 1 1 1 2 1 1 3 1 2 4 2 2 5 3 2 6 5 3 7 5 3 8 2 3 9 ПО ПОРЯДКУ
#1 3 7 1 2 4 1 2 6 1 1 2 1 3 8 1 1 3 1 1 1 1 2 5 1 3 9 В РАЗНОБОЙ