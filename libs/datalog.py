# datalog.py
# Mónica Milán (@mncmilan)
# mncmilan@gmail.com
# http://steelhummingbird.blogspot.com.es/

# Library that contains all necessary methods in order to store data in a text file.

class DatalogManager():

    def record_data(self, filename, parameter, x_axis_acceleration, y_axis_acceleration, z_axis_acceleration):
        archi = open('home/icarus/Descargas/eZ430-Chronos-master (2)/data/PruebasML/' + filename, 'a')
        data= str(parameter) + '       ' + str(x_axis_acceleration) + '      ' + str(y_axis_acceleration)+ '      ' + str(z_axis_acceleration)
        archi.write(data)
        archi.write('\n')
        archi.close()

    def create_file(self, filename):
        archi = open('/Users/Usuario/Desktop/Daniel/TFG/Codigo/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/'+filename, 'a')
        archi.close()

    def record_for_training(self, filename, index, x_axis_acceleration, y_axis_acceleration, z_axis_acceleration):
        archi = open('/Users/Usuario/Desktop/Daniel/TFG/Codigo/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/'+filename+index, 'a')
        data = str(x_axis_acceleration) + ';' + str(y_axis_acceleration) + ';' + str(z_axis_acceleration)+';'
        archi.write(data)
        archi.close()
    def record_for_training2(self, filename, index, muestraZY,muestraZX):
        archi = open('/home/icarus/Descargas/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/MuestrasZY/'+filename+index, 'a')
        data = str(muestraZY) + ';' + str(muestraZX) + ';'
        archi.write(data)
        archi.close()
    def next_line(self,filename,index):
        archi = open('/Users/Usuario/Desktop/Daniel/TFG/Codigo/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/'+filename+index, 'a')
        archi.write('\n')
        archi.close()

    def record_probabilities(self, prediction, probability,position):
        archi = open('home/icarus/Descargas/eZ430-Chronos-master (2)/data/PruebasML/probabilities.txt', 'a')
        data = str(prediction) + '         ' + str(probability[0][0])+ '         ' + str(probability[0][-1])+ '         ' + str(position)
        archi.write(data)
        archi.write('\n')
        archi.close()


