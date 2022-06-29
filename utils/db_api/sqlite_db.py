import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('sixth_floor.db')
    cur = base.cursor()

    # Таблица для соотношения комнат и айди их жильцов
    base.execute('CREATE TABLE IF NOT EXISTS {}(room_number, user_id)'.format('users_id'))
    # таблица для соотношения айди старост и их этажей
    base.execute('CREATE TABLE IF NOT EXISTS {}(floor PRIMARY KEY, user_id)'.format('supervisors'))

    if base:
        print('Data base connected OK!')
    base.commit()


async def sql_add_command(room, user_id):
    cur.execute('INSERT INTO users_id VALUES(?, ?)', (room, user_id))
    base.commit()


# Получить список айди студентов, которые дежурят сегодня
def get_students_id(current_day):
    id_list = []
    try:
        for floor_number in range(2, 17):
            floor = 'floor' + str(floor_number)
            student_room = cur.execute('SELECT room FROM {} WHERE day == ?'.format(floor), (current_day,)).fetchone()
            student_id = cur.execute('SELECT user_id FROM users_id WHERE room_number == ?', (student_room[0],)).fetchall()

            for i in range(len(student_id)):
                id_list.append(student_id[i][0])
    except Exception:
        pass
    return id_list


# Удалить айди студента из бд
def del_student_id(student_id):
    cur.execute('DELETE FROM users_id WHERE user_id == ?', (student_id,))
    base.commit()


# Добавить айди старосты в бд
async def add_supervisor(floor, supervisor_id):
    cur.execute('INSERT INTO supervisors VALUES(?, ?)', (floor, supervisor_id))
    base.commit()


# Удалить айди старосты из дб
async def del_supervisor(floor):
    cur.execute('DELETE FROM supervisors WHERE floor == ?', (floor,))
    base.commit()


# Получить айди всех старост
def get_supervisors_id():
    supervisors_list = []
    supervisors = cur.execute('SELECT user_id FROM supervisors').fetchall()
    for index in range(len(supervisors)):
        supervisors_list.append(supervisors[index][0])
    return supervisors_list
