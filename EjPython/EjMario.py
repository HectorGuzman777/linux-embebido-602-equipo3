
def my_function(x:int,y:int)->int:
    #print("x = {}".format(x)) 
    print(f"{x=}")    #permite que des formato la f, especial de strings
    print(f"{y=}")
    return x+y

#posicionales #llaves
def my_function_2(*args,**kwargs)->int:
    print(args[0])
    print(kwargs.get('power'))
    x=args[0]
    y = kwargs.get('power')
    return x**y

class Point:
    name:str = "Clase punto"
    
    def __init__(self, x:int, y:int)->None:
        self.x=x
        self.y=y
    

class Point3D(Point):

    def __init__(self,x:float,y:float,z:float):
        self.z = z
        super().__init__(x,y)





if __name__ =='__main__':
    print(my_function(3,4))

    print(my_function(y=9,x=3))

    print('second function')

    variables=(2,3,4) #this is a tuple
    variable_list = [1,2,3,4,5]
    variable_dict = {
        'var1': 1,
        'var2': 2,
        3:3
    }

xor_dict={
    (0,0): 0,
    (0,1): 1,
    (1,0): 1,
    (1,1): 0

}
#print(my_function_2(2,power=3))  #funcion 2 elevado a la potencia de 3
print(my_function_2(*variables,power=3,var=3))

print(variable_dict)
print("XOR(1,0)->",xor_dict[(1,0)])


point1=Point(5,6)

point2 = Point3D(4,5,6)

print(point2.name)