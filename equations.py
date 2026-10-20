import numpy as np
from scipy.special import expit

# ----------------------------------------------------
# Podstawowe funkcje Fermiego-Diraca
# wersja extended z członem liniowym
# ----------------------------------------------------


def Fermi_Dirac(x, k, A=1, x0=0):
    return A * (expit(-k*(x-x0)) +1)

def Fermi_Dirac_extended(x, k, A0=0, A=1, x0=0, y0=0):
    return A * (expit(-k*(x-x0)) +1) + A0*x + y0
    
 
# ----------------------------------------------------
# Funkcje Fermiego-Diraca
# jako dwie histerezowe
# ----------------------------------------------------
 
def Fermi_Dirac_ascending(x, k, a0=0, A=1):
    return A * (expit(-k*(x-a0)) +1)

def Fermi_Dirac_descending(x, k, a0=0, A=1):
    return A * (expit(-k*(x+a0)) +1)



def Fermi_Dirac_ascending_extended(x, k, a0=0, A0=0, A=1, x0=0, y0=0):
    return A * (expit(-k*((x-a0)-x0)) +1) + A0*x + y0
    
def Fermi_Dirac_descending_extended(x, k, a0=0, A0=0, A=1, x0=0, y0=0):
    return A * (expit(-k*((x+a0)-x0)) +1) + A0*x + y0



# ----------------------------------------------------
# funkcje help
# ----------------------------------------------------

def help_pl():
    print("Zestaw funkcji krzywych")
    print("parametry:")
    print(": A - amplituda krzywej")
    print(": A0 - amplituda części liniowej")
    print(": k - nachylenie (slope)")
    print(": a0 - histereza - odsuniecie od srodka histerezy w 1/2 wysokosci")
    print(": x0 - przesunięcie srodka od X=0")