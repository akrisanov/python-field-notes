import os
import tempfile


class File:
    def __init__(self, file_path: str):
        """Если файл не существует, он создается при инициализации инстанса класса."""
        self.file_path = file_path

        if not os.path.exists(file_path):
            with open(file_path, "w"):
                pass

    def read(self):
        """Возвращает строку с текущим содержанием файла."""
        with open(self.file_path) as f:
            return f.read()

    def write(self, content: str) -> int:
        """Запись в файл нового содержимого в виде строки."""
        with open(self.file_path, "w") as f:
            return f.write(content)

    def __add__(self, other):
        """
        Создается новый файл и файловый объект, в котором содержимое второго файла добавляется к
        содержимому первого файла. Новый файл создается в директории, полученной с помощью функции
        `tempfile.gettempdir`. Для получения нового пути используется `os.path.join`.
        """
        file_path = os.path.join(tempfile.gettempdir(), "concat.txt")
        tmp_file = self.__class__(file_path)
        new_content = self.read() + other.read()
        tmp_file.write(new_content)
        return tmp_file

    def __str__(self) -> str:
        """Возвращает полный путь до файла."""
        return self.file_path

    def __iter__(self):
        """Возвращает итератор."""
        with open(self.file_path) as f:
            for line in f:
                yield line
