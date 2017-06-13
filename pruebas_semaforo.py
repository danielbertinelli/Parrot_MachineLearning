from threading import Thread, Semaphore
import time
import warnings
import numpy as np
from libs import communications, filterings, graphics, datalog, normalizado,algoritmos
from sklearn.preprocessing import normalize, StandardScaler

from pyardrone import ARDrone
from pygame import mixer
from sklearn.model_selection import train_test_split
import openpyxl
import sys
semaforo = Semaphore(1)
semaforo2= Semaphore(1)
np.random.seed(777) #Semilla aleatoria para que las pruebas de precisión sean siempre iguales
warnings.filterwarnings("ignore", category=DeprecationWarning)
communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()
graphic = graphics.GraphicsManager()
report = datalog.DatalogManager()
filtros = normalizado.Normalizador()
clasificador = algoritmos.Algoritmos()
communication.open_serial_port()
graphic.set_plot_parameters()
drone=ARDrone()
old_prediction = []
old_prediction.append(0)
x = []
y = []
z = []
digitos_prediccion = []
digitos_prediccion2 = []
muestras = []
vectorguardado=[]


def Adquirir_Datos():
    tiempo_inicial_adquisicion = time.time()
    while (time.time() - tiempo_inicial_adquisicion) <= 1300:

        print(len(digitos_prediccion))
        communication.send_data_request()
        time.sleep(0.1)
        if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
            semaforo.acquire()
def leedatos():
    print(str(digitos_prediccion))
    mixer.init()
    alertasonido = mixer.Sound('ding.wav')
    contador = -1
    tiempo_inicial_lectura = time.time()
    n_iteraciones = 0
    clasificador.Entrena_algoritmo('v10.csv')
    while (time.time() - tiempo_inicial_lectura) <= 1300:
        bytestoread, inbyte = communication.read_data()

        if (bytestoread == 7) or (bytestoread == 14):
            contador += 1
            print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) + ' bits to read ' + str(
                bytestoread))
            x.append((inbyte[bytestoread - 3]))
            y.append((inbyte[bytestoread - 2]))
            z.append((inbyte[bytestoread - 1]))
            digitos_prediccion.append(x[contador])
            digitos_prediccion.append(y[contador])
            digitos_prediccion.append(z[contador])
            print('Longitud de digitos de prediccion'+ str(len(digitos_prediccion)))
            print('contador de thread 2 ' + str(contador))
            cont_predicciones = 0
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                prediccion = clasificador.Clasificador(n_iteraciones, digitos_prediccion)
                print(old_prediction)
                print('contador predicciones : ' + str(cont_predicciones))
                filtering.filter_aceleration_pro(digitos_prediccion, False)
                prediccion = clasificador.Clasificador(n_iteraciones, digitos_prediccion)
                n_iteraciones = n_iteraciones + 1
                if prediccion == 1:
                    print('arriba')
                    time.sleep(1)
                    semaforo.release()
                    alertasonido.play()

                if prediccion == 2:
                    print('abajo')
                    time.sleep(1)
                    semaforo.release()
                    alertasonido.play()
                if prediccion == 3:
                    print('derecha')
                    time.sleep(1)
                    semaforo.release()
                    alertasonido.play()

                if prediccion == 4:
                    print('izquierda')
                    time.sleep(1)
                    semaforo.release()
                    alertasonido.play()
                if prediccion == 5:
                    print('modo2')
                    time.sleep(1)
                    semaforo.release()
                    alertasonido.play()
                if prediccion == 0:
                    print('random')
                    time.sleep(1)
                    semaforo.release()
                    alertasonido.play()

def Lectura_Orden():
    contador = -1
    tiempo_inicial_lectura = time.time()
    n_iteraciones = 0
    mixer.init()
    alertamovimiento = mixer.Sound("DeskBell.wav")
    alertamal = mixer.Sound("buzzer.wav")
    alertamodo = mixer.Sound("ding.wav")
    n_pruebas = 0
    clasificador.Entrena_algoritmo('v10.csv')
    drone.trim()
    modo = True  # Por defecto esta en vertical pues al inicio el dron esta en el suelo.

    drone.navdata_ready.wait()
    bateria = drone.state.vbat_low
    print('Bateria baja?' + str(bateria))
    while (time.time() - tiempo_inicial_lectura) <= 1300:
        bytestoread, inbyte = communication.read_data()

        if (bytestoread == 7) or (bytestoread == 14):
            contador += 1
            print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) + ' bits to read ' + str(
                bytestoread))
            x.append((inbyte[bytestoread - 3]))
            y.append((inbyte[bytestoread - 2]))
            z.append((inbyte[bytestoread - 1]))

            filtering.filter_acceleration(x, contador)
            filtering.filter_acceleration(y, contador)
            filtering.filter_acceleration(z, contador)
            digitos_prediccion.append(x[contador])
            digitos_prediccion.append(y[contador])
            digitos_prediccion.append(z[contador])
            print('X: ' + str(x[contador]) + 'Y: ' + str(y[contador]))
            print('contador de thread 2 ' + str(contador))
            print('contador de iteraciones ' + str(n_iteraciones))
            cont_predicciones = 0

            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                prediccion = clasificador.Clasificador(n_iteraciones, digitos_prediccion)
                n_iteraciones = n_iteraciones + 1

                print(old_prediction)
                print('contador predicciones : ' + str(cont_predicciones))
                if prediccion == 1:
                    print('arriba')

                    if modo == True:  # movimientos verticales
                        if drone.state.fly_mask == False and old_prediction[
                                    cont_predicciones - 1] == 1:  # está en el suelo y el movimiento anterior ha sido hacia arriba (2 arriba pa despegar)
                            drone.takeoff()
                            time.sleep(3.5)
                            semaforo.release()
                            alertamovimiento.play()

                        else:  # dron esta volando
                            timex = time.time()
                            while time.time() - timex <= 0.8:
                                drone.move(up=0.7)
                            semaforo.release()
                            alertamovimiento.play()

                    else:  # movimientos plano horizontal
                        if drone.state.fly_mask == True:  # está volando
                            time1 = time.time()
                            while time.time() - time1 <= 1:
                                drone.move(backward=0.15)
                            semaforo.release()
                            alertamovimiento.play()

                    cont_predicciones += 1

                elif prediccion == 2:
                    print('abajo')

                    if modo == True:  # movimientos verticales
                        timex2 = time.time()
                        while time.time() - timex2 <= 0.8:
                            drone.move(down=0.7)
                        semaforo.release()
                        alertamovimiento.play()

                    else:  # movimientos horizontales
                        if drone.state.fly_mask == True:  # volando
                            time1 = time.time()
                            while time.time() - time1 <= 1:
                                drone.move(forward=0.15)
                            semaforo.release()
                            alertamovimiento.play()

                    cont_predicciones += 1

                elif prediccion == 3:
                    print('derecha')
                    cont_predicciones += 1
                    if modo == True:
                        time2 = time.time()
                        while time.time() - time2 <= 1:
                            drone.move(right=0.1)
                        semaforo.release()
                        alertamovimiento.play()

                    else:
                        time3 = time.time()
                        while time.time() - time3 <= 1:
                            drone.move(cw=0.3)
                        semaforo.release()
                        alertamovimiento.play()



                elif prediccion == 4:
                    print('izquierda')
                    cont_predicciones += 1
                    if modo == True:
                        time1 = time.time()
                        while time.time() - time1 <= 1:
                            drone.move(left=0.1)
                        semaforo.release()
                        alertamovimiento.play()

                    else:
                        time1 = time.time()
                        while time.time() - time1 <= 1:
                            drone.move(ccw=0.3)
                        semaforo.release()
                        alertamovimiento.play()


                if prediccion == 5:
                    print('modo2')
                    if drone.state.fly_mask == True and old_prediction[cont_predicciones - 1] == 5:
                        drone.land()
                        alertamodo.play()
                        time.sleep(0.1)
                        print()
                        print('Fin del vuelo.')
                        sys.exit()

                    else:
                        modo = not modo
                        time.sleep(1.5)
                        semaforo.release()
                        alertamodo.play()

                    cont_predicciones += 1

                elif prediccion == 0:
                    print('random')
                    time.sleep(1.5)
                    semaforo.release()
                    alertamal.play()

                    cont_predicciones += 1
                if cont_predicciones >= 1:
                    old_prediction.append(int(prediccion))

    print(digitos_prediccion)
    drone.land()

class Thread_Adquisicion(Thread):
    def __init__(self):  # Constructor de la clase
        Thread.__init__(self)

    def run(self):

        Adquirir_Datos()


class Thread_Lectura(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        leedatos()
class Thread_Orden(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):

        Lectura_Orden()
input('Pulsa enter para empezar')
#Main
hilo=Thread_Adquisicion()
hilo2 = Thread_Orden()
hilo.start()
hilo2.start()

