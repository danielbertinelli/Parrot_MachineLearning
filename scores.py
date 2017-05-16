from sklearn.metrics import classification_report
import numpy as np
import time
import matplotlib.pyplot as plt
import warnings
import sys
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import zero_one_loss
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.preprocessing import normalize
from sklearn.model_selection import cross_val_score, cross_val_predict, ShuffleSplit, train_test_split,validation_curve

#Datos de la base de datos para realizar la clasificación
datos = np.genfromtxt('/Users/Adrián/eZ430-Chronos-master (2)/data/MuestrasBDD/ManoIZQ/BaseDato.csv', delimiter = ';')
digitos = normalize(datos[:, :-1])
etiquetas = datos[:, -1]
x_train, x_eval, y_train, y_eval = train_test_split(digitos, etiquetas, test_size=0.5,
                                                    train_size=0.5,
                                                    random_state=1982)
#Creamos clasificador

#clf_neuronal = MLPClassifier(solver='lbfgs', alpha=0.000000000001, early_stopping=True, validation_fraction=0.15, max_iter=300)
clf_decisiontree = DecisionTreeClassifier(max_depth=9, min_samples_leaf=1)
clf_adaboostdisc = AdaBoostClassifier(base_estimator=clf_decisiontree,n_estimators=400,algorithm="SAMME")
clf_gradientboost = GradientBoostingClassifier(n_estimators=400)
#Entrenamos el clasificador

#clf_neuronal.fit(x_train,y_train)
clf_decisiontree.fit(x_train,y_train)
clf_adaboostdisc.fit(x_train,y_train)
clf_gradientboost.fit(x_train,y_train)
#Obtenemos los aciertos que tienen cada uno de los clasificadores

expected = y_eval
#predicted_neu = clf_neuronal.predict(x_eval)
#predicted_tree = clf_decisiontree.predict(x_eval)
predicted_ada = clf_adaboostdisc.predict(x_eval)

print("precisión entranamiento: {0: .2f}".format(
        clf_gradientboost.score(x_train, y_train)))
print("precisión test: {0: .2f}".format(
        clf_gradientboost.score(x_eval, y_eval)))
train_prec =  []
eval_prec = []
max_deep_list = list(range(1, 400))
print(clf_gradientboost.get_params().keys())
train_prec, eval_prec = validation_curve(estimator=clf_gradientboost, X=x_train,
                                        y=y_train, param_name='n_estimators',
                                        param_range=max_deep_list, cv=5)

train_mean = np.mean(train_prec, axis=1)
train_std = np.std(train_prec, axis=1)
test_mean = np.mean(eval_prec, axis=1)
test_std = np.std(eval_prec, axis=1)
plt.plot(max_deep_list, train_mean, color='r', marker='o', markersize=5,
         label='entrenamiento')
plt.fill_between(max_deep_list, train_mean + train_std,
                 train_mean - train_std, alpha=0.15, color='r')
plt.plot(max_deep_list, test_mean, color='b', linestyle='--',
         marker='s', markersize=5, label='evaluacion')
plt.fill_between(max_deep_list, test_mean + test_std,
                 test_mean - test_std, alpha=0.15, color='b')
plt.title('GradientBoost Classifier')
plt.grid()
plt.legend(loc='center right')
plt.xlabel('numero de clasificadores')
plt.ylabel('Precision')
plt.show()
train_prec =  []
eval_prec = []
max_deep_list = list(range(3, 50))

train_prec, eval_prec = validation_curve(estimator=clf_adaboostdisc, X=x_train,
                                        y=y_train, param_name='n_estimators',
                                        param_range=max_deep_list, cv=5)

train_mean = np.mean(train_prec, axis=1)
train_std = np.std(train_prec, axis=1)
test_mean = np.mean(eval_prec, axis=1)
test_std = np.std(eval_prec, axis=1)
plt.plot(max_deep_list, train_mean, color='r', marker='o', markersize=5,
         label='entrenamiento')
print('hola')
plt.fill_between(max_deep_list, train_mean + train_std,
                 train_mean - train_std, alpha=0.15, color='r')
plt.plot(max_deep_list, test_mean, color='b', linestyle='--',
         marker='s', markersize=5, label='evaluacion')
plt.fill_between(max_deep_list, test_mean + test_std,
                 test_mean - test_std, alpha=0.15, color='b')
plt.title('AdaBoost Classifier Discreto')
plt.grid()
plt.legend(loc='center right')
plt.xlabel('numero de clasificadores')
plt.ylabel('Precision')
plt.show()
# #Muestramos los resultados
#
# print("Report de clasificación para MLP Classifier:\n\%s\n"
#       % (metrics.classification_report(expected, predicted_neu)))
# print("Report de clasificación para Decision Tree:\n%s\n"
#       % (metrics.classification_report(expected, predicted_tree)))
# print("Report de clasificación para AdaBoost Discrete:\n%s\n"
#       % (metrics.classification_report(expected, predicted_ada)))
#
# #Matrices de Confusión
#
# print("Confusion matrix Decision Tree:\n%s" % metrics.confusion_matrix(expected, predicted_tree))
# print("Confusion matrix MLP Classifier:\n%s" % metrics.confusion_matrix(expected, predicted_neu))
# print("Confusion matrix AdaBoost Discrete:\n%s" % metrics.confusion_matrix(expected, predicted_ada))
#
#
# #CrossValidation Scores
#
# cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=0)
# cv_tree = cross_val_score(clf_decisiontree, x_eval,y_eval, cv=cv)
# cv_adaboost = cross_val_score(clf_adaboostdisc,x_eval,y_eval,cv=cv)
# #cv_neu = cross_val_score(clf_neuronal,x_eval,y_train,cv=cv)
#
# print("Cross Validation Scores Decision Tree:\n%s\n"
#       % (cv_tree))
# #print("Cross Validation Scores MLP Classifier:\n%s\n"
#  #     % (cv_neu))
# print("Cross Validation AdaBoost Discrete:\n%s\n"
#       % (cv_adaboost))