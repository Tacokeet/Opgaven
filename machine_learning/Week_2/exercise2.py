# MACHINE LEARNING OPGAVE WEEK 2

import numpy as np
from random import randint
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import sys
import pickle

from uitwerkingen import *

# Helperfuncties die nodig zijn om de boel te laten werken
# Hier hoef je niets aan te veranderen, maar bestudeer de 
# code om een beeld te krijgen van de werking hiervan.

def randInitializeWeights(in_conn, out_conn):
    W = np.zeros((out_conn, 1 + out_conn))
    epsilon_init = 0.12
    #W = rand(L_out, 1 + L_in) * 2 * epsilon_init - epsilon_init;
    W = np.random.rand(out_conn, 1+in_conn) * 2 * epsilon_init - epsilon_init
    return W

def displayData(X):
    m,n = X.shape
    for idx in range(0, m):
        plt.subplot(5, 5, idx+1)
        x = X[idx,:].reshape(20,20)
        plt.tick_params(which='both',left=False, bottom=False, top=False, labelleft=False, labelbottom=False)
        plt.imshow(x, cmap='gray', interpolation='nearest');

    plt.show()

itr = 1
def callbackF(Xi):
    global itr
    print ("iteration {}".format(itr))
    itr += 1


def nnCostFunction(Thetas, X, y):
    global input_layer_size, hidden_layer_size, num_labels
    size = hidden_layer_size * (1+input_layer_size) # +1 want de bias-node zit wel in de matrix
    Theta1 = Thetas[:size].reshape(hidden_layer_size, input_layer_size+1)
    Theta2 = Thetas[size:].reshape(num_labels, hidden_layer_size+1)
    J = computeCost(Theta1, Theta2, X, y)
    grad1, grad2 = nnCheckGradients(Theta1, Theta2, X, y)
    return J, np.concatenate( (grad1.flatten(), grad2.flatten()) ) 


#Laden van de data en zetten van de variabelen.
with open ('week2_data.pkl','rb') as f:
    data = pickle.load(f)

X,y = data['X'], data['y']

#Zetten van belangrijke variabelen
m,n = X.shape # aantal datapunten in de trainingsset
input_layer_size  = 400;  # 20x20 input plaatjes van getallen
hidden_layer_size = 25;   # 25 hidden units
num_labels = 10;          # 10 labels, from 1 to 10
                          # (note that we have mapped "0" to label 10)


# ========================  OPGAVE 1 ======================== 
rnd = randint(0, X.shape[0])
print ("Tekenen van data op regel {}".format(rnd))
if (len(sys.argv)>1 and sys.argv[1]=='skip') :
    print ("Slaan we over")
else:
    hyp = y[rnd]
    if (hyp==10): hyp=0
    print ("Dit zou een {} moeten zijn.".format(hyp))
    plotNumber(X[rnd,:])

input ("Druk op Return om verder te gaan...") 


# ========================  OPGAVE 2a ======================== 
print ("")
print ("Sigmoid-functie met een relatief groot negatief getal zou bijna 0 moeten zijn")
print ("Sigmoid van -10 = {}".format(sigmoid(-10)))

print ("Sigmoid-functie van 0 zou 0,5 moeten zijn.")
print ("Sigmoid van 0 = {}".format(sigmoid(0)))

print ("Sigmoid-functie met een relatief groot positief getal zou bijna 1 moeten zijn")
print ("Sigmoid van 10 = {}".format(sigmoid(10)))

print ("Simoid aangeroepen met 1×3 vector [-10, 0, 10]")
print (sigmoid(np.matrix( [-10, 0, 10] )))
print ("Simoid aangeroepen met 3×1 vector [-10, 0, 10]")
print (sigmoid(np.matrix( ([-10], [0], [10]) )))

input ("Druk op Return om verder te gaan...") 

# ========================  OPGAVE 2b ======================== 
print ("")
print ("Aanroepen van de methode predictNumber met de y-vector")
print ("en het weergeven van de dimensionaliteit van het resultaat")
matr = get_y_matrix(y, m)
print (matr.shape)
print ("Dit zou (5000,10) moeten zijn.")
input ("Druk op Return om verder te gaan.")


# ========================  OPGAVE 2c ======================== 
print("")
print ("Zetten van initiële waarden van de Theta's.")
Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size)
Theta2 = randInitializeWeights(hidden_layer_size, num_labels)

print ("Aanroepen van de methode predictNumber")
pred = np.argmax(predictNumber(Theta1,Theta2,X), axis=1).reshape(m,1)
cost = computeCost(Theta1, Theta2, X, y)

print ("De kosten die gemoeid zijn met de huidige waarden van Theta1 en Theta2 zijn {}".format(cost))
print ("Dit zou zo rond de 7 moeten liggen.")
acc = np.count_nonzero([pred - y == 0])
print ("Correct geclassificeerd: {}".format(acc))
print ("De huidige accuratessse van het netwerk is {} %".format(100 * acc/ m))
input ("Druk op Return om verder te gaan.")

# ========================  OPGAVE 3 ======================== 
print ("")
print ("Aanroepen van de methode sigmoidGradient met de waarden [-1, -0.5, 0, 0.5, 1 ]")
print (sigmoidGradient(np.array([ [-1, -0.5, 0, 0.5, 1 ] ])))
print ("Dit zou als resultaat de volgende lijste moeten hebben")
print ("[ 0.19661193  0.23500371  0.25  0.23500371  0.19661193]")
input ("Druk op Return om verder te gaan...")

print ("")
print ("Aanroepen van de methode nnCheckGradients met initiële waarden van de Theta's.")
g1, g2 =  nnCheckGradients(Theta1, Theta2, X, y)
print ("De totale som van de eerste gradiënt-matrix is {}".format(sum(sum(g1))))
print ("De totale som van de tweede gradiënt-matrix is {}".format(sum(sum(g2))))
input ("Druk op Return om verder te gaan...")

# ========================  OPGAVE 4 ======================== 

init_params = np.concatenate( (Theta1.flatten(), Theta2.flatten()) )
args = ( X, y)
print ("")
print ("Gebruik scipy.optimize.minimize om het netwerk te trainen...")
res = minimize(nnCostFunction, init_params, args=args, method='CG', callback=callbackF, jac=True, options={'maxiter':30,'disp':True})
size = hidden_layer_size * (input_layer_size+1) #voor de bias-node die wel in de matrix zit maar niet geplot moet worden
res_Theta1 = res['x'][:size].reshape(hidden_layer_size, input_layer_size+1)
res_Theta2 = res['x'][size:].reshape(num_labels, hidden_layer_size+1)

print ("Training compleet. ")
cost = computeCost(res_Theta1, res_Theta2, X, y)
print ("De totale kost is nu {}".format(cost))

cost = computeCost(res_Theta1, res_Theta2, X, y) 
print ("De kosten die gemoeid zijn met de huidige waarden van Theta1 en Theta2 zijn {}".format(cost))
print ("Dit zou een stuk lager moeten zijn dan in het begin.")

pred = np.argmax(predictNumber(res_Theta1,res_Theta2,X), axis=1)+1
pred = pred.reshape(m,1)
acc = np.count_nonzero([pred - y == 0])
print ("correct geclassificeerd: {}".format(acc))
print ("De huidige accuratessse van het netwerk is {} %".format(100 * acc/ m))
print ("Dat zou een stuk hoger moeten zijn dan in het begin.")
print ("Plotten van de waarden van de gewichten in de verborgen laag (hidden layer)")

displayData(res_Theta1[:,1:]) 