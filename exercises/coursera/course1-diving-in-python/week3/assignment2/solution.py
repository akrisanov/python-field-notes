import csv
import pprint
import os


class CarBase:
    """Базовый класс для всех типов машин."""

    allowed_photo_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    allowed_car_types = ["car", "truck", "spec_machine"]

    def __init__(self, car_type: str, brand: str, photo_file_name: str, carrying: float):
        """
        Создает экземпляр класса.

        :param car_type: значение типа объекта и может принимать одно из значений:
        «car», «truck», «spec_machine»
        :param brand: марка производителя автомобиля
        :param photo_file_name: имя файла с изображением автомобиля, допустимы названия файлов
        изображений с расширением из списка: «.jpg», «.jpeg», «.png», «.gif»
        :param carrying: грузоподъемность
        """
        if car_type in self.allowed_car_types:
            self.car_type = car_type
        else:
            raise ValueError("Тип объекта должен иметь одно из следующих значений: ",
                             ", ".join(self.allowed_car_types))

        if brand:
            self.brand = brand
        else:
            raise ValueError("Не указана марка производителя автомобиля")

        if self._get_file_ext(photo_file_name) in self.allowed_photo_extensions:
            self.photo_file_name = photo_file_name
        else:
            raise ValueError(
                "Имя файла с изображением автомобиля должно иметь одно из следующих расширений: ",
                ", ".join(self.allowed_photo_extensions))

        if carrying:
            self.carrying = float(carrying)
        else:
            raise ValueError("Не указана грузоподъемность")

    @staticmethod
    def _get_file_ext(file_path):
        _root, ext = os.path.splitext(file_path)
        return ext

    def get_photo_file_ext(self) -> str:
        """Возвращает расширение файла изображения автомобиля."""
        return self._get_file_ext(self.photo_file_name)


class Car(CarBase):
    """Класс легкового автомобиля."""

    def __init__(self, brand: str, photo_file_name: str, carrying: float,
                 passenger_seats_count: int):
        """
        Создает экземпляр класса.

        :param brand: марка производителя автомобиля
        :param photo_file_name: имя файла с изображением автомобиля, допустимы названия файлов
        изображений с расширением из списка: «.jpg», «.jpeg», «.png», «.gif»
        :param carrying: грузоподъемность
        :param passenger_seats_count: количество пассажирских мест
        """
        super().__init__("car", brand, photo_file_name, carrying)
        if passenger_seats_count:
            self.passenger_seats_count = int(passenger_seats_count)
        else:
            raise ValueError("Не указано количество пассажирских мест")


class Truck(CarBase):
    """Класс грузового автомобиля."""

    def __init__(self, brand: str, photo_file_name: str, carrying: float, body_whl: str):
        """
        Создает экземпляр класса.

        :param brand: марка производителя автомобиля
        :param photo_file_name: имя файла с изображением автомобиля, допустимы названия файлов
        изображений с расширением из списка: «.jpg», «.jpeg», «.png», «.gif»
        :param carrying: грузоподъемность
        :param body_whl: строка, в которой размеры разделены латинской буквой «x»
        """
        super().__init__("truck", brand, photo_file_name, carrying)

        body_whl = body_whl.split("x")

        if len(body_whl) != 3:
            self.body_width = self.body_height = self.body_length = 0.0
        else:
            whl = [float(p) for p in body_whl]
            self.body_length = whl[0]
            self.body_width = whl[1]
            self.body_height = whl[2]

    def get_body_volume(self) -> float:
        """Возвращает объем кузова."""
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    """Класс спецтехники."""

    def __init__(self, brand: str, photo_file_name: str, carrying: float, extra: str):
        """
        Создает экземпляр класса.

        :param brand: марка производителя автомобиля
        :param photo_file_name: имя файла с изображением автомобиля, допустимы названия файлов
        изображений с расширением из списка: «.jpg», «.jpeg», «.png», «.gif»
        :param carrying: грузоподъемность
        :param extra: дополнительное описание автомобиля
        """
        super().__init__("spec_machine", brand, photo_file_name, carrying)
        if extra:
            self.extra = extra
        else:
            raise ValueError("Не указано дополнительное описание автомобиля")


def get_car_list(csv_filename: str = "coursera_week3_cars.csv"):
    """
    Функция создает объекты классов на основе данных из CSV-файла.

    :param csv_filename: путь к файлу
    :return: список объектов с автомобилями
    """
    car_list = []

    with open(csv_filename, "r") as f:
        reader = csv.reader(f, delimiter=";")
        # пропускаем заголовки:
        # 0 car_type
        # 1 brand
        # 2 passenger_seats_count
        # 3 photo_file_name
        # 4 body_whl
        # 5 carrying
        # 6 extra
        next(reader)
        for row in reader:
            if len(row) == 0:
                continue

            try:
                if row[0] == "car":
                    car_object = Car(brand=row[1], photo_file_name=row[3], carrying=float(row[5]),
                                     passenger_seats_count=int(row[2]))
                elif row[0] == "truck":
                    car_object = Truck(brand=row[1], photo_file_name=row[3], carrying=float(row[5]),
                                       body_whl=row[4])
                elif row[0] == "spec_machine":
                    car_object = SpecMachine(brand=row[1], photo_file_name=row[3],
                                             carrying=float(row[5]),
                                             extra=row[6])
                else:
                    # Не создаем объекты неверного типа
                    continue
            except ValueError:
                # Не создаем объекты с неверными данными
                continue

            car_list.append(car_object)

    return car_list


if __name__ == "__main__":
    pprint.pprint(get_car_list())
