
Start up postgres server w/ `sudo service postgresql start` 
Running the API with `uvicorn app.main:app --reload` will look for the main.py file and inspect it for the instance of FastAPI(). 

[Warning Never, never, NEVER use Python string concatenation (+) or string parameters interpolation (%) to pass variables to a SQL query string. Not even at gunpoint](https://www.psycopg.org/docs/usage.html).