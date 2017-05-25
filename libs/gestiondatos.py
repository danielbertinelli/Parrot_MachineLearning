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
vectorguardado=[]
class GestiondeDatos():
    # Método para realizar peticiones de aceleración y esperar cuando se procese una muestra

    def adquieredatos(self):
        tiempo_inicial_adquisicion = time.time()
        while (time.time() - tiempo_inicial_adquisicion) <= 1300:
            communication.send_data_request()
            time.sleep(0.25)
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(1)
                print('HAZ MOVIMIENTO')
                time.sleep(0.2)
    def adquieredatos2(self,n_muestras,velocidad):
        vlcty = 1/velocidad
        tiempo_inicial_adquisicion = time.time()
        while (len(digitos_prediccion)) < n_muestras * 30:
            communication.send_data_request()
            time.sleep(vlcty)
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(0.11)
                #print('HAZ MOVIMIENTO')

        print('Fin de la adquisición')
    def adquieredatos3(self,velocidad):
        vlcty = 1/velocidad
        tiempo_inicial_adquisicion = time.time()
        while (time.time() - tiempo_inicial_adquisicion) <= 1300:
            communication.send_data_request()

            time.sleep(vlcty)
            if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                time.sleep(2)
                print('Haz')



    # Método para leer los datos del reloj y guardarlos en un fichero con etiqueta
    def lee_y_guarda(self,n_muestras,filename):

        archi = open(filename + '.csv', 'a')
        print('Guardando datos')
        print('Numero de muestras input' + str(n_muestras))
        n_iteraciones = 0
        contador = -1
        while len(digitos_prediccion)< n_muestras*30:
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
                if (len(digitos_prediccion) % 30) == 0 and len(digitos_prediccion) != 0:
                    muestra_guardar = digitos_prediccion[0 + (30 * (n_iteraciones)):30 + ((n_iteraciones) * 30)]
                    n_iteraciones = n_iteraciones + 1
                    if n_iteraciones<= n_muestras/6:  #Los movimientos aleatorios
                        muestra_guardar.append(0)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras/6:
                            var = input('El próximo movimiento es hacia arriba')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
                    if n_iteraciones<= n_muestras/3 and n_iteraciones>n_muestras/6 :  #Los movimientos hacia arriba
                        muestra_guardar.append(1)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras/3:
                            var = input('El próximo movimiento es hacia abajo')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
                    if n_iteraciones<= n_muestras/2 and n_iteraciones>n_muestras/3:  #Los movimientos hacia abajo
                        muestra_guardar.append(2)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras/2:
                            var = input('El próximo movimiento es hacia la derecha')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
                    if n_iteraciones<= n_muestras*4/6 and n_iteraciones>n_muestras/2 :  #Los movimientos hacia la derecha
                        muestra_guardar.append(3)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras*4/6:
                            var = input('El próximo movimiento es hacia la izquierda')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')

                    if n_iteraciones<= n_muestras*5/6 and n_iteraciones>n_muestras*4/6 :  #Los movimientos hacia la derecha
                        muestra_guardar.append(4)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras*5/6:
                            var = input('El próximo movimiento es de cambio de modo')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')

                    if n_iteraciones<= n_muestras and n_iteraciones>n_muestras*5/6 :  #Los movimientos de cambio de modo
                        muestra_guardar.append(5)
                        vectorguardado.append(muestra_guardar)
                        print(muestra_guardar)
                        if n_iteraciones==n_muestras:
                            print('Final de la recogida de muestras')
                        else:
                            var_ = input('Pulsa enter para empezar, descansa si lo necesitas.')

        print('Fichero Guardado')
        print('Vector a guardar: '+str(vectorguardado))

        for i in range(len(vectorguardado)):
            vector_aux = vectorguardado[i]
            for j in range(len(vector_aux)):
                if j%30==0 and j !=0:
                    archi.write(str(vector_aux[j]))
                else:
                    archi.write(str(vector_aux[j]) + ';')
            archi.write('\n')

        def lee_plotea_clasifica(self):
            contador = -1
            tiempo_inicial_lectura = time.time()
            n_iteraciones = 0

            n_pruebas = 0

            while (time.time() - tiempo_inicial_lectura) <= 1300:
                bytestoread, inbyte = communication.read_data()

                if (bytestoread == 7) or (bytestoread == 14):
                    contador += 1
                    print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(
                        len(inbyte)) + ' bits to read ' + str(
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
                            time.sleep(1)
                            if modo == True:  # movimientos verticales
                                if drone.state.fly_mask == False and old_prediction[
                                            cont_predicciones - 1] == 1:  # está en el suelo y el movimiento anterior ha sido hacia arriba (2 arriba pa despegar)
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

        print(digitos_prediccion)
        drone.land()