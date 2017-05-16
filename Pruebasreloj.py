import matplotlib.pyplot as plt
from libs import communications, filterings, graphics, modes, datalog, normalizado
import time

communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()
graphic = graphics.GraphicsManager()
report = datalog.DatalogManager()
mode = modes.ModesManager()
filtros = normalizado.Normalizador()
communication.open_serial_port()
tiempo_inicial = time.time()



x1=[]
y1=[]
z1=[]
graphic.set_plot_parameters()
contador=0
while len(x1)<=9:
    bytes_to_read = communication.send_data_request()
    inbyte = communication.read_data(bytes_to_read)
    time.sleep(0.12)

    if (bytes_to_read >= 7 and inbyte[3] == 1) or (bytes_to_read == 14 and inbyte[10] == 1):
        x1.append(inbyte[bytes_to_read-3])
        if x1[contador]>127:
            x1[contador]=(255 - x1[contador] + 1) * -1
        y1.append(inbyte[bytes_to_read - 2])
        if y1[contador]>127:
            y1[contador]=(255 - y1[contador] + 1) * -1
        z1.append(inbyte[bytes_to_read - 1])
        if z1[contador]>127:
            z1[contador]=(255 - z1[contador] + 1) * -1
        graphic.plot_data(x1[len(x1)-1], y1[len(x1)-1])
        contador+=1
    plt.pause(0.02)
print(time.time()-tiempo_inicial)
print(x1)
print(y1)
print(z1)