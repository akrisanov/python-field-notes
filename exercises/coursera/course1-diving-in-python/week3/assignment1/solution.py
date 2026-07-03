class FileReader:
    def __init__(self, file_path):
        """Создает экземпляр класса с указанным путем до файла."""
        self.file_path = file_path

    def read(self) -> str:
        """Возвращает содержимое файла."""
        try:
            with open(self.file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""
