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

warnings.filterwarnings("ignore", category=DeprecationWarning)
communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()
graphic = graphics.GraphicsManager()
report = datalog.DatalogManager()
filtros = normalizado.Normalizador()
communication.open_serial_port()



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
# Creamos clasificador

clf_neuronal = MLPClassifier(solver='lbfgs', alpha=0.000000000001, early_stopping=True, max_iter=9,
                             hidden_layer_sizes=12)

clf_neuronal.fit(X_train, y_train)



x = []
y = []
z = []
x_aux = []
y_aux = []
digitos_prediccion=[]
tiempo_inicial = time.time()
plt.ion()
mixer.init()
alertamovimiento = mixer.Sound("DeskBell.wav")
alertamodo = mixer.Sound("buzzer.wav")

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

def leedatos():
    contador=-1
    tiempo_inicial_lectura=time.time()
    n_iteraciones = 0

    while (time.time()-tiempo_inicial_lectura)<=40:
        bytestoread, inbyte = communication.read_data()

        if (bytestoread == 7) or (bytestoread == 14):
            contador+=1
            print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) +' bits to read '+str(bytestoread))
            x.append((inbyte[bytestoread - 3]))
            y.append((inbyte[bytestoread - 2]))
            z.append((inbyte[bytestoread - 1]))
            x_aux.append((inbyte[bytestoread - 3]))
            y_aux.append((inbyte[bytestoread - 2]))
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
                    #alertamovimiento.play()
                if prediccion == 2:
                    print('abajo')
                    time.sleep(1)
                    #alertamovimiento.play()
                if prediccion == 3:
                    print('derecha')
                    time.sleep(1)
                    #alertamovimiento.play()
                if prediccion == 4:
                    print('izquierda')
                    time.sleep(1)
                    #alertamovimiento.play()
                if prediccion == 5:
                    print('modo2')
                    time.sleep(1)
                    #alertamodo.play()
                if prediccion==0:
                    print('random')
                    time.sleep(1)
                    #alertamovimiento.play()

        time.sleep(0.25)
    print(digitos_prediccion)


def Clasificador(iteracion):
            print('Longitud de X: '+str(len(x)))
            test_data = normalize(digitos_prediccion[0+(30*(iteracion)):30+((iteracion)*30)])
            test_data = scaler.transform(test_data)
            prediccion = clf_neuronal.predict(test_data)
            return prediccion






peticion_aceleracion = Thread(target=adquieredatos)
lectura_almacenado = Thread(target=leedatos)#


peticion_aceleracion.start()
lectura_almacenado.start()

time.sleep(1)
i =0
graphic.set_plot_parameters()
tiempo_graficas = time.time()
while time.time()-tiempo_graficas<=40:
    if len(x)>0:
        if len(y)>0:
            graphic.plot_data(x[len(x)-1], y[len(y)-1])
            i +=1
    plt.pause(0.01)


