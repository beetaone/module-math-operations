""" Build tokens for Reverse Polish Notation """

import os

def generateTokens():
    try:
        FORMULA = os.getenv("FORMULA").replace(' ', '')

        if not FORMULA:
            return None, 'FORMULA not provided in module configuration.'

        TOKENS = []
        stack = []
        supported_functions = ['ceil', 'abs', 'floor', 'exp', 'sqrt', 'sin', 'cos', 'tan']
        operators_weights = {
            '(': 0,
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2,
            '^': 3,
            'sqrt': 3,
            'exp': 3,
            'ceil': 4,
            'abs': 4,
            'floor': 4,
            'sin': 4,
            'cos': 4,
            'tan': 4,
        }

        negative_number_flag = False

        # forward feed the formula and build RPN representation
        while FORMULA:
            # found a closing bracket
            if FORMULA[0] == ')':
                while stack[-1] != '(':
                    TOKENS.append(stack.pop())
                # remove '(' from stack
                stack.pop()
                FORMULA = FORMULA[1:]

            # found opening bracket
            elif FORMULA[0] == '(':
                stack.append(FORMULA[0])
                FORMULA = FORMULA[1:]
                # check for the negative number following the opening bracket
                if FORMULA[0] == '-':
                    negative_number_flag = True
                    FORMULA = FORMULA[1:]

            # found a number
            elif FORMULA[0].isdigit():
                currNumber = int(FORMULA[0])
                FORMULA = FORMULA[1:]
                decimal = True
                divider = 1
                while FORMULA and (FORMULA[0].isdigit() or FORMULA[0] == '.'):
                    if FORMULA[0].isdigit():
                        currNumber = currNumber * 10 + int(FORMULA[0])
                        if not decimal:
                            divider = divider * 10
                    else:
                        decimal = False
                    FORMULA = FORMULA[1:]
                currNumber = currNumber / divider
                if negative_number_flag:
                    currNumber = currNumber * (-1)
                    negative_number_flag = False
                TOKENS.append(currNumber)

            # found label from data
            elif FORMULA[0] == '{':
                if FORMULA[1] == '{':
                    end_of_label_name = FORMULA.find('}}')
                    if end_of_label_name == -1:
                        return None, 'Missing clossing }} in double {{...}} when referring to the data field (label)'
                    else:
                        TOKENS.append(FORMULA[:end_of_label_name + 2])
                        FORMULA = FORMULA[end_of_label_name + 2:]
                else:
                    return None, 'Missing another { in double {{...}} when referring to the data field (label)'

            # found an operator
            elif FORMULA[0] in list(operators_weights.keys()):
                while stack and operators_weights[FORMULA[0]] <= operators_weights[stack[-1]]:
                    TOKENS.append(stack.pop())
                stack.append(FORMULA[0])
                FORMULA = FORMULA[1:]

            # found a function
            elif FORMULA[0].isalpha():
                # find function name
                function_name = FORMULA[0]
                FORMULA = FORMULA[1:]
                while FORMULA and FORMULA[0].isalpha():
                    function_name = function_name + FORMULA[0]
                    FORMULA = FORMULA[1:]
                if function_name in supported_functions:
                    stack.append(function_name)
                else:
                    return None, f'Unsupported function [{function_name}]. Please select among supported functions {supported_functions}'

            # coma from function declaration so skip it
            elif FORMULA[0] == ',':
                FORMULA = FORMULA[1:]

            else:
                return None, f'Unsupported character: {FORMULA[0]}'

        # empty whatever left on stack
        while stack:
            TOKENS.append(stack.pop())

        return TOKENS, None

    except Exception as e:
        return None, f"Exception when generating Reverse Polish Notation: {e}. Check if provided formula is correct and has all brackets closed."
