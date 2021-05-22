import logging
from typing import List
from datetime import timedelta, datetime

logger = logging.getLogger(__name__)


class Account:
    __available_limit = 0
    __active_card = False
    __transactions = list()
    __violations = list()

    def __init__(self, available_limit: int, active_card: bool) -> None:
        if type(available_limit) is int and available_limit > 0:
            self.__available_limit = available_limit
        else:
            raise ValueError("available_limit must be positive number")

        if type(active_card) is bool:
            self.__active_card = active_card
        else:
            raise TypeError("active_card must be bool")

    def get_violations(self) -> List:
        return self.__violations

    def get_transactions(self) -> List:
        return self.__transactions

    def get_limit(self) -> int:
        return self.__available_limit

    def validate_withdraw_limit(self, amount: int):
        if (self.__available_limit - amount) < 0:
            self.__violations.append("insufficient-limit")

    def check_time_limit(self, final_time: str, first_time: str, limit: int) -> bool:
        time_limit_in_minutes = timedelta(minutes=limit)
        t2 = datetime.fromisoformat(final_time.replace("Z", ""))
        t1 = datetime.fromisoformat(first_time.replace("Z", ""))
        return (t2 - t1) < time_limit_in_minutes

    def validate_withdraw_frequency(self, timestamp: str):
        time_period_minute = 2
        threshold = 2

        check = [
            self.check_time_limit(
                timestamp, self.__transactions[-threshold]["time"], time_period_minute
            )
            for t in self.__transactions
            if t["time"] and len(self.__transactions) > threshold
        ]
        if True in check:
            self.__violations.append("high-frequency-small-interval")

    def validate_doubled_withdraw(self, merchant: str, amount: int, timestamp: str):
        time_period_minute = 2

        check = [
            self.check_time_limit(timestamp, t["time"], time_period_minute)
            for t in self.__transactions
            if ((merchant == t["merchant"]) and (amount == t["amount"]))
        ]

        if True in check:
            self.__violations.append("doubled-transaction")

    def withdraw(self, merchant: str, amount: int, timestamp: str) -> list:
        self.__violations = list()
        # Verify the withdraw against the business rules
        self.validate_withdraw_limit(amount)
        self.validate_withdraw_frequency(timestamp)
        self.validate_doubled_withdraw(merchant, amount, timestamp)

        if len(self.__violations) == 0:
            self.__available_limit -= amount
            t = {"merchant": merchant, "amount": amount, "time": timestamp}
            self.__transactions.append(t)
        logger.info(self.__transactions)
        return self.__violations
