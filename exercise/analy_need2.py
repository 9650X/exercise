"""
This module checks the answers of arithmetic exercises
read from files. It calculates the results of the expressions
 and compares them with the provided answers. Additionally,
 it profiles the performance of the checking process and
  outputs the profiling results to a file.
"""

import cProfile
import pstats
import fractions


def parse_fraction(fraction_str):
    """
    Parse a fraction string and return a Fraction object.
    """
    fraction_str = fraction_str.strip()
    # 检查是否只包含数字和正斜杠
    if not all(c.isdigit() or c == '/' or c == ' ' for c in fraction_str.replace(' ', '')):
        raise ValueError(f"Cannot parse '{fraction_str}' "
                         f"as a fraction. Contains non-numeric characters.")

    # 处理带分数，如 '1 2/3'
    if ' ' in fraction_str:
        whole_part, fractional_part = fraction_str.split()
        whole = int(whole_part)
        if '/' in fractional_part:
            num, denom = map(int, fractional_part.split('/'))
            return fractions.Fraction(whole, 1) + fractions.Fraction(num, denom)
        else:
            num = int(fractional_part)
            return fractions.Fraction(whole, 1) + fractions.Fraction(num, 1)
    # 处理普通分数，如 '3/4'
    elif '/' in fraction_str:
        num, denom = map(int, fraction_str.split('/'))
        return fractions.Fraction(num, denom)
    # 处理整数
    else:
        return fractions.Fraction(int(fraction_str))

def parse_expression(expression):
    """
    Parse the expression and return operands and operators.
    """
    operands = []
    operators = []
    num_str = ""
    for char in expression:
        if char.isdigit() or char in "’/*-+":
            if char in "*/+-":
                if num_str:
                    try:
                        operands.append(parse_fraction(num_str))
                        num_str = ""
                    except ValueError as e_symbol:
                        print(f"Error parsing fraction '{num_str}'"
                              f" at position {expression.find(num_str)}: {e_symbol}")
                        num_str = ""
                operators.append(char)
            else:
                num_str += char
        else:
            if num_str:
                try:
                    operands.append(parse_fraction(num_str))
                    num_str = ""
                except ValueError as e_symbol:
                    print(f"Error parsing fraction '{num_str}' "
                          f"at position {expression.find(num_str)}: {e_symbol}")
                    num_str = ""
    if num_str:
        try:
            operands.append(parse_fraction(num_str))
        except ValueError as e_symbol:
            print(f"Error parsing fraction '{num_str}' at end of expression: {e_symbol}")
    return operands, operators


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
    except FileNotFoundError:
        print(f"Error: The file was not found.")
        return None, None
    except Exception as e_symbol:
        print(f"An error occurred: {e_symbol}")
        return None, None


def calculate_expression(operands, operators):
    """
    Calculate the result of the expression.
    """
    result = operands[0]
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
        except ValueError:
            wrong.append(idx)
    return correct, wrong


def write_grades(correct, wrong, grade_file):
    """
    Write the grades to a file.
    """
    with open(grade_file, 'w', encoding='utf-8') as f_grade:
        f_grade.write(f"Correct: {len(correct)} ({', '.join(map(str, correct))})\n")
        f_grade.write(f"Wrong: {len(wrong)} ({', '.join(map(str, wrong))})\n")


def main(exercise_file, answer_file, grade_file):
    """
    Main function to check the answers of arithmetic exercises.
    """
    exercises, answers = read_files(exercise_file, answer_file)
    if exercises is not None and answers is not None:
        # 使用cProfile收集性能数据
        profiler = cProfile.Profile()
        profiler.enable()

        correct, wrong = check_answers(exercises, answers)
        write_grades(correct, wrong, grade_file)

        profiler.disable()
        profiler.dump_stats('arithmetic_checking.profile')

        # 分析性能数据并将结果写入文本文件
        stats = pstats.Stats('arithmetic_checking.profile')
        stats.strip_dirs()
        stats.sort_stats('cumulative').print_stats(20)

        # 写入性能分析结果到文件
        with open(r'E:\com\pythonProject\exercise\need2_profile_result.txt', 'w') as file:
            stats.stream = file
            stats.sort_stats('cumulative').print_stats(20)
    else:
        print("Failed to read files.")


if __name__ == "__main__":
    EXERCISE_FILE_PATH = r'E:\com\pythonProject\exercise\Exercises.txt'
    ANSWER_FILE_PATH = r'E:\com\pythonProject\exercise\Answers.txt'
    GRADE_FILE_PATH = r'E:\com\pythonProject\exercise\Grade.txt'
    main(EXERCISE_FILE_PATH, ANSWER_FILE_PATH, GRADE_FILE_PATH)
