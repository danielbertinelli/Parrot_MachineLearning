import time
from pyardrone import ARDrone

parrot_ = ARDrone() #iniciamos la clase ArDRone
class Parrot(): #clase que permite realizar los movimientos al drone, durante dos segundos ininterrumpidos.

    def Mover_izq(self): #mover a la izquierda
        tiempo_inicial = time.time()
        while time.time()-tiempo_inicial <= 2:
            parrot_.move(left=0.1)

    def Mover_dcha(self): #mover a la derecha
        tiempo_inicial = time.time()
        while time.time()-tiempo_inicial <= 2:
            parrot_.move(right=0.1)

    def Mover_arriba(self): #mover arriba
        tiempo_inicial = time.time()
        while time.time()-tiempo_inicial <= 2:
            parrot_.move(up=0.1)

    def Mover_abajo(self): #mover abajo
        tiempo_inicial = time.time()
        while time.time()-tiempo_inicial <= 2:
            parrot_.move(down=0.1)

    def Mover_delante(self): #mover hacia delante
        tiempo_inicial = time.time()
        while time.time()-tiempo_inicial <= 2:
            parrot_.move(forward=0.1)

    def Mover_atras(self): #mover hacia atrás
        tiempo_inicial = time.time()
        while time.time()-tiempo_inicial <= 2:
            parrot_.move(backward=0.1)
    def TakeOff(self):
        tiempo_inicial = time.time()
        parrot_.takeoff()
        parrot_.hover(3)
    def Landing(self):
        parrot_.land()