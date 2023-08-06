import unittest
import calc_ev_115
calc = calc_ev_115.Calculator()
#all i getting is error that the expected input was none but 1 is given :(((

class TestCalculator(unittest.TestCase):
    def test_reset(self):
        self.assertTrue(calc.reset() == 0)

    def test_add(self):
        self.assertEqual(calc.add(10), 10)
        self.assertEqual(calc.add(-10), 0)
        self.assertEqual(calc.add(-1), -1)
        self.assertRaises(SyntaxError, calc.add, '2')
        
    '''self.assertEqual(calculator.reset(), 0)
      helps to run tests without getting errors of different values
      '''  

    def test_substract(self):
        self.assertEqual(calc.reset(), 0)
        self.assertEqual(calc.substract(10), -10)
        self.assertEqual(calc.substract(-1), -9)
        self.assertEqual(calc.substract(-9), 0)
        self.assertEqual(calc.substract(-1), 1)

    def test_multiply(self):
        self.assertEqual(calc.reset(), 0)
        self.assertEqual(calc.add(1), 1)
        self.assertEqual(calc.multiply(5), 5)
        self.assertEqual(calc.multiply(-1), -5)
        self.assertEqual(calc.multiply(-1), 5)
        self.assertEqual(calc.multiply(0.5), 2.5)

    
    def test_divide(self):
        self.assertEqual(calc.reset(), 0)
        self.assertEqual(calc.add(2.5), 2.5)
        self.assertEqual(calc.divide(5), 0.5)
        self.assertEqual(calc.divide(-1), -0.5)
        self.assertEqual(calc.divide(-3), 0.16666666666666666) 
        
        self.assertRaises(Warning, calc.divide, 0) #<- checking if raised errors are right


    def test_root(self):
        '''Since the calculator has memory, and the tests are running one by one, resetting the memory and giving
        the new value for the current_value helps to run the following tests with n root functions
        '''
        self.assertEqual(calc.reset(), 0)
        self.assertEqual(calc.add(16), 16)
        self.assertEqual(calc.root(4), 2)
        self.assertEqual(calc.root(-1), 0.5)
        #This helps to get the negative value of current_value
        self.assertEqual(calc.add(-2.5), -2)

        self.assertRaises(Warning, calc.root, -2) #<- cecking if the calculator.root spots the negative current_value
        self.assertEqual(calc.reset(), 0)
        self.assertRaises(Warning, calc.root, 0) #<- checking if raised errors are right


'''this helps to write in the terminal of python:
python test_calculator.py instead of 
python -m unittest test_calculator.py
'''

if __name__ == '__main__':
    unittest.main()