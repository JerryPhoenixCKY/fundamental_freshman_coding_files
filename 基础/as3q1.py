class Matrix:
    def __init__(self, data):
        if not isinstance(data, list) or len(data) != 2 or not all(isinstance(j, list) and len(j) == 2 for i in data for j in i):
            print('error input')
            exit()
        self.data = data

    def __add__(self):
        self.__addfinal=[[self.data[0][0][0]+self.data[1][0][0],self.data[0][0][1]+self.data[1][0][1]],
                         [self.data[0][1][0]+self.data[1][1][0],self.data[0][1][1]+self.data[1][1][1]]]
        return self.__addfinal

    def __sub__(self):
        self.__subfinal=[[self.data[0][0][0]-self.data[1][0][0],self.data[0][0][1]-self.data[1][0][1]],
                         [self.data[0][1][0]-self.data[1][1][0],self.data[0][1][1]-self.data[1][1][1]]]
        return self.__subfinal
    def __mul__(self):
        # Perform matrix multiplication
        self.__mulfinal = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    self.__mulfinal[i][j] += self.data[0][i][k] * self.data[1][k][j]
        return self.__mulfinal

##########################################################################################################

a=Matrix([[[1,2],[3,4]],[[5,6],[7,8]]]);print(a.__add__())
s=Matrix([[[1,2],[3,4]],[[5,6],[7,8]]]);print(s.__sub__())
m=Matrix([[[1,2],[3,4]],[[5,6],[7,8]]]);print(m.__mul__())
a=Matrix([[[1,9,2],[3,4]],[[5,6],[7,8]]]);print(a.__add__())