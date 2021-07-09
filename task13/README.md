## Local launch
```ssh
# install python module
make install

# login virtual env
pipenv shell

# execute uvicorn server
make run
```

## Send the long_url to localhost
```ssh
curl -X POST -H 'Content-Type: application/json' -d '{"long_url":"ssh://facebook.com"}' http://localhost:5000/add_url/

{"detail":[{"loc":["body","long_url"],"msg":"Long URL is invalid.","type":"value_error"}]}

curl -X POST -H 'Content-Type: application/json' -d '{"long_url":"https://facebook.com"}' http://localhost:5000/add_url/

{"url":"http://localhost:5000/F487Z6cY"}

curl -X POST -H 'Content-Type: application/json' -d '{"long_url":"https://facebook.com"}' http://localhost:5000/add_url/

{"detail":"URL already created"}⏎
```

## Get statics 
```ssh
curl -XGET -I http://localhost:5000/F487Z6cY

HTTP/1.1 307 Temporary Redirect
date: Mon, 05 Jul 2021 17:22:23 GMT
server: uvicorn
location: http://localhost:5000/F487Z6cY/
Transfer-Encoding: chunked

curl -XGET http://localhost:5000/F487Z6cY/stats | jq

{
  "short_code": "F487Z6cY",
  "id": 3,
  "visit_counter": 0,
  "create_date": "2021-07-05T17:16:29",
  "long_url": "https://facebook.com",
  "last_access_date": null
}

curl -X GET http://localhost:5000/orVPMA6b/graph|jq

[
  "2021-07-08T21:46:10",
  "2021-07-08T21:46:11",
  "2021-07-08T21:46:12"
]
```

## Run pytest
```ssh
# install test dependencies
make test-deps

# run test
make test
find . -name '*.pyc' -delete
rm -f result.xml coverage.xml .coverage test.db sql_app.db
python3 -m pytest -vv --junitxml=result.xml --cov-report term-missing --cov-report xml:coverage.xml --cov=app tests/
=========================================================================================== test session starts ============================================================================================
platform darwin -- Python 3.9.6, pytest-6.2.4, py-1.10.0, pluggy-1.0.0.dev0 -- /Users/titan/.local/share/virtualenvs/short_url-2EiMVsOE/bin/python3
cachedir: .pytest_cache
rootdir: /Users/titan/Documents/Interview/metro.digital/short_url, configfile: pytest.ini
plugins: cov-2.12.1, mock-3.6.1
collected 4 items

tests/test_main.py::test_error_url PASSED                                                                                                                                                            [ 25%]
tests/test_main.py::test_correct_url PASSED                                                                                                                                                          [ 50%]
tests/test_main.py::test_get_stats PASSED                                                                                                                                                            [ 75%]
tests/test_main.py::test_get_graph PASSED                                                                                                                                                            [100%]

--------------------------------------------------------- generated xml file: /Users/titan/Documents/Interview/metro.digital/short_url/result.xml ----------------------------------------------------------

---------- coverage: platform darwin, python 3.9.6-final-0 -----------
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
app/crud.py          29      4    86%   21-23, 31
app/database.py       7      0   100%
app/main.py          49      5    90%   22-26, 75
app/models.py        21      0   100%
app/schemas.py       12      0   100%
-----------------------------------------------
TOTAL               118      9    92%
Coverage XML written to file coverage.xml

============================================================================================ 4 passed in 0.79s =============================================================================================
```

## Run with docker-compose
```ssh 
make compose-up
```

# [Live demo](https://asciinema.org/a/Ynh9MwBC2fXHoktMx0PouvmQc)

## TODO:
```
1. Create a DB(postgresql) in docker-compose
2. Update graph endpoint with graph module
```

## Limitation
```
1. Dut to datetime type, only handle the REST in a second, not less than a second. 
```
