import math

# ----------------------------------------------------
# Funkcje obliczające cisnienie dla różnych pol powierzchni
# i podanej sily
# ----------------------------------------------------

def pole_oblicz_cisnienie(pole_mm2: float, sila_n: float) -> float:
  """Oblicza ciśnienie dla dowolnego pola powierzchni.

  Parametry:
  - pole_mm2: pole powierzchni w milimetrach kwadratowych (mm^2)
  - sila_n: siła nacisku w niutonach (N)

  Wyjście:
  - ciśnienie w paskalach (Pa)
  """
  # Przeliczenie mm^2 na m^2 (1 mm^2 = 1e-6 m^2)
  pole_m2 = pole_mm2 * 1e-6
  if pole_m2 == 0:
    raise ValueError("Pole powierzchni nie może wynosić zero.")
  return sila_n / pole_m2

def kolo_oblicz_cisnienie(r_mm: float, sila_n: float) -> float:
  """Oblicza ciśnienie wywierane przez koło o danym promieniu.

  Parametry:
  - r_mm: promień koła w milimetrach (mm)
  - sila_n: siła nacisku w niutonach (N)

  Wyjście:
  - ciśnienie w paskalach (Pa)
  """
  r_m = r_mm * 1e-3
  pole_m2 = math.pi * (r_m**2)
  return sila_n / pole_m2


def kwadrat_oblicz_cisnienie(a_mm: float, sila_n: float) -> float:
  """Oblicza ciśnienie wywierane przez kwadrat o danym boku.

  Parametry:
  - a_mm: bok kwadratu w milimetrach (mm)
  - sila_n: siła nacisku w niutonach (N)

  Wyjście:
  - ciśnienie w paskalach (Pa)
  """
  a_m = a_mm * 1e-3
  pole_m2 = a_m**2
  return sila_n / pole_m2

def kolo_oblicz_cisnienie(bok_mm: float, sila_n: float) -> float:
  """
  Oblicza ciśnienie wywierane przez koło opisane na kwadracie.

  Parametry:
  - bok_mm: bok kwadratu w milimetrach (mm)
  - sila_n: siła nacisku w niutonach (N)

  Wyjście:
  - cisnienie w paskalach (Pa)
  """
  # Przeliczenie milimetrów na metry
  a_m = bok_mm * 1e-3

  # Pole powierzchni koła opisanego na kwadracie: S = (pi * a^2) / 2
  pole_m2 = (math.pi * (a_m**2)) / 2

  # Ciśnienie p = F / S
  cisnienie = sila_n / pole_m2
  return cisnienie


# ----------------------------------------------------
# Funkcje pomocnicze
# ----------------------------------------------------

def konwertuj_przedrostki(
    wartosc: float, z_przedrostka: str, do_przedrostka: str
) -> float:
  """Konwertuje wartość liczbową z jednego przedrostka SI na inny.

  Parametry:
  - wartosc (float): wartość do skonwertowania
  - z_przedrostka (str): symbol przedrostka źródłowego (np. 'k', 'm', '', 'M')
  - do_przedrostka (str): symbol przedrostka docelowego (np. 'M', 'k', 'u')

  Wyjście:
  - float: przeliczona wartość
  """
  # Słownik potęg dziesiątki dla standardowych przedrostków SI
  przedrostki = {
      "Y": 24,  # jotta
      "Z": 21,  # zetta
      "E": 18,  # eksa
      "P": 15,  # peta
      "T": 12,  # tera
      "G": 9,  # giga
      "M": 6,  # mega
      "k": 3,  # kilo
      "h": 2,  # hekto
      "da": 1,  # deka
      "": 0,  # brak przedrostka (jednostka bazowa)
      "d": -1,  # decy
      "c": -2,  # centy
      "m": -3,  # mili
      "u": -6,  # mikro (zamiennik dla µ)
      "n": -9,  # nano
      "p": -12,  # piko
      "f": -15,  # femto
      "a": -18,  # atto
      "z": -21,  # zepto
      "y": -24,  # jokto
  }

  if z_przedrostka not in przedrostki or do_przedrostka not in przedrostki:
    raise ValueError(
        "Nieznany przedrostek. Obsługiwane symbole: Y, Z, E, P, T, G, M, k, h, da,"
        " '', d, c, m, u, n, p, f, a, z, y"
    )

  # Różnica wykładników określa o ile potęg dziesiątki musimy przesunąć wartość
  roznica_wykladnika = przedrostki[z_przedrostka] - przedrostki[do_przedrostka]

  return wartosc * (10**roznica_wykladnika)
