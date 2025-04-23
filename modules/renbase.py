import sqlite3
from base64 import b64encode
from random import choice
from os import remove, path, makedirs, getcwd
from shutil import copy2
from datetime import datetime
from tkinter.filedialog import askopenfilename
from modules import rentempl, renmail

def send(request: str, alldata=False):
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute(request)
    if not alldata:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()
    con.commit()
    cursor.close()
    con.close()
    return result


def check_auth(username: str, password: bytes):
    data = send(f'SELECT username FROM users WHERE username="{username}"')
    if data:
        status = send(f'SELECT status FROM users WHERE username="{username}"')[0]
        if b64encode(password).decode() == send(f'SELECT password FROM users WHERE username="{username}"')[0] and status != "deactivated":
            print(f"Пользователь {username} авторизовался в системе.")
            return "Authentificated"
        print(f"Неудачная попытка аутентификации от имени {username}. [{status}]")
        return "IncorrectPassword"
    return "UserNotExist"

def keygen(chars: list, length: int):
    result = ""
    data = ""
    for element in chars:
        if element == "nums":
            data += "1234567890" 
        elif element == "chars_upper":
            data += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        elif element == "chars_lower":
            data += "abcdefghijklmnopqrstuvwxyz"
    for _ in range(length):
        result += choice(data)
    return result

def get_tables(active): # Используется для вывода блоков с таблицами
    tables = send("SELECT id, name FROM records", True)
    data = ""
    if tables and active:
        for tid, tname in tables:
            if str(tid) == str(active):
                text = ["", "Выбрано"]
            else:
                text = [f'href="/select/id{tid}"', "Выбрать"]
            data += f'<div class="stat-block"><span class="icon">⭐</span><div><div>{tname}</div><div><a {text[0]}>{text[1]}</a></div></div></div>'
    return data

def changepassword(uid, password):
    encoded = b64encode(password.encode()).decode()
    send(f'UPDATE users SET password="{encoded}" WHERE id={uid}')
    userdata = send(f"SELECT first_name, username, email FROM users WHERE id={uid}")[0]
    renmail.send(send("SELECT smtp_server, smtp_port, smtp_user, smtp_password FROM settings WHERE id=1"), rentempl.changepassword(userdata[0], userdata[1], password), [userdata[2]])
    return True

def newuser(username, email, first_name):
    if not send(f'SELECT * FROM users WHERE username="{username}"') and not send(f'SELECT * FROM users WHERE email="{email}"'):
        newpasswd = keygen(["chars_upper", "chars_lower"], 6)
        send(f'INSERT INTO users ("username", "first_name", "email", "role", "status") VALUES ("{username}", "{first_name}", "{email}", "user", "activated")')
        changepassword(send(f'SELECT id FROM users WHERE username="{username}"')[0], newpasswd)
        renmail.send(send("SELECT smtp_server, smtp_port, smtp_user, smtp_password FROM settings WHERE id=1"), rentempl.welcome(first_name, username, newpasswd), [email])
        copy2("files/img/default.png", f"files/img/users/{username}.png")
        return True
    return False

def flushdb():
    remove("database.db")

def create_db():
    requests = ['CREATE TABLE "records" ("id" INTEGER,"name" TEXT,"title" TEXT,"subject" TEXT,"recipients" TEXT,PRIMARY KEY("id" AUTOINCREMENT));',
    'CREATE TABLE "settings" ("id" INTEGER, "smtp_server" TEXT, "smtp_port" INTEGER, "smtp_user" TEXT, "smtp_password" TEXT, PRIMARY KEY("id" AUTOINCREMENT));',
    'CREATE TABLE "users" ("id" INTEGER, "username" TEXT, "password" TEXT, "first_name" TEXT, "email" TEXT, "role" TEXT, "status" TEXT, PRIMARY KEY("id" AUTOINCREMENT));',
    'INSERT INTO settings ("id") VALUES (1);',
    'INSERT INTO users ("id", "username", "password", "first_name", "email", "role", "status") VALUES (1, "admin", "YWRtaW4=", "Администратор", "admin@li-ren.ru", "admin", "activated");']
    for req in requests:
        send(req)
    return True

def backup():
    if not path.exists('backups'):
        makedirs('backups')
    copy2("database.db", f"backups/{datetime.now().strftime('%d-%m-%Y')}.db")

def restore():
    from_restore = askopenfilename()
    if from_restore != "":
        remove("database.db")
        copy2(from_restore, "database.db")
        return True
    return False