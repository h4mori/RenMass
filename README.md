# [Russian]
### [!] Данная версия программы заточена под системы **Windows**. Автор не гарантирует полную работоспособность на других системах.
## Базовая информация
+ Библиотеки, используемые в коде: **tqdm**, **art**
+ Версия Python: **3.12.3**
+ Поддержка SMTP-протокола: **Да**
+ Поддержка почтовых сервисов кроме *Mail.Ru*: **Да**
## Установка
> Для **опытных** пользователей:
1. Сохранить данный репозиторий на ПК в виде архива и распаковать его.
2. Если *Python* еще не установлен, скачать его можно с <a href="https://www.python.org/downloads/release/python-3123" target="_blank">официального сайта</a>.
3. Установить зависимости проекта при помощи `pip install -r requirements.txt`.
4. Запустить файл *main.py* `python main.py`.
6. Настроить файл *config.json*, созданный в папке с *main.py*.
7. Повторить действия из пункта 4.
   
> Для **неопытных** пользователей (простая установка)
1. Запустить файл "*renmass.exe*" из папки "*Program*". *(Скомпилированная Portable-версия программы)*
2. Открыть файл *config.json* который появился в этой же папке при помощи блокнота
3. Настроить конфигурационный файл *config.json*
4. Запустить программу
   
## Настройка конфигурации (config.json)
> Перед началом настройки требуется получить **уникальный токен** от вашей учетной записи. Рассмотрим пример на основе <a href="https:/mail.ru" target="_blank">Mail.Ru</a>
1. Авторизуйтесь в сервисе Mail.Ru
2. Перейдите по <a href="https://account.mail.ru/user/2-step-auth/passwords">ссылке</a>, создайте ключ *"Только отправка сообщений (SMTP)"* и скопируйте его.
3. Откройте config.json при помощи блокнота или любым другим тектовым редактором
4. Вместо "email_here" напишите адрес электронной почты, к которой вы создавали ключ. Пример: *noreply@renmass.ru*
5. Вместо "password_here" введите секретный ключ, полученный в пункте 2. Пример: *9jqotmaLEeaongripqme*

# [English]
### [!] This version of the program is designed for **Windows** systems. The author does not guarantee full performance on other systems.
## Basic information
+ Libraries used in the code: *tqdm*, *art*
+ Python version: *3.12.3*
+ SMTP Support: **Yes**
+ Support for mail services except *Mail.Ru*: **Yes**
## Installation
> For **experienced** users:
1. Save this repository on your PC as an archive and unzip it.
2. If *Python* is not installed yet, you can download it from <a href="https://www.python.org/downloads/release/python-3123 " target="_blank">of the official website</a>.
3. Install the project dependencies using `pip install -r requirements.txt `.
4. Run the file *main.py * `python main.py `.
6. Configure the *config.json* file created in the folder with *main.py *.
7. Repeat the steps from step 4.
   
> For **inexperienced** users (easy installation)
1. Run the file "*renmass.exe *"from the folder "*Program*". *(Compiled Portable version of the program)*
2. Open the *config.json* file that appeared in the same folder using notepad
3. Configure the configuration file *config.json*
4. Launch the program
   
## Configuration settings (config.json)
> Before starting the setup, you need to get a **unique token** from your account. Let's look at an example based on <a href="https:/mail.ru " target="_blank">Mail.Ru </a>
1. Log in to the service Mail.Ru
2. Go to <a href="https://account.mail.ru/user/2-step-auth/passwords ">link</a>, create a key *"Only sending messages (SMTP)"* and copy it.
3. Open config.json using notepad or any other text editor
4. Instead of "email_here", write the email address to which you created the key. Example: *noreply@renmass.ru*
5. Instead of "password_here", enter the secret key obtained in step 2. Example: *9jqotmaLEeaongripqme*
