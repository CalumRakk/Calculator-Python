import unittest
import sys,os

carpeta_raiz = os.getcwd() # guilded_rose
sys.path.append(carpeta_raiz)

from Calculator import operate_expression, getNumberDataType,separator,get_rpn, operate_rpn


def get_expresions():
    with open("test\data.txt", "r") as file:
        while True:
            line= file.readline()
            if "#" in line:
                continue
            elif  line in ["\n",""]:
                break
            expression, result= line.strip().split("=")
            yield  expression, getNumberDataType(result.strip())
class TestCalculator(unittest.TestCase):

    def test_operate_expression(self):
        for line in get_expresions():
            expresion, result= line          
            self.assertEqual(operate_expression(expresion, False), result)

if __name__ == '__main__':
    unittest.main()