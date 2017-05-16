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
