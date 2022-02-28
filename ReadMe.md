Start up postgres server w/ `sudo service postgresql start`
Running the API with `uvicorn app.main:app --reload` will look for the main.py file and inspect it for the instance of FastAPI().

[Warning Never, never, NEVER use Python string concatenation (+) or string parameters interpolation (%) to pass variables to a SQL query string. Not even at gunpoint](https://www.psycopg.org/docs/usage.html).

ORM Documentation - [SQL (Relational) Databases - FastAPI | Documentation](https://fastapi.tiangolo.com/tutorial/sql-databases/)

Alembec allows for upgrading of the initial db schema. After installation, running `alembic --help` can proovide some helpful commands.  When we want to introduce a new migration with Alembic we can use `alembic revision -m "message specifying commit"`, but of these the most important is `alembic upgrade <hashID>`, or alternatively `alembic upgrade +i` where `i` is an intger and `alembic downgrade <hashID>`. Also helpful to see which revision we are on is `alembic current`.

`alembic revision --autogenerate -m "some commit message"` allows alembic to create a migration automatically from models.py