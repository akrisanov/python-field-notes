# Реализация простого класса для чтения из файла

Ваша задача: написать python-модуль `solution.py`, внутрь которого необходимо поместить код класса `FileReader`.
Конструктор этого класса принимает один параметр: путь до файла на диске.
В классе `FileReader` должен быть реализован метод `read`, возвращающий строку - содержимое файла,
путь к которому был указан при создании экземпляра класса. Python модуль должен быть написан таким
образом, чтобы импорт класса `FileReader` из него не вызвал ошибок.

При написании реализации метода `read`, вам нужно учитывать случай, когда при инициализации был
передан путь к несуществующему файлу. Требуется обработать возникающее при этом исключение `FileNotFoundError`
и вернуть из метода `read` пустую строку.

Пример работы:

```python
>>> from solution import FileReader
>>> reader = FileReader('not_exist_file.txt')
>>> text = reader.read()
>>> text
''
>>> with open('some_file.txt', 'w') as file:
...     file.write('some text')
...
9
>>> reader = FileReader('some_file.txt')
>>> text = reader.read()
>>> text
'some text'
>>> type(reader)
<class 'solution.FileReader'>
>>> 
```
