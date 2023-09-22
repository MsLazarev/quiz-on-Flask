import sqlite3
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

def create_quiz(quizes):
    quiz = """CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY,
        name VARCHAR);"""
    
    do(quiz)

    cursor.executemany("""INSERT INTO quiz
    (name)
    VALUES (?)""", quizes)
    do(quiz)

def create_content_quiz(quizes, list_questions):
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
    open()
    #МОЙ СПОСОБ СОЗДАНИЯ ДБ НЕ ИСПОЛЬЗУЯ КОНСОЛЬ
    for i in range(1, len(quizes) + 1):
        quiz_id = i
        for j in range(1, len(list_questions) + 1):
            if (len(list_questions) // len(quizes)) + 1 == j:
                break
            id_memory += 1
            question_id = id_memory
            cursor.execute(query, [quiz_id, question_id])            
            conn.commit()
    close()

    #CПОСОБ АЛГОРИТМИКИ С ПОМОЩЬЮ КОНСОЛИ   
    # while input("Добавлять связь? y/n: ") != "n":
    #     quiz_id = int(input("id викторины: "))
    #     question = int(input("id вопроса: "))
    #     cursor.execute(query, [quiz_id, question])
    #     conn.commit()
        
def get_question_after(question_id=0, quiz_id=1):
    open()
    cursor.execute("SELECT quiz_content.id, question.question, question.answer, question.wrong_1, question.wrong_2, question.wrong_3 FROM quiz_content, question WHERE quiz_content.question_id == question.id AND quiz_content.quiz_id == (?) AND quiz_content.id > (?) ORDER BY quiz_content.id", [quiz_id, question_id])
    return cursor.fetchall()

# def verify_answer(answer):
#     open()
#     cursor.execute('SELECT question.answer FROM question WHERE question.answer == (?)', answer)
#     return cursor.fetchall()


def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def get_quizes():
    open()
    cursor.execute('SELECT * FROM quiz ORDER BY id')
    quiz_list = cursor.fetchall()
    print(quiz_list)
    print()
    close()
    return quiz_list


def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')
    
def main():
    quizes = [
        ('Математика', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )]
    list_questions = [
        ('Сколько будет 2 + 2?', 'Четыре', 'Один', 'Три', 'Пять'),
        ('Имя ученого который придумал нахождение гипотенузы по катетам?', 'Пифагор', 'Аристотель', 'Сократ', 'Паскаль'),
        ('Формула площади ромба', 'половине произведения диагоналей', 'произведению 2ух сторон', 'половине произведения высоты на сторону', 'произведению диагоналей'),

        ('Самое большое млекопитающее?', 'Синий кит', 'Слон', 'Акула', 'Гиппопотам'),
        ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
        ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),

        ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
        ('Что не поместится даже в самую большую кастрюлю во вселенной?', 'Ее крышка', 'Планета', 'Кастрюля супа', '100000 грузовиков'),
        ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')]
    clear_db()
    create_question(list_questions)
    create_quiz(quizes)
    create_content_quiz(quizes, list_questions)


if __name__ == "__main__":
    main()
    #print(get_question_after(1, 2))



#СВЯЗЬ quiz_content
#1 1 1 1 1 2 1 1 3 1 2 4 2 2 5 3 2 6 5 3 7 5 3 8 2 3 9 ПО ПОРЯДКУ
#1 3 7 1 2 4 1 2 6 1 1 2 1 3 8 1 1 3 1 1 1 1 2 5 1 3 9 В РАЗНОБОЙ