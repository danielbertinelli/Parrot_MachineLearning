from threading import Thread
import time
import matplotlib.pyplot as plt
from random import choice
import time
import warnings
import numpy as np
from libs import communications, filterings, graphics, datalog, normalizado
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.neural_network import MLPClassifier
from pyardrone import ARDrone
from  pygame import mixer
from sklearn.model_selection import train_test_split

# Instancias de las clases
warnings.filterwarnings("ignore", category=DeprecationWarning)
communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()
graphic = graphics.GraphicsManager()
report = datalog.DatalogManager()
filtros = normalizado.Normalizador()
communication.open_serial_port()
graphic.set_plot_parameters()
drone=ARDrone()

# Datos de la base de datos para realizar la clasificación
datos = np.genfromtxt( 'BaseDatos.csv',
        delimiter=';')
digitos = normalize(datos[:, :-1])
etiquetas = datos[:, -1]
x_train, x_eval, y_train, y_eval = train_test_split(digitos, etiquetas, test_size=0.5,
                                                    train_size=0.5,
                                                    random_state=1982)
tiempo_inicial = time.time()
scaler = StandardScaler()
scaler.fit(x_train)
X_train = scaler.transform(x_train)
X_test = scaler.transform(x_eval)


# Creación del clasificador y entrenamiento
clf_neuronal = MLPClassifier(solver='lbfgs', alpha=0.000000000001, early_stopping=True, max_iter=9,
                             hidden_layer_sizes=12)

clf_neuronal.fit(X_train, y_train)


# Declaración de los vectores a rellenar
x = []
y = []
z = []
digitos_prediccion=[]
tiempo_inicial = time.time()

# Método para realizar peticiones de aceleración y esperar cuando se procese una muestra
def adquieredatos():
    i=0
    tiempo_inicial_adquisición = time.time()
    while (time.time()-tiempo_inicial_adquisición)<=40:
        communication.send_data_request()
        if len(x)>=10*(i+1):
            time.sleep(0.3)
            i+=1
        time.sleep(0.25)
    print('Tiempo de adquisición:' +str(time.time()-tiempo_inicial_adquisición)+' segundos.')


# Método para leer los datos, clasificarlos y ejecutar ordenes del dron
def leedatos():
    contador=-1
    tiempo_inicial_lectura=time.time()
    n_iteraciones = 0
    mixer.init()
    alertamovimiento = mixer.Sound("/Users/DeskBell.wav")
    alertamodo = mixer.Sound("/Users/buzzer.wav")
    n_pruebas = 0
    old_prediction = []
    old_prediction.append(0)
    drone.trim()
    modo = True  # Por defecto esta en vertical pues al inicio el dron esta en el suelo.
    cont_predicciones = 0

    while (time.time()-tiempo_inicial_lectura)<=40:
        bytestoread, inbyte = communication.read_data()

        if (bytestoread == 7) or (bytestoread == 14):
            contador+=1
            print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) +' bits to read '+str(bytestoread))
            x.append((inbyte[bytestoread - 3]))
            y.append((inbyte[bytestoread - 2]))
            z.append((inbyte[bytestoread - 1]))

            filtering.filter_acceleration(x, contador)
            filtering.filter_acceleration(y, contador)
            filtering.filter_acceleration(z, contador)
            digitos_prediccion.append(x[contador])
            digitos_prediccion.append(y[contador])
            digitos_prediccion.append(z[contador])
            print('X: '+str(x[contador])+ 'Y: '+str(y[contador]))
            print('contador de thread 2 '+str(contador))
            print('contador de iteraciones ' + str(n_iteraciones))

            if len(digitos_prediccion)>= (30*(n_iteraciones+1)):
                prediccion = Clasificador(n_iteraciones)
                n_iteraciones = n_iteraciones + 1

                if prediccion == 1:
                    print('arriba')
                    time.sleep(1)
                    if modo == True: #movimientos verticales
                        if drone.state.fly_mask == False and old_prediction[cont_predicciones-1]==1: #está en el suelo y el movimiento anterior ha sido hacia arriba (2 arriba pa despegar)
                            drone.takeoff()
                            alertamovimiento.play()
                            time.sleep(0.1)
                        else: # dron esta volando
                            timex=time.time()
                            while time.time()-timex<=2:
                                drone.move(up=0.3)
                            alertamovimiento.play()
                            time.sleep(0.1)
                    else: #movimientos plano horizontal
                        if drone.state.fly_mask == True: #está volando
                            time1=time.time()
                            while time.time()-time1<=2:
                                drone.move(backward=0.1)
                            alertamovimiento.play()
                            time.sleep(0.1)
                    cont_predicciones += 1

                elif prediccion == 2:
                    print('abajo')
                    time.sleep(1)

                    if modo == True: #movimientos verticales
                        timex2=time.time()
                        while time.time()-timex2<=2:
                            drone.move(down=0.3)
                        alertamovimiento.play()
                        time.sleep(0.1)
                    else: #movimientos horizontales
                        if drone.state.fly_mask == True: #volando
                            time1 = time.time()
                            while time.time() - time1 <= 2:
                                drone.move(forward=0.1)
                            alertamovimiento.play()
                            time.sleep(0.1)
                    cont_predicciones += 1

                elif prediccion == 3:
                    print('derecha')
                    time.sleep(1)
                    cont_predicciones += 1
                    time2 = time.time()
                    while time.time() - time2 <= 2:
                        drone.move(right=0.1)
                    alertamovimiento.play()
                    time.sleep(0.1)


                elif prediccion == 4:
                    print('izquierda')
                    time.sleep(1)
                    cont_predicciones += 1
                    time1 = time.time()
                    while time.time() - time1 <= 2:
                        drone.move(left=0.1)
                    alertamovimiento.play()
                    time.sleep(0.1)

                if prediccion == 5:
                    print('modo2')
                    time.sleep(1)
                    if drone.state.fly_mask==True and old_prediction[cont_predicciones - 1] == 5:
                        drone.land()
                        alertamovimiento.play()
                        time.sleep(0.1)
                    else:
                        modo = not modo
                        alertamodo.play()
                        time.sleep(0.1)
                    cont_predicciones += 1

                elif prediccion==0:
                    print('random')
                    time.sleep(1)
                    cont_predicciones += 1
                if cont_predicciones >= 1:
                    old_prediction.append(int(prediccion))
        time.sleep(0.25)
    print(digitos_prediccion)

# Método para realizar las clasificaciones
def Clasificador(iteracion):
            print('Longitud de X: '+str(len(x)))
            test_data = normalize(digitos_prediccion[0+(30*(iteracion)):30+((iteracion)*30)])
            test_data = scaler.transform(test_data)
            prediccion = clf_neuronal.predict(test_data)
            return prediccion

# Declaración de los hilos
peticion_aceleracion = Thread(target=adquieredatos)
lectura_almacenado = Thread(target=leedatos)#

# Espera de los datos de navegación para iniciar los hilos
drone.navdata_ready.wait()
peticion_aceleracion.start()
lectura_almacenado.start()

# Si los hilos han acabado finalizar la comunicación con el reloj
if not lectura_almacenado.isAlive():
    communication.close_serial_port()