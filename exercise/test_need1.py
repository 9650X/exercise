"""
Unit tests for the arithmetic expressions generation module.
"""

import unittest
from unittest.mock import patch, mock_open
from need1 import generate_and_write_expressions, generate_expressions


class TestArithmeticExpressions(unittest.TestCase):
    """
    Test class for testing arithmetic expressions generation.
    """

    def test_generate_expressions(self):
        """
        Test if generate_expressions function generates correct number of expressions and answers.
        """
        num_expressions = 5
        range_limit = 10
        expressions, answers = generate_expressions(num_expressions, range_limit)

        self.assertEqual(len(expressions), num_expressions)
        self.assertEqual(len(answers), num_expressions)

        for expr, answer in zip(expressions, answers):
            # 这里可以添加更多的断言来检查表达式和答案的正确性
            self.assertIsInstance(expr, str)
            self.assertIsInstance(answer, str)

    @patch('builtins.open', new_callable=mock_open)  # 使用 new_callable 参数正确地使用 mock_open
    def test_generate_and_write_expressions(self, mock_file):
        """
        Test if generate_and_write_expressions function writes to files correctly.
        """
        num_expressions = 5
        range_limit = 10
        generate_and_write_expressions(num_expressions, range_limit)

        # 检查 'exercises.txt' 文件是否被正确打开
        mock_file.assert_any_call(r'E:\com\pythonProject'
                                  r'\exercise\Exercises.txt', 'w', encoding='utf-8')
        # 检查 'answers.txt' 文件是否被正确打开
        mock_file.assert_any_call(r'E:\com\pythonProject'
                                  r'\exercise\Answers.txt', 'w', encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
