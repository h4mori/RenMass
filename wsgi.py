from flask import Flask, render_template, session, redirect, request
from markupsafe import Markup
from modules import renbase, rentempl, renmail
from webbrowser import open as weblink
from os import path

app = Flask(__name__, static_folder="files")


def alert(text: str, url: str):
    return f'<script type="text/javascript">alert("{text}"); window.location.href="{url}"; </script>'


@app.route("/")
def index():
    if "username" in session:
        if "table" not in session:
            session["table"] = None
            tables = renbase.send("SELECT id FROM records", True)
            if tables:
                session["table"] = tables[0][0]
        return render_template("index.html", first_name=session["first_name"], username=session["username"])
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect("/")
    elif request.method == "POST":
        username, password = request.values["login"], request.values["password"].encode()
        match renbase.check_auth(username, password):
            case "Authentificated":
                session["username"] = username
                session["first_name"] = renbase.send(f'SELECT first_name FROM users WHERE username="{username}"')[0]
                renmail.send(renbase.send("SELECT smtp_server, smtp_port, smtp_user, smtp_password FROM settings WHERE id=1"), rentempl.newauth(session["first_name"]), [renbase.send(f'SELECT email FROM users WHERE username="{username}"')[0]])
                return redirect("/")
            case "IncorrectPassword":
                return alert("Неверный пароль, или учетная запись деактивирована.", "/login")
            case "UserNotExist":
                return alert("Пользователя не существует", "/")
    return render_template("login.html")

@app.route("/message", methods=["GET", "POST"])
def message():
    if "username" not in session:
            return redirect("/")
    if request.method == "GET":
        data = renbase.get_tables(session["table"])
        tabledata = ["", ""]
        if data and session["table"]:
            temp = renbase.send(f'SELECT title, subject FROM records WHERE id={session["table"]}')
            if temp[0] != temp[1] != None:
                tabledata = temp
        return render_template("message.html", first_name=session["first_name"], username=session["username"], tables=Markup(data), title=tabledata[0], subject=tabledata[1])
    else:
        data = request.values
        renbase.send(f'UPDATE records SET title="{data["title"]}", subject="{data["subject"]}" WHERE id={session["table"]}')
        if "massmail" in data and data["massmail"] == "on":
            recipients = renbase.send(f'SELECT recipients FROM records WHERE id={session["table"]}')[0]
            if recipients:
                if renmail.send(renbase.send("SELECT smtp_server, smtp_port, smtp_user, smtp_password FROM settings WHERE id=1"), [data["title"], data["subject"]], recipients.split(";")):
                    return alert("Рассылка прошла успешно!", "/message")
            return alert("Рассылка не удалась. Вы указали данные от корпоративной почты?", "/settings")
        return redirect("/message")

@app.route("/tables", methods=["GET", "POST"])
def tables():
    if "username" not in session:
        return redirect("/")
    if request.method == "GET":
        data = renbase.get_tables(session["table"])
        userlist = "❌ | Список пуст!"
        if data:
            recipients = renbase.send(f'SELECT recipients FROM records WHERE id={session["table"]}')[0]
            if recipients:
                userlist = ""
                for recipient in recipients.split(";"):
                    userlist += f"👤 {recipient}\n"
        return render_template("tables.html", first_name=session["first_name"], username=session["username"], tables=Markup(data), recipients=userlist)
    else:
        data = request.values
        if "action" in data: # Если используют первую форму
            recipients = renbase.send(f'SELECT recipients FROM records WHERE id={session["table"]}')[0]
            if recipients:
                recipients = recipients.split(";")
            else:
                recipients = []
            if data["action"] == "add" and data["user"] not in recipients: recipients.append(data["user"])
            elif data["action"] == "remove" and data["user"] in recipients: recipients.remove(data["user"])
            renbase.send(f'UPDATE records SET recipients="{";".join(recipients)}" WHERE id={session["table"]}')
        elif "table_action" in data:
            if data["table_action"] == "add":
                tables = renbase.send("SELECT name FROM records", True)
                for table in tables:
                    if table == data["table"]: return alert("Такая таблица уже существует!", "/tables")
                renbase.send(f'INSERT INTO records ("name") VALUES ("{data["table"]}")')
                session["table"] = renbase.send(f'SELECT id FROM records WHERE name="{data["table"]}"')[0]
            elif data["table_action"] == "remove":
                renbase.send(f'DELETE FROM records WHERE name="{data["table"]}"')
        return redirect("/tables")

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if "username" not in session:
        return redirect("/")
    if request.method == "GET":
        userdata = renbase.send(f'SELECT id, role, email FROM users WHERE username="{session["username"]}"')
        admin = False
        if userdata[1] == "admin":
            admin = True
        smtp = renbase.send("SELECT smtp_server, smtp_port, smtp_user, smtp_password FROM settings WHERE id=1")
        userlist = renbase.send("SELECT * FROM users", True)
        users = ""
        for user in userlist:
            users += f"<tr><td>{user[0]}</td><td>{user[1]}</td><td>Скрыт</td><td>{user[4]}</td><td>{user[5]}</td><td>{user[6]}</td></tr>"
        return render_template("settings.html", first_name=session["first_name"], admin=admin, 
            username=session["username"], email=userdata[2], id=userdata[0], role=userdata[1], 
            smail=smtp[2], spassword=smtp[3], sserver=smtp[0], sport=smtp[1], users=Markup(users))
    else:
        data = request.values
        if "password" in data: # Настройки SMTP-сервера
            renbase.send(f'UPDATE settings SET smtp_server="{data["server"]}", smtp_port={data["port"]}, smtp_user="{data["user"]}", smtp_password="{data["password"]}" WHERE id=1')
            return redirect("/settings")
        elif "action" in data: # Управление БД через option
            if data["action"] == "flush":
                renbase.flushdb()
                renbase.create_db()
                return alert(f"Пожалуйста, перезапустите программу!", "/settings")
            elif data["action"] == "backup":
                renbase.backup()
            elif data["action"] == "restore":
                if not renbase.restore():
                    return alert("Действие было прервано", "/settings")
                else:
                    return alert("Бэкап восстановлен. Пожалуйста, перезапустите программу!", "/settings")
            return redirect("/settings")
        elif "newrow" in data: # Смена данных в бд через форму
            if data["row"] == "password":
                renbase.changepassword(data["id"], data["newrow"])
            else:
                renbase.send(f'UPDATE users SET {data["row"]}="{data["newrow"]}" WHERE id={data["id"]}')
            return redirect("/settings")
        elif "new_username" in data: # Добавление юзера
            if renbase.newuser(data["new_username"], data["new_email"], data["new_first_name"]):
                return alert("Аккаунт был зарегистрирован. Сообщение было отправлено получателю", "/settings")
            return alert("Ошибка: пользователь с таким username или почтой уже существует")

@app.route("/select/<string:tableid>", methods=["GET"])
def select_table(tableid):
    if "username" not in session:
        return redirect("/")
    session["table"] = tableid[2:]
    return redirect("/message")

@app.route("/change_avatar", methods=["POST"])
def change_avatar():
        if request.method == "POST":
            file = request.files["file"]
            if file.filename.split(".")[1].lower() == "png":
                file.save(path.join(app.config['UPLOAD_FOLDER'], f'{session["username"]}.png'))
            else:
                return alert("Можно загружать только .png картинки!", "/")
        return redirect("/settings")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.secret_key = renbase.keygen(["chars_lower", "chars_upper"], 26)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['UPLOAD_FOLDER'] = "files/img/users/"
    weblink(f"http://127.0.0.1:1103")
    app.run("127.0.0.1", 1103)
