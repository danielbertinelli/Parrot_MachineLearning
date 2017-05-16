# free_mode.py
# Mónica Milán (@mncmilan)
# mncmilan@gmail.com
# http://steelhummingbird.blogspot.com.es/

# This code obtains acceleration data from eZ430-Chronos watch by Texas Instruments, then it eliminates the noise in X
# and Y axis and finally it plots the resulting values.

import matplotlib.pyplot as plt
from libs import communications, filterings, graphics, modes, datalog, normalizado
import time


communication = communications.CommunicationManager()
filtering = filterings.FilteringManager()
graphic = graphics.GraphicsManager()
report = datalog.DatalogManager()
mode = modes.ModesManager()
filtros = normalizado.Normalizador()
index = 2
#report.create_file('Lmodo')
class FreeMovement():
    communication.open_serial_port()

    watch_samples_counter = -1

    x_axis_acceleration = []
    y_axis_acceleration = []
    z_axis_acceleration = []

    x_axis_limited_acceleration = 0
    y_axis_limited_acceleration = 0

    graphic.set_plot_parameters()
    initial_time = time.time()
    time_limit = 5
    while watch_samples_counter <= 8:
        bytes_to_read = communication.send_data_request()
        inbyte = communication.read_data(bytes_to_read)
        print('bytes to read '+str(bytes_to_read))
        print(inbyte)
        if (bytes_to_read >= 7 and inbyte[3] == 1) or (bytes_to_read == 14 and inbyte[10] == 1):
            watch_samples_counter += 1
            x_axis_acceleration.append(inbyte[bytes_to_read-3])
            filtering.filter_acceleration(x_axis_acceleration, watch_samples_counter)
            y_axis_acceleration.append(inbyte[bytes_to_read-2])
            filtering.filter_acceleration(y_axis_acceleration, watch_samples_counter)
            z_axis_acceleration.append(inbyte[bytes_to_read-1])
            filtering.filter_acceleration(z_axis_acceleration, watch_samples_counter)
            graphic.plot_data(x_axis_acceleration[watch_samples_counter], y_axis_acceleration[watch_samples_counter])
            #report.record_data('Lizq', watch_samples_counter, x_axis_acceleration[watch_samples_counter], y_axis_acceleration[watch_samples_counter], z_axis_acceleration[watch_samples_counter])
        #print(x_axis_acceleration)
        plt.pause(0.01)  # 10ms

    print(time.time()-initial_time)
    # Filtrado de 0s.
    x_0 = filtros.filtrar_ceros(x_axis_acceleration)
    y_0 = filtros.filtrar_ceros(y_axis_acceleration)
    z_0 = filtros.filtrar_ceros(z_axis_acceleration)
    cont = 0
    print(len(x_axis_acceleration))
    print(len(y_axis_acceleration))
    print(len(z_axis_acceleration))
    #while cont <= (len(x_0)-1):
        #report.record_data('Larribafiltrado', cont, x_0[cont], y_0[cont], z_0[cont])
        #report.record_for_training('Lrandomfiltrado', str(index), x_0[cont], y_0[cont], z_0[cont])
        #cont += 1

    # Normalizado entre -1 y 1.
    #[x_norm, y_norm, z_norm] = filtros.normalizar(x_axis_acceleration, y_axis_acceleration, z_axis_acceleration)
    #cont = 0
    #while cont <= (len(x_axis_acceleration)-1):
        #report.record_data('Larribanormalizado', cont, x_norm[cont], y_norm[cont], z_norm[cont])
        #report.record_for_training('Lrandomnormalizado', str(index), x_norm[cont], y_norm[cont], z_norm[cont])
        #cont += 1
    # communication.close_serial_port()
    while cont <= (len(x_0)-1):
        report.record_for_training('Larriba', str(index), x_0[cont], y_0[cont], z_0[cont])
        cont +=1
    report.next_line('Larriba',str(index))
