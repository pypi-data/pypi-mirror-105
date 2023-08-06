class Calculator:

    def __init__(self, current_value = 0):
        self.current_value = current_value

    def add(self, to_add):
        #Add function
         if type(to_add) != str:
             self.current_value += to_add
         else:
             raise SyntaxWarning("Please insert a number")

         return self.current_value
    
    def substract(self, to_sub):
        #Substraction Function
        # if type(input) == int <-checking that the user uses the right type of input
        if type(to_sub) != str:
            self.current_value -= to_sub
        else:
            raise SyntaxWarning("Please insert a number")

        return self.current_value

    def multiply(self, to_mul):
        #Multiplication Function
        if type(to_mul) != str:
            self.current_value *= to_mul
        else:
            return SyntaxWarning("Please insert a number")

        return self.current_value

    def divide(self, to_div):
        #Division Function
        if type(to_div) != str():
            self.current_value /= to_div


        #Checking if division is not made by zero
        elif int(to_div) == 0:
            raise Warning("Division by zero is invalid :(")

        else:
            raise SyntaxWarning("Please insert a number")
        
        return self.current_value
    
    def root(self, to_root):
        #n root Function
        
        if type(to_root) != str:
            x = 1/to_root
            self.current_value **= x
        #Checking if division is not made by zero
        elif to_root == 0:
            raise Warning("n root by zero is invalid :(")

        if int(self.current_value) < 0:
            raise Warning("Can not root the negative values!")

        return self.current_value

    def reset(self):
        #resets the memory
        self.current_value = 0
        return self.current_value 
    
    #Helps to keep the script to be not invoked
    if __name__ == '__main__':
        current_value = 0
        memory = current_value
        memo = [current_value]
        main(current_value, memory, memo)
    