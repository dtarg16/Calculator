import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from calculation.nsp import NumericStringParser
from .models import Calculation
import operator


def custom_evaluate(expression):
    def apply_operator(operators, values):
        op = operators.pop()
        if op == operator.truediv and values[-1] == 0:
            raise ValueError("Division by zero")
        if op in [abs, len]:
            val = values.pop()
            values.append(op(val))
        else:
            right = values.pop()
            left = values.pop()
            values.append(op(left, right))

    def evaluate(tokens):
        operators = []
        values = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'abs': 3, 'len': 3}
        ops_map = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv, '(': '(', ')': ')'}

        for token in tokens:
            if token.isdigit():
                values.append(int(token))
            elif token in ['abs', 'len']:
                operators.append(token)
            elif token in ops_map:
                while operators and operators[-1] in precedence and precedence[operators[-1]] >= precedence[token]:
                    apply_operator(operators, values)
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()  # Remove '('

        while operators:
            apply_operator(operators, values)

        return values[0]

    expression = re.sub(r'len\((\d+)\)', lambda x: str(len(x.group(1))), expression)
    expression = re.sub(r'abs\((\d+)\)', lambda x: str(abs(int(x.group(1)))), expression)

    tokens = re.findall(r'\b\d+\b|\babs\b|\blen\b|[()+\-*/]', expression)

    if tokens.count('(') != tokens.count(')'):
        raise ValueError("Unbalanced parentheses")

    try:
        return evaluate(tokens)
    except ZeroDivisionError:
        raise ValueError("Division by zero in expression")
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


@api_view(['POST'])
def evaluate(request):
    expression = request.data.get('expression')
    if not expression:
        return Response({'error': 'No expression provided'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        # result = custom_evaluate(expression)
        nsp = NumericStringParser()
        result = nsp.eval(expression)

        if request.user.is_authenticated:
            Calculation.objects.create(
                expression=expression,
                result=result,
                user=request.user)
        return Response({'result': result}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Invalid expression'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def history(request):
    if request.user.is_authenticated:
        calculations = Calculation.objects.filter(user=request.user).order_by('-created_at')
        data = [{'expression': c.expression, 'result': c.result, 'created_at': c.created_at} for c in calculations]
        return Response(data, status=status.HTTP_200_OK)
    return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
