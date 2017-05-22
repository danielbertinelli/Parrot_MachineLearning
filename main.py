from libs import gestiondatos,algoritmos
from threading import Thread
import time




i=input('Elige entre las dos opciones: [0]Configuración predeterminada, [1]Configuración personalizada:')
i=int(i)
gestionador = gestiondatos.GestiondeDatos()
print('Cargado gestionador')
if i==0:
    print('Modo predeterminado elegido')
    algoritmos.Algoritmos().Entrena_algoritmo('BaseDatos.csv')
    print('Algoritmo MLP entrenado')
    # Declaración de los hilos
    peticion_aceleracion = Thread(target=gestionador.adquieredatos)
    lectura_orden = Thread(target=gestionador.lee_plotea_ordena)  #

    #iniciar los hilos
    peticion_aceleracion.start()
    lectura_orden.start()



elif i ==1:
    print('Modo personalizado seleccionado')
    print ()
    numero_muestras = input('A continuación se procederá a introducir las muestras personalmente, elige el número de muestras (multiplo de 6): ')
    numero_muestras=int(numero_muestras)
    print('El numero elegido es :'+str(numero_muestras)+' por lo tanto se introducirán '+str(numero_muestras/6)+'muestras.')
    time.sleep(1)

    #Declaración de los hilos
    peticion_aceleracion = Thread(target=gestionador.adquieredatos3,args=(numero_muestras,))
    guardar_random = Thread(target=gestionador.lee_y_guarda,args=(0,numero_muestras,))
    guardar_arriba = Thread(target=gestionador.lee_y_guarda, args=(1, numero_muestras,))
    guardar_abajo = Thread(target=gestionador.lee_y_guarda, args=(2, numero_muestras,))
    guardar_dcha = Thread(target=gestionador.lee_y_guarda,args=(3,numero_muestras,))
    guardar_izq = Thread(target=gestionador.lee_y_guarda, args=(4, numero_muestras,))
    guardar_modo2 = Thread(target=gestionador.lee_y_guarda,args=(5,numero_muestras,))
    print('MOVIMIENTOS ALEATORIOS')
    in_=input('Pulsa enter para empezar, descansa si lo necesitas.')
    peticion_aceleracion.start()
    guardar_random.start()
    guardar_random.join()
    print('MOVIMIENTOS HACIA ARRIBA')
    in_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
    guardar_arriba.start()
    guardar_arriba.join()
    print('MOVIMIENTOS HACIA ABAJO')
    in_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
    guardar_abajo.start()
    guardar_abajo.join()
    print('MOVIMIENTOS HACIA LA DERECHA')
    in_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
    guardar_dcha.start()
    guardar_dcha.join()
    print('MOVIMIENTOS HACIA LA IZQUIERDA')
    in_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
    guardar_izq.start()
    guardar_izq.join()
    print('MOVIMIENTOS CAMBIO DE MODO')
    in_ = input('Pulsa enter para empezar, descansa si lo necesitas.')
    guardar_modo2.start()
    guardar_modo2.join()
    if guardar_modo2.isAlive()==False:
        print('Fin de la recogida de muestras')
