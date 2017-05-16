# Parrot_MachineLearning
Control del Parrot 2.0 de ARDrone gracias a un reloj con acelerómetro (eZ430-Chronos de Texas Instruments) y machine learning
El código presente en este repositorio permite actualmente iniciar la conexión con el reloj, tomar muestras, leerlas, entrenar un algoritmo clasificador (Machine Learning) y clasificar las muestras obtenidas con el reloj.

-La carpeta libs contiene todos los scripts necesarios para realizar la adquisición de los datos, filtrado de ruido y graficado de las muestras, cortesía de Mónica Milán (@mncmilan).

-Los archivos BaseDatos.csv y BaseDatos.xlsx contienen muestras guardadas de diferentes movimientos etiquetados por las cifras del 0 al 5. Siendo 0 movimento random, 1 arriba, 2 abajo, 3 giro derecha, 4 giro izquierda y 5 cambio de modo(giro completo hacia la izquierda).

-El script pruebas-threading3.py contiene el código necesario para iniciar la adquisición de datos, el entrenamiento del clasificador y la clasificación de los datos adquiridos.

-El script basedatosthreading.py permite introducir nuevas muestras a la base de datos (BaseDatos.xlsx), esta base de datos debe ser guardada como .csv (MS-DOS) posteriormente.

-El script pruebasvarias.py permite realizar mesuras de precisión y validación cruzada de diferentes algoritmos clasificadores.
