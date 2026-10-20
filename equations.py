import numpy as np
import math as m
from scipy.special import expit

# ----------------------------------------------------
# Podstawowe funkcje Fermiego-Diraca
# wersja extended z członem liniowym
# ----------------------------------------------------


def Fermi_Dirac(x, k, A=1, a0=0):
    return A * (explit(k*(x-a0)) +1)

def Fermi_Dirac_extended(x, k, A=1, a0=0,A0=0):
    return A * (explit(k*(x-a0)) +1) + A0*x
    
 
# ----------------------------------------------------
# Funkcje Fermiego-Diraca
# jako dwie histerezowe
# ----------------------------------------------------
 
def Fermi_Dirac_ascending(x, k, A=1, a0=0):
    return A * (explit(k*(x-a0)) +1)

def Fermi_Dirac_descending(x, k, A=1, a0=0):
    return A * (explit(k*(x+a0)) +1)



def Fermi_Dirac_ascending_extended(x, k, A=1, a0=0,A0=0, x0=0):
    return A * (explit(k*((x-a0)-x0)) +1) + A0*x
    
def Fermi_Dirac_descending_extended(x, k, A=1, a0=0,A0=0, x0=0):
    return A * (explit(k*((x+a0)-x0)) +1) + A0*x



# ----------------------------------------------------
# funkcje help
# ----------------------------------------------------

def help_pl():
    print("Zestaw funkcji krzywych")
    print("parametry:")
    print(": A - amplituda krzywej")
    print(": A0 - amplituda części liniowej")
    print(": k - nachylenie (slope")
    print(": a0 - histereza - odsuniecie od srodka histerezy w 1/2 wysokosci")
    print(": x0 - przesunięcie srodka od X=0")