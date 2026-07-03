import functools
import json


def to_json(f):
    @functools.wraps(f)
    def serialize(*args, **kwargs):
        return json.dumps(f(*args, **kwargs))
    return serialize


@to_json
def get_data():
    return {
        "data": 42
    }


if __name__ == "__main__":
    assert(get_data() == '{"data": 42}')
