#script que convierte todos los ficheros con una fila de información en un fichero con todas las lineas
from libs import datalog
report = datalog.DatalogManager()

index = 1
ficherofinal = open('/home/icarus/Descargas/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/Normalizado/Random/LizqSUMnormalizado.txt','w')

filename = 'Lrandomnormalizado'

while index <= 100:
    ficheroactual = open('/home/icarus/Descargas/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/Normalizado/Random/'+filename+str(index))
    ficherofinal.write(ficheroactual.read())
    ficherofinal.write('\n')
    index += 1

def escribevector_CSV(vector,filename):
    print('len del vector de entrada ' +str(len(vector)))
    ficherofinal=open(filename,'w')
    i=-1

    while i <<len(vector):
        i+=1
        print('I de escribe vector '+str(i))
        print(str(vector[i]))
        ficherofinal.write(str(vector[i]) + ';')

        ficherofinal.write('\n')
