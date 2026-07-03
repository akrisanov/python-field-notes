import logging
from json import loads, dumps
from triggers import create_notify_trigger, add_table_triggers
from boltons.cacheutils import LRU

logger = logging.getLogger("perf")
CREATE_TABLE = (
    "CREATE TABLE IF NOT EXISTS patron("
    "id serial PRIMARY KEY, name text, "
    "fav_dish text)"
)
INSERT = "INSERT INTO patron(name, fav_dish) " "VALUES ($1, $2) RETURNING id"
SELECT = "SELECT * FROM patron WHERE id = $1"
UPDATE = "UPDATE patron SET name=$1, fav_dish=$2 WHERE id=$3"
DELETE = "DELETE FROM patron WHERE id=$1"
EXISTS = "SELECT to_regclass('patron')"
CACHE = LRU(max_size=65536)


async def add_patron(conn, data: dict) -> int:
    return await conn.fetchval(INSERT, data["name"], data["fav_dish"])


async def update_patron(conn, id: int, data: dict) -> bool:
    result = await conn.execute(UPDATE, data["name"], data["fav_dish"], id)
    return result == "UPDATE 1"


async def delete_patron(conn, id: int):
    result = await conn.execute(DELETE, id)
    return result == "DELETE 1"


async def get_patron(conn, id: int) -> dict:
    if id not in CACHE:
        logger.info(f"id={id} Cache miss")
        record = await conn.fetchrow(SELECT, id)
        CACHE[id] = record and dict(record.items())
    return CACHE[id]


def db_event(conn, pid, channel, payload):
    """The callback that asyncpg will make when there are events on our DB notification channel."""
    event = loads(payload)
    logger.info("Got DB event:\n" + dumps(event, indent=4))

    id = event["id"]

    # Update cache when the database notifies about any change in the table.
    if event["type"] == "INSERT":
        CACHE[id] = event["data"]
    elif event["type"] == "UPDATE":
        CACHE[id] = event["data"]["new"]  # cache new data
    elif event["type"] == "DELETE":
        CACHE[id] = None


async def create_table_if_missing(conn):
    if not await conn.fetchval(EXISTS):
        await conn.fetchval(CREATE_TABLE)
        await create_notify_trigger(conn, channel="chan_patron")
        await add_table_triggers(conn, table="patron")
