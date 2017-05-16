# free_mode_with_ML.py
# Mónica Milán (@mncmilan)
# mncmilan@gmail.com
# http://steelhummingbird.blogspot.com.es/

# This code obtains acceleration data from eZ430-Chronos watch by Texas Instruments, then it eliminates the noise in X
# and Y axis and finally it plots the resulting values. It also uses machine learning in order to detect a clap, the
# background color of the graph.

import matplotlib.pyplot as plt
import time
import warnings
import numpy as np
from libs import communications, filterings, graphics, datalog, normalizado
from sklearn.preprocessing import normalize
#from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from pyardrone import ARDrone
from  pygame import mixer

warnings.filterwarnings("ignore", category=DeprecationWarning)
drone=ARDrone()
communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()
graphic = graphics.GraphicsManager()
report = datalog.DatalogManager()
normalizados = normalizado.Normalizador()

# Load dataset
train_digits = np.genfromtxt('/Users/Usuario/Desktop/Daniel/TFG/Codigo/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/BaseDato.csv', delimiter = ';')
train_data = train_digits[:, :-1]
train_labels = train_digits[:, -1]

#print(train_digits)
#print(train_labels)
train_data = normalize(train_data)

# Create a classifier
#classifier = KNeighborsClassifier()
#classifier = SVC(gamma=0.001, probability=True)
#classifier = DecisionTreeClassifier(random_state=0)
#classifier = RandomForestClassifier(n_estimators = 100)
classifier = MLPClassifier(solver='lbfgs', alpha=0.000000000001, early_stopping=True, validation_fraction=0.15, max_iter=300)
# Train the classifier
classifier.fit(train_data, train_labels)

drone.navdata_ready.wait()
class FreeMovementML():
    communication.open_serial_port()
    #max_samples = 22
    watch_samples_counter = -1
    save_into_file = True
    lower_index = 0
    higher_index = 30
    snapfingers = 0
    mixer.init()
    alertamovimiento = mixer.Sound("/Users/DeskBell.wav")
    alertamodo = mixer.Sound("/Users/buzzer.wav")
    n_pruebas= 0
    old_prediction = []
    old_prediction.append(0)
    x_axis_acceleration = []
    y_axis_acceleration = []
    z_axis_acceleration = []
    test_digits = []
    drone.trim()
    time_limit = 60 # Datalog time)
    k = 0
    t1=0
    modo = True  # Por defecto esta en vertical pues al inicio el dron esta en el suelo.
    muestra = []
    n_pruebas = 0  # contador del numero de movimientos clasificados
    time_limit = 300  # tiempo del vuelo
   # print(drone.navdata.demo.vbat_flying_percentage)
    time_initial = time.time()
    graphic.set_plot_parameters()
#time.time() - time_initial <= time_limit:
    while time.time() - time_initial <= time_limit:
        time_final = time.time()
        bytes_to_read = communication.send_data_request()
        inbyte = communication.read_data(bytes_to_read)

        if (bytes_to_read == 7 and inbyte[3] == 1) or (bytes_to_read == 14 and inbyte[10] == 1):
            watch_samples_counter += 1
            print(watch_samples_counter)
            x_axis_acceleration.append(inbyte[bytes_to_read-3])
            filtering.filter_acceleration(x_axis_acceleration, watch_samples_counter)
            y_axis_acceleration.append(inbyte[bytes_to_read-2])
            filtering.filter_acceleration(y_axis_acceleration, watch_samples_counter)
            z_axis_acceleration.append(inbyte[bytes_to_read-1])
            filtering.filter_acceleration(z_axis_acceleration, watch_samples_counter)
            time_final = time.time()
            x_0 = normalizados.filtrar_ceros(x_axis_acceleration)
            y_0 = normalizados.filtrar_ceros(y_axis_acceleration)
            z_0 = normalizados.filtrar_ceros(z_axis_acceleration)

            #report.record_data('dataPython.txt',time_final - time_initial, x_axis_acceleration[watch_samples_counter],
                              # y_axis_acceleration[watch_samples_counter], z_axis_acceleration[watch_samples_counter])

            #report.record_for_training(x_axis_acceleration[watch_samples_counter],
                                 #      y_axis_acceleration[watch_samples_counter],
                                  #     z_axis_acceleration[watch_samples_counter])

            test_digits = test_digits + [x_0[watch_samples_counter], y_0[watch_samples_counter], z_0[watch_samples_counter]]
            cont_predicciones = 0
            if watch_samples_counter>=8 and higher_index <= len(test_digits):

                # Load the dataset
                test_data = normalize(test_digits[lower_index:higher_index])
                #print(test_data)
                # Predict values
                test_predicted = classifier.predict(test_data)
                test_probabilities = classifier.predict_proba(test_data)

                #report.record_probabilities(int(test_predicted[0]), test_probabilities, test_digits[lower_index:higher_index])
                #print(test_digits)
                if test_predicted == 1:
                    lower_index += 30
                    higher_index += 30
                    print('arriba')
                    n_pruebas += 1
                    print(n_pruebas)


                    if modo == True: #movimientos verticales
                        if drone.state.fly_mask == False and old_prediction[cont_predicciones-1]==1: #está en el suelo y el movimiento anterior ha sido hacia arriba (2 arriba pa despegar)
                            drone.takeoff()
                            alertamovimiento.play()
                            time.sleep(0.1)
                            #time.sleep(2)
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
                    cont_predicciones+=1
                    #t1=time.time()
                elif test_predicted == 2:
                    print('abajo')
                    lower_index += 30
                    higher_index += 30
                    n_pruebas += 1
                    print(n_pruebas)

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
                    #graphic.restore_color()
                    #lower_index += 3
                    #higher_index += 3
                elif test_predicted == 3:
                    print('derecha')
                    lower_index += 30
                    higher_index += 30
                    n_pruebas += 1
                    print(n_pruebas)
                    cont_predicciones+=1
                    time2=time.time()
                    while time.time()-time2<=2:
                        drone.move(right=0.1)
                    alertamovimiento.play()
                    time.sleep(0.1)
                elif test_predicted == 4:
                    print('izquierda')
                    lower_index += 30
                    higher_index += 30
                    n_pruebas += 1
                    time1=time.time()
                    cont_predicciones+=1
                    while time.time()-time1<=2:
                        drone.move(left=0.1)
                    print(n_pruebas)
                    alertamovimiento.play()
                    time.sleep(0.1)
                elif test_predicted == 5:
                    print('modo 2')
                    lower_index += 30
                    higher_index += 30
                    n_pruebas += 1
                    if drone.state.fly_mask==True and old_prediction[cont_predicciones - 1] == 5:
                        drone.land()
                        alertamovimiento.play()
                        time.sleep(0.1)
                    else:
                        modo = not modo
                        alertamodo.play()
                        time.sleep(0.1)
                    cont_predicciones+=1

                    print(n_pruebas)
                else:
                    print('random')
                    lower_index += 30
                    higher_index += 30
                    n_pruebas += 1
                    print(n_pruebas)
                    cont_predicciones+=1
                if cont_predicciones>=1:
                    old_prediction.append(int(test_predicted))
                    #print(old_prediction)
            graphic.plot_data(x_axis_acceleration[watch_samples_counter], y_axis_acceleration[watch_samples_counter])

        plt.pause(0.05)  # 50m

        #report.next_line()

        k +=1   #communication.close_serial_port()