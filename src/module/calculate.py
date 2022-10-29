""" Solve Reverse Polish Notation """

import math

single_argument_functions = ["ceil", "fabs", "floor", "exp", "sqrt", "sin", "cos", "tan"]

operations_mapping = {
    "+": (lambda a, b: a + b),
    "-": (lambda a, b: a - b),
    "*": (lambda a, b: a * b),
    "/": (lambda a, b: a / 1e-16 if b == 0 else a / b), # divide by epsilon, standard approach in data science and machine learning to handle division by zero
    "ceil": math.ceil,
    "fabs": math.fabs,
    "floor": math.floor,
    "pow": math.pow,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "log": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "mod": math.fmod
}

def evaluateRVN(RVN):
    try:
        stack = []

        # iterating Reversed Polish Notation
        for element in RVN:
            # element is a number
            if element not in list(operations_mapping.keys()):
                stack.append(int(element))

            # element is an operator
            else:
                if element in single_argument_functions:
                    # getting operands
                    rhs = stack.pop()
                    # perform operation
                    stack.append(operations_mapping[element](rhs))
                else:
                    # getting operands
                    rhs = stack.pop()
                    lhs = stack.pop()
                    # perform operation
                    stack.append(operations_mapping[element](lhs, rhs))

        # return final solution
        return stack.pop()

    except Exception as e:
        return None, f"Exception when evaluating Reverse Polish Notation: {e}"
