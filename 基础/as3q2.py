class ComplexNumber:
    def __init__(self, num1, num2):
        try:
            self.num1_str=num1
            self.num2_str=num2

            if '+' in num1 and 'i' in num1:
                parts = num1.split('+')
                self.num1_real=int(parts[0])
                self.num1_imag=int(parts[1].replace('i', '')) if 'i' in parts[1] else 0
            elif '-' in num1 and 'i' in num1:
                if num1[0]=='-':
                    parts = num1.split('-')
                    self.num1_real=-int(parts[1]) if parts[1] else 0
                    self.num1_imag=-int(parts[2].replace('i', '')) if 'i' in parts[1] else 0
                else:
                    parts = num1.split('-',1)
                    self.num1_real = int(parts[0]) if parts[0] else 0
                    self.num1_imag = -int(parts[1].replace('i', '')) if 'i' in parts[1] else 0
            elif 'i' in num1:
                self.num1_real= 0
                self.num1_imag=int(num1.replace('i', ''))
            else:
                self.num1_real= int(num1)
                self.num1_imag=0

            if '+' in num2 and 'i' in num2:
                parts = num2.split('+')
                self.num2_real=int(parts[0])
                self.num2_imag=int(parts[1].replace('i', '')) if 'i' in parts[1] else 0
            elif '-' in num2 and 'i' in num2:
                if num2[0] == '-':
                    parts = num2.split('-')
                    self.num2_real = -int(parts[1]) if parts[1] else 0
                    self.num2_imag = -int(parts[2].replace('i', '')) if 'i' in parts[1] else 0
                else:
                    parts = num2.split('-', 1)
                    self.num2_real = int(parts[0]) if parts[0] else 0
                    self.num2_imag = -int(parts[1].replace('i', '')) if 'i' in parts[1] else 0
            elif 'i' in num2:
                self.num2_real=0
                self.num2_imag=int(num2.replace('i', ''))
            else:
                self.num2_real=int(num2)
                self.num2_imag=0

        except:
            print('Invalid complex number format')

    def __add__(self):
        real = self.num1_real+self.num2_real
        imag = self.num1_imag+self.num2_imag
        if imag== 0:
            return f"Addition:{real}"
        elif real== 0:
            return f"Addition:{imag}i"
        else:
            return f"Addition:{real}+{imag}i"

    def __sub__(self):
        real = self.num1_real - self.num2_real
        imag = self.num1_imag - self.num2_imag
        if imag == 0:
            return f"Subtraction:{real}"
        elif real == 0:
            return f"Subtraction:{imag}i"
        else:
            return f"Subtraction:{real}+{imag}i"

    def __mul__(self):
        real = self.num1_real*self.num2_real- self.num1_imag*self.num2_imag
        imag = self.num1_real*self.num2_imag +self.num1_imag*self.num2_real
        if imag==0:
            return  f"Multiplication:{real}"
        elif real==0:
            return f"Multiplication:{imag}i"
        else:
            if imag<0:
                return f"Multiplication:{real}{imag}i"
            else:
                return f"Multiplication:{real}+{imag}i"

    def __division__(self):
        if self.num2_real == 0 and self.num2_imag==0:
            print('can not be divided')
            exit()
        fm= self.num2_real ** 2 + self.num2_imag ** 2
        real = (self.num1_real * self.num2_real+self.num1_imag*self.num2_imag) /fm
        imag = (self.num1_imag * self.num2_real-self.num1_real*self.num2_imag) /fm
        if imag == 0:
            return f"Division:{real}"
        elif real == 0:
            return f"Division:{imag}i"
        else:
            return f"Division:{real}+{imag}i"

##################################################################################################################################

a=ComplexNumber('3+4i','-2-5i');print(a.__add__());print(a.__sub__());print(a.__mul__());print(a.__division__())
d=ComplexNumber('3+4i','1-2i');print(d.__add__());print(d.__sub__());print(d.__mul__());print(d.__division__())
b=ComplexNumber('3+4i','0');print(b.__add__());print(b.__sub__());print(b.__mul__());print(b.__division__())