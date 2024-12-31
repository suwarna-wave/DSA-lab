def evaluate_postfix(expression):
    stack = []
    operators = set(['+', '-', '*', '/', '^'])

    #tokens for splot
    tokens = expression.split()

    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token in operators:
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression")
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '^':
                result = operand1 ** operand2
            elif token == '/':
                if operand2 == 0:
                    raise ZeroDivisionError("Division by zero")
                result = operand1 / operand2
            stack.append(result)
        else:
            # Ignore invalid tokens spaces error handle gareko
            pass

    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    return stack.pop()

postfix_expression = "12 3 * 4 2 - +"  # Postfix expression with multi-digit handling
try:
    result = evaluate_postfix(postfix_expression)
    print(f"Result: {result}")
except (ValueError, ZeroDivisionError) as e:
    print(f"Error: {e}")
