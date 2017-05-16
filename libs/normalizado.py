#Función que elimina los 0s invalidos de los vectores de aceleración y
#escala los valores entre -1 y 1, utilizando el valor máximo para los valores positivos
#y el mínimo para los valores negativos.

class Normalizador():


    def filtrar_ceros(self, vector_aceleracion):

        index = len(vector_aceleracion)
        cont = 0

        while cont <= index-1:
            if (cont > 1) and (vector_aceleracion[cont] == 0):
                if (cont == index-1):
                    vector_aceleracion[cont] == vector_aceleracion[cont]

                elif (vector_aceleracion[cont-1] == 0) or (vector_aceleracion[cont+1] == 0):
                    vector_aceleracion[cont] == vector_aceleracion[cont]

                else:
                    dif = vector_aceleracion[cont+1]-vector_aceleracion[cont-1]
                    adit = dif/2
                    vector_aceleracion[cont] = vector_aceleracion[cont-1] + adit

            cont += 1
        return vector_aceleracion

    def normalizar(self, vector_aceleracionx, vector_aceleraciony, vector_aceleracionz):
        index = len(vector_aceleracionx)
        cont = 0
        maximo = max(vector_aceleracionx + vector_aceleraciony + vector_aceleracionz)
        minimo = min(vector_aceleracionx + vector_aceleraciony + vector_aceleracionz)*-1
        if (minimo == 0) or (maximo == 0):
            minimo += 1
            maximo += 1
        print(maximo)
        print(minimo)
        while cont <= index-1:
            if vector_aceleracionx[cont] >= 0:

                vector_aceleracionx[cont] = round(vector_aceleracionx[cont]/maximo, 4)

                #print(vector_aceleracion[cont])

                cont += 1
            else:
                vector_aceleracionx[cont] = round(vector_aceleracionx[cont]/minimo, 4)

                #print(vector_aceleracion[cont])
                cont += 1
        cont = 0
        while cont <= index-1:
            if vector_aceleraciony[cont] >= 0:

                vector_aceleraciony[cont] = round(vector_aceleraciony[cont]/maximo, 4)

                #print(vector_aceleracion[cont])

                cont += 1
            else:
                 vector_aceleraciony[cont] = round(vector_aceleraciony[cont]/minimo, 4)
                 cont += 1

        cont = 0
        while cont <= index-1:
            if vector_aceleracionz[cont] >= 0:
                vector_aceleracionz[cont] = round(vector_aceleracionz[cont]/maximo, 4)
                cont += 1
            else:
                vector_aceleracionz[cont] = round(vector_aceleracionz[cont]/minimo, 4)
                cont += 1

        return vector_aceleracionx, vector_aceleraciony, vector_aceleracionz
