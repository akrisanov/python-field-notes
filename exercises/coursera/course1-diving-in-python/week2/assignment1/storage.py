import argparse
import json
import os
import tempfile

storage_path = os.path.join(tempfile.gettempdir(), "storage.data")


def parse_args():
    """Возвращает объект аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Простое key-value хранилище во временном файле.")
    parser.add_argument("--key", required=True,
                        help="ключ по которому сохраняются/получаются значения")
    parser.add_argument("--val", help="сохраняемое значение")
    return parser.parse_args()


def read_from_storage():
    """Десериализует JSON читая его из файла."""
    if not os.path.exists(storage_path):
        return {}

    with open(storage_path, "r") as f:
        raw_data = f.read()
        if raw_data:
            return json.loads(raw_data)
        return {}


def write_to_storage(data):
    """Сериализует данные в JSON и записывает их в файл."""
    with open(storage_path, "w") as f:
        f.write(json.dumps(data))


def get(key):
    """"Получение списка значений по ключу из файлового хранилища."""
    data = read_from_storage()
    return data.get(key, [])


def set(key, value):
    """
    Сохранение значения по ключу в примитивное файловое хранилище.
    Значения по одному ключу не перезаписываются, а добавляются к уже сохраненным.
    """
    data = read_from_storage()
    data[key] = data.get(key, [])
    data[key].append(value)
    write_to_storage(data)


if __name__ == "__main__":
    args = parse_args()

    if args.key and args.val:
        set(args.key, args.val)
    else:
        print(*get(args.key), sep=", ")
