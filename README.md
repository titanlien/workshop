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
```

## Run pytest
```ssh
# install test dependencies
make test-deps

# run test
make test
```

## Run with docker-compose
```ssh 
make compose-up
```

## [live demo](https://asciinema.org/a/Ynh9MwBC2fXHoktMx0PouvmQc)

## TODO:
```
1. Create a DB(postgresql) in docker-compose
2. Create an endpoint with graph module
```

## Limitation
```
1. Dut to datetime type, only handle the REST in a second, not less than a second. 
```
