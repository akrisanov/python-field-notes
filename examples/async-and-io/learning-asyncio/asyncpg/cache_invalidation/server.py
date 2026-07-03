import argparse
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json
from util import Database
from perf import aelapsed, aprofiler
import model

app = Sanic()


@aelapsed
async def new_patron(request):
    data = request.json
    id = await model.add_patron(app.pool, data)
    return json({"msg": "ok", "id": id})


class PatronAPI(HTTPMethodView, metaclass=aprofiler):
    async def get(self, request, id):
        data = await model.get_patron(app.pool, id)
        return json(data)

    async def put(self, request, id):
        data = request.json
        ok = await model.update_patron(app.pool, id, data)
        return json({"msg": "ok" if ok else "bad"})

    async def delete(self, request, id):
        ok = await model.delete_patron(app.pool, id)
        return json({"msg": "ok" if ok else "bad"})


@app.listener("before_server_start")
async def db_connect(app, loop):
    app.db = Database("restaurant", owner=False)
    app.pool = await app.db.connect()
    await model.create_table_if_missing(app.pool)
    await app.db.add_listener("chan_patron", model.db_event)


@app.listener("after_server_stop")
async def db_disconnect(app, loop):
    await app.db.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    app.add_route(new_patron, "/patron", methods=["POST"])
    app.add_route(PatronAPI.as_view(), "/patron/<id:int>")
    app.run(host="0.0.0.0", port=args.port)
