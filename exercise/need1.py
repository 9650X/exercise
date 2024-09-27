import random
import fractions
import argparse

# 初始化argparse对象
PARSER = argparse.ArgumentParser(description='Generate arithmetic expressions and answers.')
# 添加-n参数，设置为必须
PARSER.add_argument('-n', type=int, required=True, help='Number of expressions to generate')
# 添加-r参数，设置为必须
PARSER.add_argument('-r', type=int, required=True, help='Range limit for numbers in expressions')

# 解析命令行参数
ARGS = PARSER.parse_args()

# 生成自然数或真分数
def generate_number(range_limit):
    """Generate a random natural number or a true fraction."""
    return random.randint(1, range_limit - 1) \
        if random.random() > 0.5 else generate_true_fraction(range_limit)

# 生成真分数
def generate_true_fraction(range_limit):
    """Generate a true fraction."""
    numerator = random.randint(1, range_limit - 1)
    denominator = random.randint(2, range_limit)  # 避免分母为1
    return fractions.Fraction(numerator, denominator)

# 随机选择运算符
def generate_operator(allow_subtract=False, allow_divide=False):
    """Randomly select an operator."""
    operators = ['+', '*']
    if allow_subtract:
        operators.append('-')
    if allow_divide:
        operators.append('/')
    return random.choice(operators)

# 生成算术表达式
def generate_expression(range_limit, num_operators):
    """Generate an arithmetic expression."""
    operands = [generate_number(range_limit) for _ in range(num_operators + 1)]
    operators = [generate_operator(allow_subtract=True, allow_divide=True) for _ in range(num_operators)]

    # 确保结果非负
    while True:
        result = calculate_expression(operands, operators)
        if result >= 0:
            break
        operands = [generate_number(range_limit) for _ in range(num_operators + 1)]
        operators = [generate_operator(allow_subtract=True, allow_divide=True) for _ in range(num_operators)]

    # 创建表达式字符串，并在需要的地方添加括号
    expression = f"{format_number(operands[0])} "
    for op_symbol, operand in zip(operators, operands[1:]):
        if op_symbol in ['-', '/']:
            expression += f" {op_symbol} ({format_number(operand)})"
        else:
            expression += f" {op_symbol} {format_number(operand)}"
    return expression, format_number(result)

# 格式化数字
def format_number(number):
    """Format the number as a string."""
    if isinstance(number, fractions.Fraction):
        if number.numerator == 0:
            return "0"
        elif number.denominator == 1:
            return str(number.numerator)
        elif number < 1:  # 真分数
            return f"{number.numerator}/{number.denominator}"
        else:  # 带分数
            whole_number = int(number)
            fractional_part = number - whole_number
            numerator = int(fractional_part * number.denominator)
            return f"{whole_number}’{numerator}/{number.denominator}"
    else:
        return str(number)

# 计算表达式的结果
def calculate_expression(operands, operators):
    """Calculate the result of the expression."""
    result = operands[0]
    for op_symbol, operand in zip(operators, operands[1:]):
        if op_symbol == '+':
            result += operand
        elif op_symbol == '-':
            result -= operand
        elif op_symbol == '*':
            result *= operand
        elif op_symbol == '/':
            result = result / operand
    return result

def generate_expressions(num_expressions, range_limit):
    """Generate a list of arithmetic expressions and their answers."""
    expressions = []
    answers = []
    for _ in range(num_expressions):
        num_operators = random.randint(1, 3)  # 限制运算符数量
        while True:
            expr, answer = generate_expression(range_limit, num_operators)
            if not contains_negative_result(expr):
                expressions.append(expr)
                answers.append(answer)
                break
    return expressions, answers

def contains_negative_result(expression):
    """Check if the expression contains a negative result."""
    operands = []
    operators = []
    num_str = ""
    for char in expression:
        if char.isdigit() or char in "*/+-":
            if char in "*/+-":
                if num_str:
                    operands.append(fractions.Fraction(num_str))
                    num_str = ""
                operators.append(char)
            else:
                num_str += char
    if num_str:  # 添加最后一个操作数
        operands.append(fractions.Fraction(num_str))

    result = calculate_expression(operands, operators)
    return result < 0

def generate_and_write_expressions(num_expressions, range_limit):
    """Generate and write expressions and answers to files."""
    expressions, answers = generate_expressions(num_expressions, range_limit)
    with open('Exercises.txt', 'w', encoding='utf-8') as f_ex:
        for i, expr in enumerate(expressions, start=1):
            f_ex.write(f"{i}. {expr}\n")
    with open('Answers.txt', 'w', encoding='utf-8') as f_ans:
        for i, answer in enumerate(answers, start=1):
            f_ans.write(f"{i}. {answer}\n")
    return expressions, answers

def main():
    """Main function to generate and write expressions."""
    num_expressions = ARGS.n
    range_limit = ARGS.r
    generate_and_write_expressions(num_expressions, range_limit)

if __name__ == "__main__":
    main()
