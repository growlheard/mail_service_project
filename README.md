# Mail Service Project
**Менеджер рассылок - это онлайн-платформа, позволяющая создавать и отправлять электронные письма большому количеству адресатов с**
**возможностью настройки параметров отправки и получения статистики по доставке и открытию писем.**

# Запуск на Windows
## **Установите виртуальное окружение командой**
```bash
python -m venv venv
```
## **Запустите виртуальное окружение командой**
```bash
venv\Scripts\activate 
```

## **Установите зависимости из файла `requirements.txt`**
```bash
pip install -r requirements.txt
```
## **Так же нужно поставить  redis, используйте wsl, терминал Ubuntu**
```bash
sudo apt-get update
sudo apt-get install redis
```
После установки запустите сервер Redis с помощью:
```bash
sudo service redis-server start
```
## Создайте файл `.env`
_Заполните настройки следуя файлу: `.env.sample`
```bash
CACHE_ENABLED=
CACHE_LOCATION=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_PORT=
```
## Выполните `migrate`
```bash
python manage.py migrate
```
## **После этого можно запустить сервер командой : **
```bash
python manage.py runserver
```
## **Для запуска периодичных рассылок используйте команду: **
```bash
python manage.py services
```
