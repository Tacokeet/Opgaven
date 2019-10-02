import numpy as np

# Naieve implementatie


L1 = np.array([0.5, 2])
L2 = np.array([2, 0])
L3 = np.array([0, 0.5])


p1 = np.array([1,1])
p2 = np.array([4,1])
p3 = np.array([3,4])
p4 = np.array([4,4])

# De voorspelling van punt p1 door hypothese L1
fout_van_hypothese_L1 = L1[0] + p2[0]*L1[1]
print(fout_van_hypothese_L1)

verschil_van_punt_en_L1 = (L1[0] + p2[0]*L1[1]) - p2[1]
print(verschil_van_punt_en_L1)

# Berekenen van de totale fout voor hypthese L1
J_val1 = 0
for p in [p1, p2, p3, p4]:
    h = L1[0] + p[0]*L1[1]      #waarde voorspeld door hypothese L1
    delta = (h - p[1]) ** 2     #kwadrateren van het verschil met de actuele waarde
    J_val1 += delta             #dit verschil optellen bij het totaal

J_val1 = J_val1/4               #delen door het aantal observaties

print("Totale fout voor hypthese L1: {}".format(J_val1))


# Vectoriale implementatie
data = np.array([ [1,1], [4,1],[3,4],[4,4] ]) # 4 bij 2 dimensionale array
print("Data:\n{}".format(data))
data = np.c_[np.ones(4), data]
# Eerste twee kolommen van deze matrix zijn de x matrix, de laatste kolom is de y matrix
print("Data:\n{}".format(data))
# Get the x matrix
X=data[:, 0:2]
print("X-matrix:\n{}".format(X))
Y=data[:, [2]]
print("Y-matrix:\n{}".format(Y))

theta = np.array([ [0.5, 2] ]) # = L1
print("Theta:\n{}".format(theta))

# Dot operatie A . B
predictions = np.dot(X, theta.T)
print("Result dot operation: {}".format(predictions))

print("Opvragen dimensie van matrix met .shape: ")
print(Y.shape)

errors = (predictions - Y) ** 2
print("errors: {}".format(errors))

J_val = sum(errors)/4
print("Totale fout: {}".format(J_val))
