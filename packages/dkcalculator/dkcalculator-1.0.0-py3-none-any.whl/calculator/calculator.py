from typing import Union


class Calculator:
    """Allows to perform these main methods: addition, subtraction, multiplication, division and taking the nth root of
     number.

    Calculator class has a memory attribute which by default is 0. All above methods perform actions with a value inside
    class memory until it is reset to 0 again. As a result reset method is a part of Calculator class.
    """

    def __init__(self):
        self.memory = 0

    @staticmethod
    def is_float(value: Union[int, float]) -> None:
        if type(value) != int and type(value) != float:
            raise ValueError(f'expected float or int, got {type(value)}')

    def add(self, number: Union[int, float]) -> Union[int, float]:
        """Adds the given number to the value of memory attribute"""
        self.is_float(number)
        self.memory += number
        return self.memory

    def subtract(self, number: Union[int, float]) -> Union[int, float]:
        """Subtracts the given number from the value of memory attribute"""
        self.is_float(number)
        self.memory -= number
        return self.memory

    def multiply(self, number: Union[int, float]) -> Union[int, float]:
        """Multiplies the value of memory attribute by the given number"""
        self.is_float(number)
        self.memory *= number
        return self.memory

    def divide(self, number: Union[int, float]) -> float:
        """Divides the value of memory attribute by the given number or raises ValueError if divisor is 0"""
        self.is_float(number)
        if number == 0:
            raise ZeroDivisionError('can not divide by zero!')
        self.memory /= number
        return self.memory

    def nth_root(self, root: Union[int, float]) -> Union[int, float]:
        """Performs the nth root on the value of memory attribute"""
        self.is_float(root)
        if self.memory == 0 and root < 0:
            raise ValueError('this calculator does not take negative root of zero')
        self.memory = self.memory**(1/root)
        return self.memory

    def reset(self) -> int:
        """Resets memory attribute to 0"""
        self.memory = 0
        return self.memory


if __name__ == "__main__":
    print("Calculator says hi!")