# CardioIntegro
## Как установить

1. Клонируем репозиторий

```
git clone git@github.com:almanelis/CardioIntegro.git
```
2. Создаём и активируем виртуальное окружение

```
python -m venv venv
```

```
source venv/Scripts/activate
```

3. Устанавливаем зависимости

```
pip install -r requirements.txt
```
## Запуск Django проекта
1. Переходим в директорию проекта
```
cd cardiointegro
```
2. Выполняем миграции
```
python manage.py migrate
```
3. Создаём суперюзера
```
python med_it_forum/manage.py createsuperuser
```
4. Запускаем приложение
```
python manage.py runserver
```
Далее переходим по url из терминала
## Запуск Tailwind CSS

```
python manage.py tailwind start
```
