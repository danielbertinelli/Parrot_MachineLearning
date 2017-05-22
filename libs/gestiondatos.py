from threading import Thread
import time
import matplotlib.pyplot as plt
from random import choice
import time
import warnings
import numpy as np
from libs import communications, filterings, graphics, datalog, normalizado,algoritmos
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.neural_network import MLPClassifier
from pyardrone import ARDrone
from pygame import mixer
from sklearn.model_selection import train_test_split
import openpyxl
import sys


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
muestras = []
class GestiondeDatos():
    # Método para realizar peticiones de aceleración y esperar cuando se procese una muestra

    def adquieredatos(self):
        tiempo_inicial_adquisicion = time.time()
        while (len(digitos_prediccion)) <= 1300:
            communication.send_data_request()
            time.sleep(0.25)
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(1)
                print('HAZ MOVIMIENTO')
                time.sleep(0.2)
    def adquieredatos2(self,n_muestras):
        tiempo_inicial_adquisicion = time.time()
        while (len(muestras)) <= n_muestras * 30:
            communication.send_data_request()
            time.sleep(0.25)
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(1)
                print('HAZ MOVIMIENTO')
                time.sleep(0.2)

    # Método para leer los datos del reloj y guardarlos en un fichero con etiqueta
    def lee_y_guarda(self,index,n_muestras_input):

        print('Guardando datos')
        print('Numero de muestras input'+str(n_muestras_input))
        contador = -1
        tiempo_inicial_lectura = time.time()
        i=n_muestras_input*5
        print ('Longitud de vector muestras deseada '+str(i))
        contador_while=0
        etiqueta = 1
        while contador_while <= i: # 5 pues divides 30 aceleraciones por 6 movimientos
            bytestoread, inbyte = communication.read_data()

            if (bytestoread == 7) or (bytestoread == 14):
                contador += 1
                print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) + ' bits to read ' + str(
                    bytestoread))
                x.append((inbyte[bytestoread - 3]))
                y.append((inbyte[bytestoread - 2]))
                z.append((inbyte[bytestoread - 1]))
                print('contador de thread 2 ' + str(contador))
                filtering.filter_acceleration(x, contador)
                filtering.filter_acceleration(y, contador)
                filtering.filter_acceleration(z, contador)
                muestras.append(x[contador])
                muestras.append(y[contador])
                muestras.append(z[contador])
                contador_while+=3
                print('Longitud de muestras: ' + str(len(muestras)))
                if (len(muestras) % 30) == 0 and len(muestras) != 0:
                    w = len(muestras) / 30
                    print('W =' + str(w))
                    index_inicial = int((w - 1) * 30)
                    print(index_inicial)
                    index_final = int((w * 30) - 1)
                    print(index_final)
                    digitos_muestra = muestras[index_inicial:index_final+1]
                    print('Longitud de datos a guardar'+str(len(digitos_muestra)))
                    digitos_muestra.append(index)
                    print(str(digitos_muestra))
                    doc = openpyxl.load_workbook('datos_muestra.xlsx')
                    hoja = doc.get_sheet_by_name('Hoja1')
                    ws = doc.active
                    ws.append(digitos_muestra)
                    doc.save('datos_muestra.xlsx')

                    time.sleep(0.7)
            time.sleep(0.25)

    # Método para leer los datos, clasificarlos y ejecutar ordenes del dron
    def lee_plotea_ordena(self):
        contador = -1
        tiempo_inicial_lectura = time.time()
        n_iteraciones = 0
        mixer.init()
        alertamovimiento = mixer.Sound("DeskBell.wav")
        alertamodo = mixer.Sound("buzzer.wav")
        n_pruebas = 0


        drone.trim()
        modo = True  # Por defecto esta en vertical pues al inicio el dron esta en el suelo.

        drone.navdata_ready.wait()
        bateria = drone.state.vbat_low
        print('Bateria baja?'+str(bateria))
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
                    prediccion = clasificador.Clasificador(n_iteraciones,digitos_prediccion)
                    n_iteraciones = n_iteraciones + 1

                    print(old_prediction)
                    print('contador predicciones : '+str(cont_predicciones))
                    if prediccion == 1:
                        print('arriba')
                        time.sleep(1)
                        if modo == True:  # movimientos verticales
                            if drone.state.fly_mask == False and old_prediction[cont_predicciones - 1] == 1:  # está en el suelo y el movimiento anterior ha sido hacia arriba (2 arriba pa despegar)
                                drone.takeoff()
                                time.sleep(0.3)
                                print('HOLADANIEL')
                                alertamovimiento.play()
                                time.sleep(0.1)
                            else:  # dron esta volando
                                timex = time.time()
                                while time.time() - timex <= 1:
                                    drone.move(up=0.6)
                                alertamovimiento.play()
                                time.sleep(0.1)
                        else:  # movimientos plano horizontal
                            if drone.state.fly_mask == True:  # está volando
                                time1 = time.time()
                                while time.time() - time1 <= 1:
                                    drone.move(backward=0.2)
                                alertamovimiento.play()
                                time.sleep(0.1)
                        cont_predicciones += 1

                    elif prediccion == 2:
                        print('abajo')
                        time.sleep(1)

                        if modo == True:  # movimientos verticales
                            timex2 = time.time()
                            while time.time() - timex2 <= 1:
                                drone.move(down=0.6)
                            alertamovimiento.play()
                            time.sleep(0.1)
                        else:  # movimientos horizontales
                            if drone.state.fly_mask == True:  # volando
                                time1 = time.time()
                                while time.time() - time1 <= 1:
                                    drone.move(forward=0.2)
                                alertamovimiento.play()
                                time.sleep(0.1)
                        cont_predicciones += 1

                    elif prediccion == 3:
                        print('derecha')
                        time.sleep(1)
                        cont_predicciones += 1
                        time2 = time.time()
                        while time.time() - time2 <= 1:
                            drone.move(right=0.2)
                        alertamovimiento.play()
                        time.sleep(0.1)


                    elif prediccion == 4:
                        print('izquierda')
                        time.sleep(1)
                        cont_predicciones += 1
                        time1 = time.time()
                        while time.time() - time1 <= 1:
                            drone.move(left=0.2)
                        alertamovimiento.play()
                        time.sleep(0.1)

                    if prediccion == 5:
                        print('modo2')
                        time.sleep(1)
                        if drone.state.fly_mask == True and old_prediction[cont_predicciones - 1] == 5:
                            drone.land()
                            alertamovimiento.play()
                            time.sleep(0.1)

                        else:
                            modo = not modo
                            alertamodo.play()
                            time.sleep(0.1)
                        cont_predicciones += 1

                    elif prediccion == 0:
                        print('random')
                        time.sleep(1)
                        cont_predicciones += 1
                    if cont_predicciones >= 1:
                        old_prediction.append(int(prediccion))
            time.sleep(0.25)
        print(digitos_prediccion)
