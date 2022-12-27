""" Build tokens for Reverse Polish Notation """

import os

def generateTokens():
    try:
        formula = os.getenv("FORMULA").replace(' ', '')

        if not formula:
            return None, 'FORMULA not provided in module configuration.'

        tokens = []
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
        while formula:
            # found a closing bracket
            if formula[0] == ')':
                while stack[-1] != '(':
                    tokens.append(stack.pop())
                # remove '(' from stack
                stack.pop()
                formula = formula[1:]

            # found opening bracket
            elif formula[0] == '(':
                stack.append(formula[0])
                formula = formula[1:]
                # check for the negative number following the opening bracket
                if formula[0] == '-':
                    negative_number_flag = not negative_number_flag
                    formula = formula[1:]

            # found a number
            elif formula[0].isdigit():
                number_str = ""
                while formula and (formula[0].isdigit() or formula[0] == '.'):
                    number_str += formula[0]
                    formula = formula[1:]
                number = float(number_str)
                if negative_number_flag:
                    number = number * (-1)
                    negative_number_flag = False
                tokens.append(number)

            # found label from data
            elif formula[0] == '{':
                if formula[1] == '{':
                    end_of_label_name = formula.find('}}')
                    if end_of_label_name == -1:
                        return None, 'Missing closing }} in double {{...}} when referring to the data field (label)'
                    else:
                        tokens.append(formula[:end_of_label_name + 2])
                        formula = formula[end_of_label_name + 2:]
                else:
                    return None, 'Missing another { in double {{...}} when referring to the data field (label)'

            # found an operator
            elif formula[0] in list(operators_weights.keys()):
                while stack and operators_weights[formula[0]] <= operators_weights[stack[-1]]:
                    tokens.append(stack.pop())
                stack.append(formula[0])
                formula = formula[1:]

            # found a function
            elif formula[0].isalpha():
                # find function name
                function_name = formula[0]
                formula = formula[1:]
                while formula and formula[0].isalpha():
                    function_name = function_name + formula[0]
                    formula = formula[1:]
                if function_name in supported_functions:
                    stack.append(function_name)
                else:
                    return None, f'Unsupported function [{function_name}]. Please select among supported functions {supported_functions}'

            # # coma from function declaration so skip it
            # elif formula[0] == ',':
            #     formula = formula[1:]

            else:
                return None, f'Unsupported character: {formula[0]}'

        # empty whatever left on stack
        while stack:
            tokens.append(stack.pop())

        return tokens, None

    except Exception as e:
        return None, f"Exception when generating Reverse Polish Notation: {e}. Check if provided formula is correct and has all brackets closed."
