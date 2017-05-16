#Imports de las clases necesarias para obtener los datos del reloj, así como operadores matemáticos, ploteadores, warnings..
#from libs import communications, filterings, graphics, datalog, normalizado
#import parrot
import time
cont=[]
contador=0
timex=time.time()
while time.time()-timex<=50:
    cont.append(contador)
    contador+=1
    print('b')
    print(contador)
    print('a')
    print(cont[contador-1])
