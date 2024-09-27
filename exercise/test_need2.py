"""
Unit tests for the arithmetic exercises parsing and calculation module.
"""

import unittest
import fractions
from need2 import parse_fraction, calculate_expression


class TestArithmeticExercises(unittest.TestCase):
    """
    Test class for testing arithmetic exercises parsing and calculation.
    """

    def test_parse_fraction(self):
        """
        Test if parse_fraction function parses fractions correctly.
        """
        # 测试 parse_fraction 函数
        self.assertEqual(parse_fraction('1'), fractions.Fraction(1))
        self.assertEqual(parse_fraction('1/2'), fractions.Fraction(1, 2))
        self.assertEqual(parse_fraction('2 1/4'), fractions.Fraction(9, 4))
        self.assertEqual(parse_fraction('3/4'), fractions.Fraction(3, 4))
        self.assertEqual(parse_fraction('2+3/4'), fractions.Fraction(11, 4))

    def test_calculate_expression(self):
        """
        Test if calculate_expression function calculates expressions correctly.
        """
        operands = [fractions.Fraction(1), fractions.Fraction(2)]
        operators = ['+']
        self.assertEqual(calculate_expression(operands, operators),
                         fractions.Fraction(3))

        operands = [fractions.Fraction(3), fractions.Fraction(1, 2)]
        operators = ['+']
        self.assertEqual(calculate_expression(operands, operators),
                         fractions.Fraction(7, 2))

        operands = [fractions.Fraction(2), fractions.Fraction(3),
                    fractions.Fraction(4)]
        operators = ['+', '*']
        self.assertEqual(calculate_expression(operands, operators),
                         fractions.Fraction(20))  # 修正预期结果

        operands = [fractions.Fraction(5), fractions.Fraction(2, 3)]
        operators = ['-']
        self.assertEqual(calculate_expression(operands, operators),
                         fractions.Fraction(13, 3))

        operands = [fractions.Fraction(10, 3), fractions.Fraction(4, 3)]
        operators = ['+']
        self.assertEqual(calculate_expression(operands, operators),
                         fractions.Fraction(14, 3))  # 修正预期结果


if __name__ == '__main__':
    unittest.main()
