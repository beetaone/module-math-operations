"""
This file implements module's main logic.
Data processing should happen here.

Edit this file to implement your module.
"""

import os
import re
import copy
from logging import getLogger
from .tokens import generateTokens
from .calculate import evaluateRPN

log = getLogger("module")

__RESULT_LABEL__ = os.getenv("RESULT_LABEL", "defaultLabel")
__NEW_RESULT__ = os.getenv("NEW_RESULT", "stand-alone")

TOKENS, tokensError = generateTokens()
if tokensError:
    log.error(tokensError)

def calculate(data):
    global TOKENS

    # find labeled data in TOKENS and emplace their values from received_data
    token_copy = copy.deepcopy(TOKENS)

    for i in range(len(token_copy)):
        if type(token_copy[i]) == str and re.search("{{.*?}}", token_copy[i]):
            # its a label so emplace value
            token_copy[i] = data[token_copy[i][2:-2]]

    calc_result, calc_error = evaluateRPN(token_copy)
    if calc_error:
        return None, calc_error

    if __NEW_RESULT__ == "update" or __NEW_RESULT__ == "append":
        data[__RESULT_LABEL__] = calc_result
    elif __NEW_RESULT__ == "stand-alone":
        data = {
            __RESULT_LABEL__: calc_result
        }

    return data, None


def module_main(received_data: any) -> [any, str]:
    """
    Process received data by implementing module's main logic.
    Function description should not be modified.

    Args:
        received_data (any): Data received by module and validated.

    Returns:
        any: Processed data that are ready to be sent to the next module or None if error occurs.
        str: Error message if error occurred, otherwise None.

    """

    log.debug("Processing ...")

    try:
        global TOKENS

        if type(received_data) == list:
            for data in received_data:
                data, calc_error = calculate(data)
                if calc_error:
                    return None, calc_error

        else:
            received_data, calc_error = calculate(received_data)
            if calc_error:
                return None, calc_error

        return received_data, None

    except Exception as e:
        return None, f"Exception in the module business logic: {e}"
