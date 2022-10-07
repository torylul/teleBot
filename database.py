import sqlite3

connect = sqlite3.connect('C:/Users/vdolg/PycharmProjects/pythonProject/database.db', check_same_thread=False)
cursor = connect.cursor()

# выводит имя пользователя
def user_prov(id_user):
    sql = "SELECT users.id_user FROM users WHERE id_user=:id_user"
    result = cursor.execute(sql, {'id_user': id_user}).fetchone()
    connect.commit()
    return result

# проверка существует ли такая категория
def cat_prov_indef(id):
    sql = "SELECT categories.id FROM categories WHERE id=:id"
    result = cursor.execute(sql, {'id': id}).fetchone()
    connect.commit()
    return result

# проверка существует ли такая категория у пользователя
def cat_prov_indef_user(id_u, id_cat):
    result = cursor.execute("SELECT * FROM subscribes WHERE user_id=? AND categories_id=?", (id_u, id_cat)).fetchall()
    connect.commit()
    return result

# проверка подписан или нет пользователь
# def inner_id_cat(us, cat):
#     return cursor.execute("SELECT * FROM subscribes JOIN users ON users.id = subscribes.user_id JOIN categories ON categories.id = subscribes.categories_id WHERE user_id=? AND categories_id=?", (us, cat)).fetchall()

def inner_id_cat(us, cat):
    return cursor.execute("SELECT * FROM subscribes WHERE user_id=? AND categories_id=?", (us, cat)).fetchall()

# оформить подписку
def sub(us, cat):
    cursor.execute('INSERT INTO subscribes (user_id, categories_id) VALUES(?,?)', (us, cat))
    connect.commit()

# удалить подписку
def unsub(us, cat):
    cursor.execute('DELETE FROM subscribes WHERE user_id=? AND categories_id=?', (us, cat))
    connect.commit()

# список подписок
def res_sub():
    result = cursor.execute('SELECT categories.* FROM categories').fetchall()
    connect.commit()
    return result

# название категории
def name_cat(id_cat):
    result = cursor.execute('SELECT name FROM categories WHERE id=?', (id_cat, )).fetchall()
    connect.commit()
    return result

# список подписок юзера
def res_sub_user(id_user):
    return cursor.execute('SELECT * FROM categories INNER JOIN subscribes ON subscribes.categories_id = categories.id WHERE user_id=?', (id_user, )).fetchall()


# регистрация пользователя
def users_db(id_user: int, user_name: str):
    cursor.execute('INSERT INTO users (id_user, user_name) VALUES (?, ?)', (id_user, user_name))
    connect.commit()
