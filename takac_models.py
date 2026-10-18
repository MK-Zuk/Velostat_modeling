import numpy as np

# ----------------------------------------------------
# Funkcje pomocnicze
# ----------------------------------------------------

def relu_numpy(x):
    return np.maximum(0, x)

def x_save(x):
    return np.maximum(x, 0.001)


# ----------------------------------------------------
# Podstawowe stałe dla równania Takaca ZORC
# ----------------------------------------------------

def takac_b1(xm, a0):
    return (np.tanh(xm+a0) - np.tanh(xm-a0))/2

def takac_b1e(xm, a0, A=1):
    return A*(np.tanh(xm+a0) - np.tanh(xm-a0))/2

def takac_b3(xm, a0, d0):
    return (np.tanh(xm+d0+a0) - np.tanh(xm+d0-a0))/2

def takac_b4(xm, a0, d0):
    return (np.tanh(-xm+d0+a0) - np.tanh(-xm+d0-a0))/2

def takac_bu(x, xm, a0, d0):
    b3 = takac_b3(xm, a0, d0)
    b4 = takac_b4(xm, a0, d0)
    b3_numerator = np.tanh(-xm+d0-a0)
    b3_denominator = (np.tanh(-xm+d0-a0) - np.tanh(xm+d0-a0))
    b4_numerator = (np.tanh(xm+d0-a0)-np.tanh(x-a0))
    b4_denominator = (np.tanh(xm+d0-a0)-np.tanh(-xm+d0-a0))
    return ((b3*b3_numerator/b3_denominator) + (b4*b4_numerator/b4_denominator))

def takac_bd(x, xm, a0, d0):
    b3 = takac_b3(xm, a0, d0)
    b4 = takac_b4(xm, a0, d0)
    b3_numerator = (np.tanh(-xm+d0+a0)-np.tanh(x+a0))
    b3_denominator = (np.tanh(-xm+d0+a0) - np.tanh(xm+d0+a0))
    b4_numerator = (np.tanh(xm+d0+a0)-np.tanh(x+a0))
    b4_denominator = (np.tanh(xm+d0+a0)-np.tanh(-xm+d0+a0))
    return ((b3*b3_numerator/b3_denominator) + (b4*b4_numerator/b4_denominator))

# ----------------------------------------------------
# Równania Takaca unhysteretic
# ----------------------------------------------------

def takac_zero(x, a0, A0):
    return (np.tanh(x + a0)+np.tanh(x - a0))/2 + A0*x

def takac_virgin(x, C3):
    sech = 1/(np.cosh(x))
    return ( np.tanh(x)*(1-2*C3*(sech*sech)) )

# ----------------------------------------------------
# Podstawowe równania Takaca ZORC
# ----------------------------------------------------

def takac_zorc_ascending(x, a0, A0, xm):
    b1 = takac_b1(xm, a0)
    return np.tanh(x - a0) + A0*x + b1

def takac_zorc_descending(x, a0, A0, xm):
    b1 = takac_b1(xm, a0)
    return np.tanh(x + a0) + A0*x - b1 


# ----------------------------------------------------
# Równania Takaca ZORC z bias
# ----------------------------------------------------

def takac_zorc_biased_ascending(x, a0, A0, xm, d0):
    bu = takac_bu(x, xm, a0, d0)
    return np.tanh(x - a0) + A0*x + bu

def takac_zorc_biased_descending(x, a0, A0, xm, d0):
    bd = takac_bd(x, xm, a0, d0)
    return np.tanh(x + a0) + A0*x + bd

# ----------------------------------------------------
# Równania Takaca z przesunięciem środka pętli o x0, y0
# ----------------------------------------------------

def takac_zorc_ascending_extended(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1e = takac_b1e(xm, a0, A)
    return A * np.tanh((x - a0)-x0) + np.sign(A)*A0*x + b1e+y0

def takac_zorc_descending_extended(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1e = takac_b1e(xm, a0, A)
    return A*np.tanh((x + a0)-x0) + np.sign(A)*A0*x - b1e+y0


# ----------------------------------------------------
# Równania Takaca z przesunięciem środka pętli o x0, y0
# i nachyleniem A0 tylko po prawej stronie 
# ----------------------------------------------------

def takac_zorc_ascending_relu(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1 = takac_b1(xm, a0)
    return A * np.tanh((x - a0)-x0) + np.sign(A)*A0*relu_numpy(x-x0) + b1e+y0

def takac_zorc_descending_relu(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1 = takac_b1(xm, a0)
    return A*np.tanh((x + a0)-x0) + np.sign(A)*A0*relu_numpy(x-x0) - b1e+y0  

# ----------------------------------------------------
# Równania Takaca wg gemini 
# ----------------------------------------------------

'''
R0 to punkt srodka na amplitudzie (przesunięcie w górę)
A to amplituda (cały wykres jako symetryczny jest 2*A)
F0 to punkt środka na osi OX
w współczynnik nachylenia - mniejsza wartość bardziej stromo
k Współczynnik skali): Mnożnik różnicy potęgowej. Decyduje o amplitudzie (pionowym rozciągnięciu) efektu histerezy w fazie unloading
p Wkład potęgowy / stopień nieliniowości): Określa, jak szybko zmienia się kształt krzywizny powrotu
R_rev Rezystancja w punkcie maksymalnej siły
F_rev Maksymalna siła nacisku
'''

def takac_loading_curve(F, R0, A, F0, w):
    return R0 + A * np.tanh((F - F0) / w)

def takac_unloading_continuous(F, k, p, R_rev,F_rev):
    return R_rev + k * (np.power(x_save(F), -p) - np.power(F_rev, -p))

# ----------------------------------------------------
# funkcje help
# ----------------------------------------------------

def help_pl():
    print("Zestaw funkcji krzywych ZORC modelu takaca")
    print("zawiera następujące funkcje:")
    print("podstawowy model takaca symetryczny względem (0,0)")
    print("\t takac_zorc_ascending (x, a0, A0, xm)")
    print("\t takac_zorc_descending (x, a0, A0, xm)")
    print("podstawowy model takaca z biasem")
    print("\t takac_zorc_biased_ascending (x, a0, A0, xm, d0)")
    print("\t takac_zorc_biased_descending(x, a0, A0, xm, d0)")      
    print("model takaca z przesunięciem środka histerezy do (x0,y0):")
    print("\t takac_zorc_ascending_extended (x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("\t takac_zorc_descending_extended (x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("model takaca z przesunięciem środka histerezy i wyprostowaniem lewej strony funkcją relu:")
    print("\t takac_zorc_ascending_relu(x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("\t takac_zorc_descending_relu(x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("Parametry wejściowe (model podstawowy):")
    print(": x - zmienna - wektor danych wejściowych")
    print(": a0 - szerokość histerezy")
    print(": A0 - nachylenie prostej poza histerezą")
    print(": xm - punkt zwrotu na osi OX)")
    print("Parametry wejściowe (model rozszerzony i relu):")
    print(": A - Ampliduda histerezy (domyślnie = 1)")
    print(": x0 - przesunięcie środka histerezy na osi OX (domyślnie = 0)")
    print(": y0 - przesunięcie środka histerezy na osi OY (domyślnie = 0)")
    print(": d0 - stałe pole")
