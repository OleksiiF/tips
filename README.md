# Tips
Tips is a little tool to help you to get some tips (how unexpectedly) from the search form of the famous site.

### Tech
Tips uses a number of open source projects to work properly:
* [httpx](https://github.com/encode/httpx/) - HTTPX is a fully featured HTTP client for Python 3, which provides sync and async APIs, and support for both HTTP/1.1 and HTTP/2.
* [aiofiles](https://github.com/Tinche/aiofiles) - aiofiles is an Apache2 licensed library, for handling local disk files in asyncio applications.
* [orm](https://github.com/encode/orm) - The orm package is an async ORM for Python.
* [fake-useragent](https://github.com/hellysmile/fake-useragent) - Provide user agents.
* [databases](https://github.com/encode/databases) - Databases gives you simple asyncio support for a range of databases.
* [aiosqlite](https://github.com/jreese/aiosqlite) - AsyncIO bridge to the standard sqlite3 module for Python 3.5+.
* [SQLite](https://www.sqlite.org/) - Light weight database.

### Installation
Tips requires [Python 3.8](https://www.python.org/downloads/) to run.
 Create virtual environment. Install the dependencies.
```sh
$ python3.8 -m venv name_of_your_env_here
$ source name_of_your_env_here/bin/activate
$ pip install -r requirements.txt
```

Also, you can use your own proxies. Just put the file (use the options.py to choose properly filename and format of content) with its near the main.py.
### Run
```sh
$ python3 main.py
```
Just wait until the work is completed. During operation, a database will be created with the received information and an error log (if necessary).