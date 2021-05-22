# Tree

```bash
 tree .
.
├── Dockerfile   # Build base, test and release image
├── Pipfile      # Dependencies library
├── Pipfile.lock # Constrain dependencies library
├── README.md    # Introduce document
├── authorizer   # Main application
│   ├── account.py # bank's account class
│   └── main.py  # Application entry point
├── entrypoint.sh  # Docker container's entry point
├── makefile     # Developer helper command tool
├── operations   # Example input file
└── tests
    └── test_account.py # Unit test for authorizer/account
```

# Local develop

## Install develop python library

```bash
pip3 install pipenv
pipenv install --dev
pipenv shell
```

## Run test

```bash
python -m pytest -m "not integration" -vv --junitxml=result.xml --cov-report term-missing --cov-report xml:coverage.xml --cov=authorizer tests/

# Sample output
=========================================================================================== test session starts ============================================================================================
platform darwin -- Python 3.9.4, pytest-6.2.3, py-1.10.0, pluggy-0.13.1 -- /Users/titan/.local/share/virtualenvs/Nubank-fDMThiVP/bin/python
cachedir: .pytest_cache
rootdir: /Users/titan/Documents/Interview/Nubank
plugins: cov-2.11.1, mock-3.6.0
collected 9 items

tests/test_account.py::test_init_exception PASSED                                                                                                                                                    [ 11%]
tests/test_account.py::test_init_account PASSED                                                                                                                                                      [ 22%]
tests/test_account.py::test_validate_withdraw_limit PASSED                                                                                                                                           [ 33%]
tests/test_account.py::test_check_time_limit_pass PASSED                                                                                                                                             [ 44%]
tests/test_account.py::test_check_time_limit_fail PASSED                                                                                                                                             [ 55%]
tests/test_account.py::test_withdraw_pass PASSED                                                                                                                                                     [ 66%]
tests/test_account.py::test_validate_doubled_withdraw_fail PASSED                                                                                                                                    [ 77%]
tests/test_account.py::test_validate_doubled_withdraw_pass PASSED                                                                                                                                    [ 88%]
tests/test_account.py::test_validate_withdraw_frequency_pass PASSED                                                                                                                                  [100%]

------------------------------------------------------------------ generated xml file: /Users/titan/Documents/Interview/Nubank/result.xml ------------------------------------------------------------------

---------- coverage: platform darwin, python 3.9.4-final-0 -----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
authorizer/account.py      52      0   100%
authorizer/main.py         40     40     0%   3-68
-----------------------------------------------------
TOTAL                      92     40    57%
Coverage XML written to file coverage.xml
```

## Build docker image

### Because we merged test stage in our multipl-stage build, if it failed in docker build process. Please also check the tests/ directory.

```bash
docker build -t authorizer .

# Sample output
 docker build -t authorizer
[+] Building 2.5s (12/12) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                                   0.0s
 => => transferring dockerfile: 562B                                                                                                                                                                   0.0s
 => [internal] load .dockerignore                                                                                                                                                                      0.0s
 => => transferring context: 2B                                                                                                                                                                        0.0s
 => [internal] load metadata for docker.io/library/python:3.9.4-slim                                                                                                                                   1.3s
 => [internal] load build context                                                                                                                                                                      0.0s
 => => transferring context: 20.00kB                                                                                                                                                                   0.0s
 => [base 1/5] FROM docker.io/library/python:3.9.4-slim@sha256:bca2bcc8afda3abca3f73ff3d9ac146076aa47d09a226290eb3c99f175b1371a                                                                        0.0s
 => CACHED [base 2/5] RUN pip install pipenv                                                                                                                                                           0.0s
 => CACHED [base 3/5] WORKDIR /authorizer                                                                                                                                                              0.0s
 => [base 4/5] COPY Pipfile Pipfile.lock ./                                                                                                                                                            0.0s
 => [base 5/5] RUN pipenv install --system                                                                                                                                                             0.9s
 => [release 1/2] COPY authorizer ./authorizer                                                                                                                                                         0.0s
 => [release 2/2] COPY entrypoint.sh operations ./                                                                                                                                                     0.0s
 => exporting to image                                                                                                                                                                                 0.1s
 => => exporting layers                                                                                                                                                                                0.0s
 => => writing image sha256:26e5df619e3ff538784a2c0909c32d3412746efe85a73707237176bf2d80d691                                                                                                           0.0s
 => => naming to docker.io/library/authorizer                                                                                                                                                          0.0s
```

## Docker run

```bash
# Production run
 docker run --rm -e LOG_LEVEL=WARN authorizer
{"account": {"active-card": false, "available-limit": 0}, "violations": ["account-not-initialized"]}
{"account": {"active-card": true, "available-limit": 120}, "violations": []}
{"account": {"active-card": true, "available-limit": 100}, "violations": []}
{"account": {"active-card": true, "available-limit": 100}, "violations": ["doubled-transaction"]}
{"account": {"active-card": true, "available-limit": 80}, "violations": []}
{"account": {"active-card": true, "available-limit": 60}, "violations": []}
{"account": {"active-card": true, "available-limit": 60}, "violations": ["insufficient-limit", "high-frequency-small-interval"]}
{"account": {"active-card": true, "available-limit": 40}, "violations": []}

# Develop run
 docker run --rm -e LOG_LEVEL=DEBUG authorizer
DEBUG:__main__:{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}

DEBUG:__main__:{"account": {"active-card": true, "available-limit": 120}}

DEBUG:__main__:{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:00.000Z"}}

INFO:account:[{'merchant': 'Burger King', 'amount': 20, 'time': '2019-02-13T10:00:00.000Z'}]
DEBUG:__main__:{"transaction": {"merchant": "Burger King", "amount": 20, "time": "2019-02-13T10:00:10.000Z"}}

INFO:account:[{'merchant': 'Burger King', 'amount': 20, 'time': '2019-02-13T10:00:00.000Z'}]
DEBUG:__main__:{"transaction": {"merchant": "Starbucks", "amount": 20, "time": "2019-02-13T10:00:20.000Z"}}

INFO:account:[{'merchant': 'Burger King', 'amount': 20, 'time': '2019-02-13T10:00:00.000Z'}, {'merchant': 'Starbucks', 'amount': 20, 'time': '2019-02-13T10:00:20.000Z'}]
DEBUG:__main__:{"transaction": {"merchant": "Pizza hot", "amount": 20, "time": "2019-02-13T10:00:20.000Z"}}

INFO:account:[{'merchant': 'Burger King', 'amount': 20, 'time': '2019-02-13T10:00:00.000Z'}, {'merchant': 'Starbucks', 'amount': 20, 'time': '2019-02-13T10:00:20.000Z'}, {'merchant': 'Pizza hot', 'amount': 20, 'time': '2019-02-13T10:00:20.000Z'}]
DEBUG:__main__:{"transaction": {"merchant": "KFC", "amount": 90, "time": "2019-02-13T10:00:30.000Z"}}

INFO:account:[{'merchant': 'Burger King', 'amount': 20, 'time': '2019-02-13T10:00:00.000Z'}, {'merchant': 'Starbucks', 'amount': 20, 'time': '2019-02-13T10:00:20.000Z'}, {'merchant': 'Pizza hot', 'amount': 20, 'time': '2019-02-13T10:00:20.000Z'}]
DEBUG:__main__:{"transaction": {"merchant": "Habbib's", "amount": 20, "time": "2019-02-13T11:00:00.000Z"}}

INFO:account:[{'merchant': 'Burger King', 'amount': 20, 'time': '2019-02-13T10:00:00.000Z'}, {'merchant': 'Starbucks', 'amount': 20, 'time': '2019-02-13T10:00:20.000Z'}, {'merchant': 'Pizza hot', 'amount': 20, 'time': '2019-02-13T10:00:20.000Z'}, {'merchant': "Habbib's", 'amount': 20, 'time': '2019-02-13T11:00:00.000Z'}]
{"account": {"active-card": false, "available-limit": 0}, "violations": ["account-not-initialized"]}
{"account": {"active-card": true, "available-limit": 120}, "violations": []}
{"account": {"active-card": true, "available-limit": 100}, "violations": []}
{"account": {"active-card": true, "available-limit": 100}, "violations": ["doubled-transaction"]}
{"account": {"active-card": true, "available-limit": 80}, "violations": []}
{"account": {"active-card": true, "available-limit": 60}, "violations": []}
{"account": {"active-card": true, "available-limit": 60}, "violations": ["insufficient-limit", "high-frequency-small-interval"]}
{"account": {"active-card": true, "available-limit": 40}, "violations": []}
```

## Develop via make (optional)

- Install make command

```bash
# Install python dependency library
make install

# Run unit test
make test

# Build up docker image
make build

# Production Run
make run

# Clean up
make clean

# Cleanup and remove virtual environment
make dist-clean
```

# Live demo:
https://asciinema.org/a/LDw6mZpFM6hO7oJMSZhIPfvLh

# TODO:

1. Increase test coverage on authorizer/main.py
1. Create CICD pipeline to build up docker image
