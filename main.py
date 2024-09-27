import smtplib
from json import load, dump
from email.mime.text import MIMEText
from tqdm import tqdm
from pick import pick
from art import text2art
from os import system

users = []
theme = "С днем рождения!"
msg = ("Здравствуйте, уважаемый пользователь! Мы очень рады, что вы - наш клиент, и в такой замечательный день, в "
       "ваш день рождения, мы дарим вам скидку 10% на все наши продукты!")


def logo(subtitle="Выберите опцию: "):
    data = ["Developer: Назар Моисеенко", "Telegram: @h4mori"]
    maxlen = 0
    for element in data:
        if maxlen < len(element):
            maxlen = len(element)
    return text2art("RenMass") + "\n" + "=" * maxlen + "\n" + '\n'.join(data) + "\n" + "=" * maxlen + "\n\n" + subtitle


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
    global theme, msg
    system("cls")
    if cmd == "Обновить список получателей":
        print(logo("Введите получателя (введите \"exit\" чтобы прекратить ввод)"))
        while True:
            user = input("-> ")
            if user in users:
                print("\033[91m[!] Этот пользователь уже есть в списке!\033[0m\n")
            elif "@" in user:
                users.append(user)
                print("\033[94m[*] Пользователь добавлен\033[0m\n")
            elif user == "exit":
                break
            else:
                print("\033[91m[!] Пользователь не добавлен, так как указана некорректная почта\033[0m\n")
    elif cmd == "Посмотреть список получателей":
        recs = ""
        for user in users:
            recs += f"[*] {user}\n"
        pick(["Выход"], logo(f"Список получателей: \n\n{recs}"))
    elif cmd == "Смена темы сообщения":
        quest = input(logo(f"Текущая тема: {theme}\n\n* Если вы хотите ее сменить, введите новую тему ниже\n* Если вы "
                           f"передумали, введите \"exit\"\n\n-> "))
        if quest != "exit":
            theme = quest
    elif cmd == "Смена текста сообщения":
        quest = input(logo(f"Текущий текст: {msg}\n\n* Если вы хотите его сменить, введите новый текст ниже\n* Если вы "
                           f"передумали, введите \"exit\"\n\n-> "))
        if quest != "exit":
            msg = quest
    elif cmd == "Начать рассылку":
        recs = "\n\n"
        for user in users:
            recs += f"[*] {user}\n"
        text = logo(f"Перед тем как начать, проверим данные:\n\nТема: {theme}\nСообщение: {msg}\n\nПолучатели: {recs}")
        t, tt = pick(["Да, начинаем рассылку!", "Пожалуй, внесу правки..."], text)
        if t == "Да, начинаем рассылку!":
            for i in tqdm(range(len(users)), ascii=True, desc="Отправка"):
                send(theme, msg, users[i])
            pick(["Выход"], "Рассылка завершена!")
    elif cmd == "Выход":
        exit()
    return ["Обновить список получателей", "Посмотреть список получателей", "Смена темы сообщения",
            "Смена текста сообщения", "Начать рассылку", "Выход"]


if __name__ == "__main__":
    options = commands()
    try:
        with open("config.json", "r") as file:
            config = load(file)
    except FileNotFoundError:
        with open("config.json", "w") as file:
            filedump = {"user": "email_here", "password": "password_here", "users": ""}
            dump(filedump, file, indent=4)
        raise FileNotFoundError("Не настроен файл config.json. Настройте файл в корне программы и повторите запуск.")
    while True:
        option, index = pick(options, logo())
        options = commands(option)
