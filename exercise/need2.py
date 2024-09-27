"""
Check the answers of arithmetic exercises.
"""

import fractions
import argparse
import re


# 设置命令行参数解析
PARSER = argparse.ArgumentParser(description="Check the answers of arithmetic exercises.")
PARSER.add_argument("-e", "--exercise_file", required=True, help="Path to the exercises file")
PARSER.add_argument("-a", "--answer_file", required=True, help="Path to the answers file")
ARGS = PARSER.parse_args()


def parse_fraction(fraction_str):
    """
    Parse a fraction string and return a Fraction object.
    """
    fraction_str = fraction_str.strip()
    # 处理带分数，如 '1’1/3'
    if '’' in fraction_str:
        whole_part, fractional_part = fraction_str.split('’')
        whole = int(whole_part)
        if '/' in fractional_part:
            num, denom = map(int, fractional_part.split('/'))
            return fractions.Fraction(whole, 1) + fractions.Fraction(num, denom)
        else:
            num = int(fractional_part)
            return fractions.Fraction(whole, 1) + fractions.Fraction(num, 1)
    # 处理普通分数
    elif '/' in fraction_str:
        num, denom = map(int, fraction_str.split('/'))
        return fractions.Fraction(num, denom)
    # 处理整数
    else:
        return fractions.Fraction(int(fraction_str))

def read_files(exercise_file, answer_file):
    """
    Read exercises and answers from the specified files.
    """
    try:
        with open(exercise_file, 'r', encoding='utf-8') as f_ex:
            exercises = f_ex.readlines()
        with open(answer_file, 'r', encoding='utf-8') as f_ans:
            answers = f_ans.readlines()
        return exercises, answers
    except FileNotFoundError as e_symbol:
        print(f"Error: The file was not found - {e_symbol}")
        return None, None
    except Exception as e_symbol:
        print(f"An error occurred: {e_symbol}")
        return None, None


def calculate_expression(operands, operators):
    """
    Calculate the result of the expression.
    """
    # 初始结果为第一个操作数
    result = operands[0]
    # 遍历操作符和后续操作数
    for op_symbol, operand in zip(operators, operands[1:]):
        if op_symbol == '+':
            result += operand
        elif op_symbol == '-':
            result -= operand
        elif op_symbol == '*':
            result *= operand
        elif op_symbol == '/':
            result /= operand
    return result.limit_denominator()



def parse_expression(expression):
    """
    Parse the expression and return operands and operators.
    """
    operands = []
    operators = []
    num_str = ""
    skip_next = False  # 用于跳过操作符后的空格

    for char in expression:
        if skip_next:
            skip_next = False
            continue
        if char.isspace():
            if num_str:  # 如果当前有数字字符串，则记录操作数
                operands.append(parse_fraction(num_str))
                num_str = ""
            continue
        elif char in "*/+-":
            if num_str:  # 如果当前有数字字符串，则记录操作数
                operands.append(parse_fraction(num_str))
                num_str = ""
            operators.append(char)
            skip_next = True  # 跳过操作符后的空格
        elif char in "’":
            if num_str:  # 如果当前有数字字符串，则记录操作数
                operands.append(parse_fraction(num_str))
                num_str = ""
            operators.append(char)  # 添加带分数符号作为操作符
            skip_next = True
        else:
            num_str += char

    if num_str:  # 添加最后一个操作数
        operands.append(parse_fraction(num_str))

    return operands, operators

def check_answers(exercises, answers):
    """
    Check the answers and return the list of correct and wrong answers.
    """
    correct = []
    wrong = []
    for idx, (exercise, answer) in enumerate(zip(exercises, answers), start=1):
        expression = exercise.split('. ')[1].strip()
        operands, operators = parse_expression(expression)
        calculated_result = calculate_expression(operands, operators)
        given_answer_str = answer.split('. ')[1].strip()
        try:
            given_answer = parse_fraction(given_answer_str)
            if calculated_result == given_answer:
                correct.append(idx)
            else:
                wrong.append(idx)
        except ValueError as e_symbol:
            print(f"Error parsing answer '{given_answer_str}': {e_symbol}")
            wrong.append(idx)
    return correct, wrong


def write_grades(correct, wrong, grade_file):
    """
    Write the grades to a file.
    """
    with open(grade_file, 'w', encoding='utf-8') as f_grade:
        f_grade.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f_grade.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def main():
    """
    Main function to check the answers of arithmetic exercises.
    """
    exercise_file = ARGS.exercise_file
    answer_file = ARGS.answer_file
    grade_file = r'E:\com\pythonProject\exercise\Grade.txt'
    exercises, answers = read_files(exercise_file, answer_file)
    correct, wrong = check_answers(exercises, answers)
    write_grades(correct, wrong, grade_file)


if __name__ == "__main__":
    main()
