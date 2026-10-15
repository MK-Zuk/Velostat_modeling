import numpy as np

# ----------------------------------------------------
# Funkcje pomocnicze
# ----------------------------------------------------

def relu_numpy(x):
    return np.maximum(0, x)


# ----------------------------------------------------
# Podstawowe równania Takaca ZORC
# ----------------------------------------------------

def takac_b1(xm, a0):
    return (np.tanh(xm+a0) - np.tanh(xm-a0))/2

def takac_zorc_ascending(x, a0, A0, xm):
    b1 = takac_b1(xm, a0)
    return np.tanh(x - a0) + A0*x + b1

def takac_zorc_descending(x, a0, A0, xm):
    b1 = takac_b1(xm, a0)
    return np.tanh(x + a0) + A0*x - b1 


# ----------------------------------------------------
# Równania Takaca z przesunięciem środka pętli o x0, y0
# ----------------------------------------------------

def takac_zorc_ascending_extended(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1 = takac_b1(xm, a0)
    return A * np.tanh((x - a0)-x0) + np.sign(A)*A0*x + b1+y0

def takac_zorc_descending_extended(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1 = takac_b1(xm, a0)
    return A*np.tanh((x + a0)-x0) + np.sign(A)*A0*x - b1+y0


# ----------------------------------------------------
# Równania Takaca z przesunięciem środka pętli o x0, y0
# i nachyleniem A0 tylko po prawej stronie 
# ----------------------------------------------------

def takac_zorc_ascending_relu(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1 = takac_b1(xm, a0)
    return A * np.tanh((x - a0)-x0) + np.sign(A)*A0*relu_numpy(x-x0) + b1+y0

def takac_zorc_descending_relu(x, a0, A0, xm, A=1, x0=0,y0=0):
    b1 = takac_b1(xm, a0)
    return A*np.tanh((x + a0)-x0) + np.sign(A)*A0*relu_numpy(x-x0) - b1+y0  


# ----------------------------------------------------
# funkcje help
# ----------------------------------------------------

def help_pl():
    print("Zestaw funkcji krzywych ZORC modelu takaca")
    print("zawiera następujące funkcje:")
    print("podstawowy model takaca symetryczny względem (0,0)")
    print("takac_zorc_ascending (x, a0, A0, xm)")
    print("takac_zorc_descending (x, a0, A0, xm)")
    print("model takaca z przesunięciem środka histerezy:")
    print("takac_zorc_ascending_extended (x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("takac_zorc_descending_extended (x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("model takaca z przesunięciem środka histerezy i wyprostowaniem lewej strony funkcją relu:")
    print("takac_zorc_ascending_relu(x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("takac_zorc_descending_relu(x, a0, A0, xm, A=1, x0=0,y0=0)")
    print("Parametry wejściowe (model podstawowy):")
    print("x - zmienna - wektor danych wejściowych")
    print("a0 - szerokość histerezy")
    print("A0 - nachylenie prostej poza histerezą")
    print("xm - punkt zwrotu na osi OX)")
    print("Parametry wejściowe (model rozszerzony i relu):")
    print("A - Ampliduda histerezy (domyślnie = 1)")
    print("x0 - przesunięcie środka histerezy na osi OX (domyślnie = 0)")
    print("y0 - przesunięcie środka histerezy na osi OY (domyślnie = 0)")
