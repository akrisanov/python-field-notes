# Essential SQLAlchemy

## Resources

- [Docs](https://docs.sqlalchemy.org/en/14/)
- [The Architecture of Open Source Applications](http://www.aosabook.org/en/sqlalchemy.html)
- [Talks](https://www.sqlalchemy.org/library.html#talks)
- [Awesome SQLAlchemy](https://github.com/dahlia/awesome-sqlalchemy)

## Core

- Use the `first` method for getting a single record over both the `fetchone` and `scalar` methods,
  because it is clearer to our fellow coders.
- Use the iterable version of the `ResultProxy` over the `fetchall` and `fetchone` methods.
  It is more memory efficient and we tend to operate on the data one record at a time.
- Avoid the `fetchone` method, as it leaves connections open if you are not careful.
- Use the `scalar` method sparingly, as it raises errors if a query ever returns more than one row
  with one column, which often gets missed during testing.

## ORM

When we use a query to get an object, we get back an object that is connected to a
session. That object could move through several states in relationship to the session.

There are four possible states for data object instances:

- `Transient` — The instance is not in session, and is not in the database.
- `Pending` — The instance has been added to the session with `add()`, but hasn't been flushed or committed.
- `Persistent` — The object in session has a corresponding record in the database.
- `Detached` — The instance is no longer connected to the session, but has a record in the database.

To get an object into the detached state, we want to call the `expunge()` method on the session.
You might do this if you are moving data from one session to another. One case in which you might
want to move data from one session to another is when you are archiving or consolidating data from
your primary database to your data warehouse:

```python
session.expunge(obj)
```

### Fetching objects

- Use the iterable version of the query over the `all()` method. It is more memory efficient than
  handling a full list of objects and we tend to operate on the data one record at a time anyway.
- To get a single record, use the `first()` method (rather than `one()` or `scalar()`) because it
  is clearer to our fellow coders. The only exception to this is when you must ensure that there
  is one and only one result from a query; in that case, use `one()`.
- Use the `scalar()` method sparingly, as it raises errors if a query ever returns more than one
  row with one column. In a query that selects entire records, it will return the entire record
  object, which can be confusing and cause errors.

### Exceptions

[Official Documentation](http://docs.sqlalchemy.org/en/latest/orm/exceptions.html)

- `MultipleResultsFound` — occurs when we use the `.one()` query method, but get more than one result back.
- `NoResultFound` — occurs when we used the `.one()` method and the query returned no results.
- `DetachedInstanceError` — attempt to access an attribute on an instance that needs to be loaded
  from the database, but the instance we are using is not currently attached to the database.
- `ObjectDeletedError`
- `StaleDataError`
- `ConcurrentModificationError`

### Reflection

Reflection via [automap](https://docs.sqlalchemy.org/en/14/orm/extensions/automap.html#specifying-classes-explcitly)
is a very useful tool; however, as of version 1.0 of SQLAlchemy we cannot reflect `CheckConstraints`,
comments, or triggers. You also can't reflect client-side defaults or an association between
a sequence and a column. However, it is possible to add them manually.

Automap can automatically reflect and establish many-to-one, one-to-many, and
many-to-many relationships.

## Alembic

SQLAlchemy will only create missing tables when we use the metadata’s `create_all` method,
it doesn’t update the database tables to match any changes we might make to the columns.
Nor would it delete tables that we removed from the code.

- The `env.py` file is used by Alembic to define and instantiate a SQLAlchemy engine,
  connect to that engine, and start a transaction, and calls the migration engine properly when
  you run an Alembic command.
- The `script.py.mako` template is used when creating a migration, and it defines
  the basic structure of a migration.

So when we run the autogeneration command, Alembic inspects the metadata of our SQLAlchemy Base
and then compares that to the current database state.

### Commands

```shell
alembic current

alembic history

alemibc upgrade head

alembic downgrade 34044511331

alembic stamp 2e6a6cc63e9 # skips applying the 34044511331 migration

alembic upgrade 34044511331:2e6a6cc63e9 --sql > migration.sql
```

### Schema changes that autogenerate can detect

- `Table` — Additions and removals
- `Column` — Additions, removals, change of nullable status on columns
- `Index` — Basic changes in indexes and explicitly named unique constraints,
  support for autogenerate of indexes and unique constraints
- `Keys` — Basic renames

### Schema changes that autogenerate cannot detect

- `Tables` — Name changes
- `Column` — Name changes
- `Constraints` — Constraints without an explicit name
- `Types` — Types like ENUM that aren’t directly supported on a database backend

### Alembic operations

While Alembic supports all the operations in the following table,
they are not supported on every backend database:

- `add_column` — Adds a new column
- `alter_column` — Changes a column type, server default, or name
- `create_check_constraint` — Adds a new CheckConstraint
- `create_foreign_key` — Adds a new ForeignKey
- `create_index Adds` — a new Index
- `create_primary_key` — Adds a new PrimaryKey
- `create_table` — Adds a new table
- `create_unique_constraint` — Adds a new UniqueConstraint
- `drop_column` — Removes a column
- `drop_constraint` — Removes a constraint
- `drop_index` — Drops an index
- `drop_table` — Drops a table
- `execute` — Run a raw SQL statement
- `rename_table` — Renames a table

## Packages

- [sqlacodegen](https://github.com/agronholm/sqlacodegen)

  ```shell
  sqlacodegen sqlite:///Chinook.sqlite
  sqlacodegen sqlite:///Chinook.sqlite --tables Artist,Track > db.py
  ```
