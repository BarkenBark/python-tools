#import numpy as np

class MultiBaseNumber:
    """ Class representing a 'multi-base number', i.e. a number whose digits stem from different bases

        E.g. number 1020 with multi-base [2,2,3,4] would be equal to 32

        Parameters
        ---------------
        bases : sequence
            Ordered collection of bases.
            bases[0] is the leftmost base
        digits : sequence
            Digits of the number
            digits[0] is the leftmost digit
    """

    def __init__(self, bases, digits=None):
        if self.__check_bases(bases):
            self.bases = bases
        else:
            raise ArithmeticError('Provided bases are not eligible')

        if digits is None:
            self.digits = [0]*len(self.bases)
        else:
            if self.__check_digits(digits):
                self.digits = digits
            else:
                raise ArithmeticError('Provided digits not compatible with specified bases')

    def __check_bases(self, bases):
        return all([base > 0 for base in bases])

    def __check_digits(self, digits):
        """ Checks if 'digits' is compatible with 'bases'

            Parameters
            ---------------
            digits : sequence 
                Digits of the number

            Returns : bool
                True of digits are compatible with bases, False otherwise
        """
        if len(digits) != len(self.bases): return False
        return all([digits[i] < self.bases[i] for i in range(len(digits))])

    def __eq__(self, other):
        return self.base_10() == other.base_10()

    def __ne__(self, other):
        return self.base_10() != other.base_10()

    def __lt__(self, other):
        return self.base_10() < other.base_10()

    def __gt__(self, other):
        return self.base_10() > other.base_10()

    def __le__(self, other):
        return self.base_10() <= other.base_10()

    def __ge__(self, other):
        return self.base_10() >= other.base_10()

    def base_10(self):
        """ Return the base 10 value of the MultiBaseNumber

            Returns : int
        """
        n, b = 0, 1
        for i in reversed(range(len(self.digits))):
            n = n + b*self.digits[i]
            b = b*self.bases[i]
        return n
