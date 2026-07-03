# Cache Invalidation Case

1. Each app instance has an in-memory cache of DB queries.
2. When one writes new data to the database, the database alerts all of the connected app instances of the new data.
3. Each app instance then updates its internal cache accordingly.

This case study will highlight how PostgreSQL, with its built-in support for event updates
via the LISTEN and NOTIFY commands, can simply tell us when its data has changed.

asyncpg already has support for the LISTEN/NOTIFY API. This feature of PostgreSQL allows your app
to subscribe to events on a named channel and to post events to named channels. PostgreSQL can
almost become a lighter version of RabbitMQ or ActiveMQ!
