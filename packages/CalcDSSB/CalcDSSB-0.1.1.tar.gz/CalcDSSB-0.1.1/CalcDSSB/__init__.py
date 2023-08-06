""" Calculator package"""

__version__ = "0.1.1"


class Calculator_SB(object):
    """
    DESCRIPTION
        This Class provides Calculator functionality by performing these
        mathematical functions: addition, subtraction,
        multiplication and division.
        Calculator has internal memory with a reset optionality.

    METHODS
        __init__(self)
            Sets memory to zero.

        add(self, number)
            Adds number to memory.
            Returns memory.

        sub(self, number)
            Subtracts number from memory.
            Return memory.

        multi(self, number)
            Multiples  memory by number.
            Return memory.

        div(self, number)
            Divides memory by number.
            Return memory.

        srt(self)
            Takes square root of memory.
            Return memory.

        mem_reset(self)
            Resets memory to zero.
    """

    def __init__(self):
        self.memory = 0

    def add(self, number):
        self.memory += number
        return self.memory

    def sub(self, number):
        self.memory -= number
        return self.memory

    def multi(self, number):
        self.memory *= number
        return self.memory

    def div(self, number):
        self.memory /= number
        return self.memory

    def sqr(self):
        self.memory **= 0.5
        return self.memory

    def mem_reset(self):
        self.memory = 0


if __name__ == "__main__":
    print("Calculator package")
