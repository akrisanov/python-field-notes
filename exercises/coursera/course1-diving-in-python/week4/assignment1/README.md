# Файл с магическими методами

В этом задании вам нужно создать интерфейс для работы с файлами. Интерфейс должен предоставлять следующие возможности
по работе с файлами:

- чтение из файла, метод `read` возвращает строку с текущим содержанием файла
- запись в файл, метод `write` принимает в качестве аргумента строку с новым содержанием файла
- сложение объектов типа `File`, результатом сложения является объект класса `File`, при этом создается новый файл
и файловый объект, в котором содержимое второго файла добавляется к содержимому первого файла. Новый файл должен
создаваться в директории, полученной с помощью функции `tempfile.gettempdir`. Для получения нового пути можно
использовать `os.path.join`
- возвращать в качестве строкового представления объекта класса `File` полный путь до файла
- поддерживать протокол итерации, причем итерация проходит по строкам файла

При создании экземпляра класса `File` в конструктор передается полный путь до файла на файловой системе.
Если файла с таким путем не существует, он должен быть создан при инициализации.

Пример работы:

```python
>>> import os.path
>>> from solution import File
>>> path_to_file = 'some_filename'
>>> os.path.exists(path_to_file)
False
>>> file_obj = File(path_to_file)
>>> os.path.exists(path_to_file)
True
>>> file_obj.read()
''
>>> file_obj.write('some text')
9
>>> file_obj.read()
'some text'
>>> file_obj.write('other text')
10
>>> file_obj.read()
'other text'
>>> file_obj_1 = File(path_to_file + '_1')
>>> file_obj_2 = File(path_to_file + '_2')
>>> file_obj_1.write('line 1\n')
7
>>> file_obj_2.write('line 2\n')
7
>>> new_file_obj = file_obj_1 + file_obj_2
>>> isinstance(new_file_obj, File)
True
>>> print(new_file_obj)
C:\Users\Media\AppData\Local\Temp\71b9e7b695f64d85a7488f07f2bc051c
>>> for line in new_file_obj:
....    print(ascii(line))
'line 1\n'
'line 2\n'
```
