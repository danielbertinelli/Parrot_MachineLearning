from threading import Thread
import time
import warnings
from libs import communications, filterings, graphics, datalog, normalizado
import openpyxl


warnings.filterwarnings("ignore", category=DeprecationWarning)
communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()
graphic = graphics.GraphicsManager()
report = datalog.DatalogManager()
filtros = normalizado.Normalizador()
communication.open_serial_port()
graphic.set_plot_parameters()


x = []
y = []
z = []
digitos_prediccion=[]

def adquieredatos():
    tiempo_inicial_adquisicion = time.time()
    while(len(digitos_prediccion)) <= 30:
        communication.send_data_request()

        time.sleep(0.25)


def lee_y_escribe(index):
    contador=-1
    tiempo_inicial_lectura=time.time()
    n_iteraciones = 0
    fila=0
    etiqueta = 1
    while (len(digitos_prediccion)) <= 30:
        bytestoread, inbyte = communication.read_data()

        if (bytestoread == 7) or (bytestoread == 14):
            contador+=1
            print('Thread 2-inbyte: ' + str(inbyte) + ' length inbyte ' + str(len(inbyte)) +' bits to read '+str(bytestoread))
            x.append((inbyte[bytestoread - 3]))
            y.append((inbyte[bytestoread - 2]))
            z.append((inbyte[bytestoread - 1]))
            print('contador de thread 2 ' + str(contador))
            filtering.filter_acceleration(x, contador)
            filtering.filter_acceleration(y, contador)
            filtering.filter_acceleration(z, contador)
            digitos_prediccion.append(x[contador])
            digitos_prediccion.append(y[contador])
            digitos_prediccion.append(z[contador])
            print('Longitud de digitos prediccion: ' + str(len(digitos_prediccion)))
            if len(digitos_prediccion)==30:
                digitos_prediccion.append(index)
                doc = openpyxl.load_workbook('BaseDatos.xlsx')
                hoja = doc.get_sheet_by_name('Hoja1')
                ws=doc.active
                ws.append(digitos_prediccion)
                doc.save('BaseDatos.xlsx')
        time.sleep(0.25)


peticion_aceleracion = Thread(target=adquieredatos)
lectura_almacenado = Thread(target=lee_y_escribe,args=(0,))#

peticion_aceleracion.start()
lectura_almacenado.start()