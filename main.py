import smtplib
from json import load, dump
from email.mime.text import MIMEText
from tqdm import tqdm
from pick import pick
from art import text2art
from os import system


def conf_manage(mode: str, data=None):
    try:
        with open("config.json", mode, encoding="utf-8") as file:
            if mode == "r":
                return load(file)
            elif mode == "w":
                dump(data, file, indent=4)
                return True
    except FileNotFoundError:
        with open("config.json", "w", encoding="utf-8") as file:
            data = {"user": "email_here",
                    "password": "password_here",
                    "title": "С днем рождения!",
                    "subtitle": "Здравствуйте, уважаемый пользователь! Мы очень рады, что вы - наш клиент, и в такой "
                                "замечательный день, в ваш день рождения, мы дарим вам скидку 10% на все наши "
                                "продукты!",
                    "users": ""}
            dump(data, file, indent=4)
            return pick(["Выход"], logo("Конфигурационный файл программы не найден.\nВ папке с программой п"
                                        "оявился файл config.json,\nнастройте его в соответствии с документацией."))


def logo(subtitle="Выберите опцию: "):
    data = ["Developer: Назар Моисеенко", "Telegram: @h4mori", "Group: РПО 24/3"]
    sep = f"\n{'=' * max(map(len, data))}\n"
    return text2art("RenMass") + sep + '\n'.join(data) + sep + "\n" + subtitle


def send(title: str, message: str, recipient: str):
    server = smtplib.SMTP_SSL("smtp.mail.ru", 465)
    try:
        server.login(config["user"], config["password"])
    except smtplib.SMTPAuthenticationError:
        raise ValueError("Указаны неверные данные в config.json")
    message = MIMEText(message + "\n\n⚠ Это сообщение сформировано автоматически. Пожалуйста, не отвечайте на него.")
    message["Subject"] = title
    message["From"] = config["user"]
    message["To"] = recipient
    server.send_message(message)
    server.quit()
    return True


def commands(cmd=None):
    title, subtitle = config["title"], config["subtitle"]
    if config["users"]:
        users = config["users"].split(";")
    else:
        users = []
    system("cls")
    if cmd == "Получатели":
        recs = ""
        if users:
            for user in users:
                recs += f"[*] {user}\n"
        else:
            recs = "[*] Никого нет, список пуст."
        opt, idx = pick(["Добавить получателей", "Очистить список", "На главную"],
                        logo(f"Список получателей: \n\n{recs}"))
        if opt == "Добавить получателей":
            print(logo("Введите получателя (введите \"exit\" чтобы прекратить ввод)"))
            while True:
                user = input("-> ")
                if user in users:
                    print("\033[91m[!] Этот пользователь уже есть в списке!\033[0m\n")
                elif "@" in user:
                    users.append(user)
                    print("\033[94m[*] Пользователь добавлен\033[0m\n")
                elif user == "exit":
                    config["users"] = ";".join(users)
                    return commands("Получатели")
                else:
                    print("\033[91m[!] Пользователь не добавлен, так как указана некорректная почта\033[0m\n")
        elif opt == "Очистить список":
            config["users"] = []
    elif cmd == "Электронное сообщение":
        opt, idx = pick(["Сменить тему", "Сменить текст", "На главную"], logo(
            f"Тема сообщения: {title}\nТекст: {subtitle}\n\n[*] Полное сообщение можно увидеть в пункте\n\"Сменить "
            f"сообщение\"."))
        if opt == "Сменить тему":
            quest = input(
                logo(f"Текущая тема: {title}\n\n* Если вы хотите ее сменить, введите новую тему ниже\n* Если вы "
                     f"передумали, введите \"exit\"\n\n-> "))
            if quest != "exit":
                config["title"] = quest
                return commands("Электронное сообщение")
        elif opt == "Сменить текст":
            quest = input(
                logo(f"Текущий текст: {subtitle}\n\n* Если вы хотите его сменить, введите новый текст ниже\n* Если вы "
                     f"передумали, введите \"exit\"\n\n-> "))
            if quest != "exit":
                config["subtitle"] = quest
                return commands("Электронное сообщение")
    elif cmd == "Начать рассылку":
        recs = "\n\n"
        for user in users:
            recs += f"[*] {user}\n"
        t, tt = pick(["Да, начинаем рассылку!", "Пожалуй, внесу правки..."], logo(
            f"Перед тем как начать, проверим данные:\n\nТема: {title}\nСообщение: {subtitle}\n\nПолучатели: {recs}"))
        if t == "Да, начинаем рассылку!":
            for i in tqdm(range(len(users)), ascii=True, desc="Рассылка"):
                send(title, subtitle, users[i])
            config["users"] = ";".join(users)
            config["title"] = title
            config["subtitle"] = subtitle
            conf_manage("w", config)
            t, tt = pick(["Создать еще одну рассылку", "Выход из программы"],
                         "Рассылка завершена!\nСписок получателей, тема и сообщение сохранены.")
            if tt == 1:
                exit()
    elif cmd == "Выход":
        exit()
    return ["Получатели", "Электронное сообщение", "Начать рассылку", "Выход"]


if __name__ == "__main__":
    config = conf_manage("r")
    options = commands()
    while True:
        option, index = pick(options, logo())
        options = commands(option)
