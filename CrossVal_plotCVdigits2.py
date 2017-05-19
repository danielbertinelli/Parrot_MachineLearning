print(__doc__)

from sklearn.preprocessing import normalize
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import datasets


vector_barrido = []
mlp = MLPClassifier(solver='lbfgs', early_stopping=False)
datos = np.genfromtxt('BaseDatos.csv', delimiter = ';')
X = (datos[:, :-1])
y = datos[:, -1]
for i in range(25):
    i+=1
    vector_barrido.append(i)
hiddenlayers = vector_barrido

scores = list()
scores_std = list()
for hl in hiddenlayers:
    mlp.hidden_layer_sizes = hl
    this_scores = cross_val_score(mlp, X, y, n_jobs=1)
    scores.append(np.mean(this_scores))
    scores_std.append(np.std(this_scores))

# Do the plotting
import matplotlib.pyplot as plt
plt.figure(1, figsize=(4, 3))
plt.clf()
plt.plot(hiddenlayers, scores,label='CV score')
plt.plot(hiddenlayers, np.array(scores) + np.array(scores_std), 'b--',label='CV máx score')
plt.plot(hiddenlayers, np.array(scores) - np.array(scores_std), 'b--',label='CV min score')
locs,labels = plt.yticks()
plt.legend()
plt.yticks(locs, list(map(lambda x: "%g" % x, locs)))
plt.ylabel('Valoración CV')
plt.xlabel('Número de Capas ocultas')
plt.ylim(0, 1.1)
plt.show()