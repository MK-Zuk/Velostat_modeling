import numpy as np
import math as m

# ----------------------------------------------------
# Podstawowe funkcje Fermiego-Diraca
# wersja extended z członem liniowym
# ----------------------------------------------------


def Fermi_Dirac(x, k, A=1, x0=0):
    return A / (m.exp(k(x-x0)) +1)

def Fermi_Dirac_extended(x, k, A=1, x0=0,A0=0):
    return A / (m.exp(k(x-x0)) +1) + A0*x
    
 
# ----------------------------------------------------
# Funkcje Fermiego-Diraca
# jako dwie histerezowe
# ----------------------------------------------------
 
def Fermi_Dirac_ascending(x, k, A=1, x0=0):
    return A / (m.exp(k(x-x0)) +1)

def Fermi_Dirac_descending(x, k, A=1, x0=0):
    return A / (m.exp(k(x0-x)) +1)



def Fermi_Dirac__ascending_extended(x, k, A=1, x0=0,A0=0):
    return A / (m.exp(k(x-x0)) +1) + A0*x
    
def Fermi_Dirac__descending_extended(x, k, A=1, x0=0,A0=0):
    return A / (m.exp(k(x0-x)) +1) + A0*x



# ----------------------------------------------------
# funkcje help
# ----------------------------------------------------

def help_pl():
    print("Zestaw funkcji krzywych")
    print("parametry:")
    print(": A - amplituda krzywej")
    print(": A0 - amplituda części liniowej")
    print(": k - nachylenie (slope")
    print(": x0 - przesunięcie srodka od X=0")