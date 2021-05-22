#!/usr/bin/env python3

import json, os, fileinput
import logging

from account import Account

# Debug
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO").upper())
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Init account
    account = None
    active_card = False
    available_limit = 0

    # Init transaction
    merchant = ""
    amount = 0
    time = ""
    violations = list()

    for line in fileinput.input():
        logger.debug(line)
        json_data = json.loads(line)

        oper = list(json_data.keys())[0]

        if oper == "account":
            if account is None:
                # Create a new account
                active_card = json_data[oper]["active-card"]
                available_limit = json_data[oper]["available-limit"]
                account = Account(available_limit, active_card)
            else:
                violations.append("account-already-initialized")

        elif oper == "transaction":
            if account is None:
                violations.append("account-not-initialized")
            elif active_card is False:
                violations.append("card-not-active")
            else:
                merchant = json_data[oper]["merchant"]
                amount = json_data[oper]["amount"]
                time = json_data[oper]["time"]

        # Perform transcation
        if oper == "transaction" and len(violations) == 0:
            response = account.withdraw(merchant, amount, time)

            if len(response) > 0:
                [violations.append(r) for r in response]

            available_limit = account.get_limit()

        # Output transaction retsult
        output_data = {
            "account": {"active-card": active_card, "available-limit": available_limit},
            "violations": violations,
        }

        output_json = json.dumps(output_data)

        print(output_json)

        violations = list()
