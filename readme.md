## Требования 

1. Установлен Microsoft Visual C++ 14.0 и выше. [Сюда](https://learn.microsoft.com/en-us/answers/questions/136595/error-microsoft-visual-c-140-or-greater-is-require.html) если нет
   

## Настройка

1. Создать виртуальное окружение 

```python
python -m vevn .
```

2. Активировать виртуальное окружение

- linux/macos
```python
source Scripts/activate
```

 - windows
```python
Scripts\activate.bat   
```

1. Установить библиотеки

```python
(venv) pip install -r requirements.txt
```

4. Скопировать файл `.env copy`, переименовать файл `.env copy` в `.env` добавить необходимые переменные в файл.

## Функционал

1. Запуск

```python
(venv) python main.py
```