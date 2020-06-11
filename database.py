import psycopg2 as pg


with pg.connect(database='my_base', user='user_new', password='1111',
                host='localhost', port=5432) as conn:
    cur = conn.cursor()
    """Создание таблицы"""
    def create_db(name_db, title):
        if title == 'student':
            cur.execute(f'''CREATE TABLE IF NOT EXISTS {name_db} (
                                        id SERIAL PRIMARY KEY,
                                        name VARCHAR(40) NOT NULL,
                                        gpa DECIMAL(3, 2)
                                    );''')
        elif title == 'course':
            cur.execute(f'''CREATE TABLE IF NOT EXISTS {name_db} (
                                            id SERIAL PRIMARY KEY,
                                            name character varying(100) not null
                                        );''')

    # создаем таблицу студента
    create_db('student', 'student')

    # создаем таблицу курса
    create_db('course', 'course')

    def add_student(id, name, *args): # просто создает студента

        if args != ():
            cur.execute('INSERT INTO student(id, name, gpa) VALUES (%s, %s, %s);', (id, name, args[0]))
            conn.commit()
        elif id != None and name != None and args == ():
            cur.execute('INSERT INTO student(id, name) VALUES (%s, %s);', (id, name))
            conn.commit()
        else:
            pass

    #add_student(1, "Egor")
    # add_student(2, "Igor", 5)
    # add_student(3, "Vlodimir", 5.54)
    # add_student(4, "Ura", 2.34)
    #add_student(5, "Petr")
    #add_student(6, "Son")

    def add_course(id, name):
        cur.execute('INSERT INTO course(id, name) VALUES (%s, %s);', (id, name))
        conn.commit()

    # add_course(1, 'course_namber_one')
    # add_course(2, 'course_namber_two')
    # add_course(3, 'course_namber_three')
    # add_course(4, 'course_namber_four')
    # add_course(5, 'course_namber_five')

    cur.execute('''SELECT id, name, gpa FROM student;''')
    print("Выводим студентов", cur.fetchall(), "\n")

    cur.execute('''SELECT * FROM course;''')
    print("Вывод курсов", cur.fetchall(), "\n")

    #add_student(12, "Igor", 2.34)
    #conn.rollback()  # не применять изменения
    # cur.execute("select * from student;")
    # print(cur.fetchall()) # увидим, что студент не создался

    def delete(name, title):
        if title == 'course':
            cur.execute('''DELETE FROM course WHERE name = %s;''', (name,))
        elif title == 'student':
            cur.execute('''DELETE FROM student WHERE name = %s;''', (name,))
        else:
            pass

    """Удаление студента или курса по имени"""
    delete("Son", 'student')

    cur.execute('''SELECT id, name, gpa FROM student;''')
    print("Удалили студента", cur.fetchall(), "\n")

    """Удаление всех студентов и курсов"""
    #cur.execute('''DELETE FROM course;''')

    """Удаление таблиц студентов и курсов"""
    #cur.execute('''DROP TABLE IF EXISTS course ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS student_course (
            id serial PRIMARY KEY,
            student_id INT REFERENCES student(id),
            course_id INT REFERENCES course(id)
        );''')

    """Записываем студента на курс"""
    def add_sc(student_id, course_id):
        cur.execute("""insert into student_course (student_id, course_id) values (%s, %s)""",(student_id, course_id))  # добавить связь студент-курс

        cur.execute("""select s.id, s.name, c.name from student_course sc
        join student s on s.id = sc.student_id
        join course c on c.id = sc.course_id""")


        print("Студент записанный на курс", cur.fetchall(), "\n")

    cur.execute('''DELETE FROM student_course;''')
    add_sc(2,2)
    add_sc(3,4)

    def get_students(course_id):
        cur.execute("""select s.id, s.name, c.id, c.name from student_course sc
                join student s on s.id = sc.student_id
                join course c on c.id = sc.course_id""")

        information = cur.fetchall()
        for item in information:
            if item[2] == course_id:
                print(f'{item[1]} на курсе {item[2]}')

    get_students(2)

    def get_course(student_id):
        cur.execute("""select s.id, s.name, c.id, c.name from student_course sc
                        join student s on s.id = sc.student_id
                        join course c on c.id = sc.course_id""")

        information = cur.fetchall()
        for item in information:
            if item[0] == student_id:
                print(item[3])

    get_course(3)

    cur.execute('''SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');''')
    print(cur.fetchall())