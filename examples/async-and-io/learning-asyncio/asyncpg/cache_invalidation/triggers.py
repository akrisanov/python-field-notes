from asyncpg.connection import Connection


async def create_notify_trigger(
    conn: Connection,
    trigger_name: str = "table_update_notify",
    channel: str = "table_change",
) -> None:
    await conn.execute("CREATE EXTENSION IF NOT EXISTS hstore")
    await conn.execute(
        SQL_CREATE_TRIGGER.format(trigger_name=trigger_name, channel=channel)
    )


async def add_table_triggers(
    conn: Connection,
    table: str,
    trigger_name: str = "table_update_notify",
    schema: str = "public",
) -> None:
    templates = (SQL_TABLE_INSERT, SQL_TABLE_UPDATE, SQL_TABLE_DELETE)

    for template in templates:
        await conn.execute(
            template.format(table=table, trigger_name=trigger_name, schema=schema)
        )


SQL_CREATE_TRIGGER = """\
CREATE OR REPLACE FUNCTION {trigger_name}()
  RETURNS trigger AS $$
DECLARE
  id integer; -- or uuid
  data json;
BEGIN
  data = json 'null';
  IF TG_OP = 'INSERT' THEN
id = NEW.id;
    data = row_to_json(NEW);
  ELSIF TG_OP = 'UPDATE' THEN
    id = NEW.id;
    data = json_build_object(
      'old', row_to_json(OLD),
      'new', row_to_json(NEW),
      'diff', hstore_to_json(hstore(NEW) - hstore(OLD))
); ELSE
id = OLD.id;
    data = row_to_json(OLD);
  END IF;
  PERFORM
    pg_notify(
      '{channel}',
      json_build_object(
        'table', TG_TABLE_NAME,
        'id', id,
        'type', TG_OP,
        'data', data
)::text );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""

SQL_TABLE_UPDATE = """\ DROP TRIGGER IF EXISTS
  {table}_notify_update ON {schema}.{table};
CREATE TRIGGER {table}_notify_update
  AFTER UPDATE ON {schema}.{table}
    FOR EACH ROW
      EXECUTE PROCEDURE {trigger_name}();
"""


SQL_TABLE_INSERT = """\ DROP TRIGGER IF EXISTS
  {table}_notify_insert ON {schema}.{table};
CREATE TRIGGER {table}_notify_insert
  AFTER INSERT ON {schema}.{table}
    FOR EACH ROW
      EXECUTE PROCEDURE {trigger_name}();
"""

SQL_TABLE_DELETE = """\ DROP TRIGGER IF EXISTS
  {table}_notify_delete ON {schema}.{table};
CREATE TRIGGER {table}_notify_delete
  AFTER DELETE ON {schema}.{table}
    FOR EACH ROW
      EXECUTE PROCEDURE {trigger_name}();
"""
