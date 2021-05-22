import pytest

from authorizer.account import Account

transactions = list()


@pytest.fixture
def test_account():
    return Account(100, True)


def test_init_exception():
    with pytest.raises(ValueError):
        Account(-10, True)
    with pytest.raises(TypeError):
        Account(10, "True")


def test_init_account(test_account):
    assert test_account.get_limit() == 100


def test_validate_withdraw_limit(test_account):

    test_account.validate_withdraw_limit(20)

    assert test_account.get_violations() == []

    test_account.validate_withdraw_limit(120)

    assert test_account.get_violations() == ["insufficient-limit"]


def test_check_time_limit_pass(test_account):
    t2 = "2019-02-13T10:05:00.000Z"
    t1 = "2019-02-13T10:00:00.000Z"
    time_period = 2
    assert test_account.check_time_limit(t2, t1, time_period) == False


def test_check_time_limit_fail(test_account):
    t2 = "2019-02-13T10:00:30.000Z"
    t1 = "2019-02-13T10:00:00.000Z"
    time_period = 2

    assert test_account.check_time_limit(t2, t1, time_period) == True


def test_withdraw_pass(test_account):
    merchant = "unit_tester 1"
    amount = 20
    timestamp = "2019-02-13T10:00:00.000Z"
    t = {"merchant": merchant, "amount": amount, "time": timestamp}
    transactions.append(t)

    assert test_account.withdraw(merchant, amount, timestamp) == []


def test_validate_doubled_withdraw_fail(test_account):
    merchant = transactions[-1]["merchant"]
    amount = transactions[-1]["amount"]
    timestamp = transactions[-1]["time"]

    assert test_account.withdraw(merchant, amount, timestamp) == ["doubled-transaction"]


def test_validate_doubled_withdraw_pass(test_account):
    merchant = "unit_tester 2"
    amount = 10
    timestamp = "2019-02-13T10:00:30.000Z"
    t = {"merchant": merchant, "amount": amount, "time": timestamp}
    transactions.append(t)

    assert test_account.withdraw(merchant, amount, timestamp) == []


def test_validate_withdraw_frequency_pass(test_account):
    merchant = "unit_tester 3"
    amount = 10
    timestamp = "2019-02-13T10:00:50.000Z"
    t = {"merchant": merchant, "amount": amount, "time": timestamp}
    transactions.append(t)

    assert test_account.withdraw(merchant, amount, timestamp) == []

    merchant = "unit_tester 2"
    amount = 5
    timestamp = "2019-02-13T10:01:00.000Z"

    assert len(test_account.get_transactions()) == 3
    assert test_account.withdraw(merchant, amount, timestamp) == [
        "high-frequency-small-interval"
    ]
