from abc import ABC, abstractmethod
from datetime import datetime


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar):
        self._jaratszam = jaratszam
        self._celallomas = celallomas
        self._jegyar = jegyar

    @property
    def jaratszam(self):
        return self._jaratszam

    @property
    def celallomas(self):
        return self._celallomas

    @property
    def jegyar(self):
        return self._jegyar

    @abstractmethod
    def jarat_tipus(self):
        pass

    def __str__(self):
        return f"{self.jarat_tipus()} | {self._jaratszam} | {self._celallomas} | {self._jegyar} Ft"


class BelfoldiJarat(Jarat):
    def jarat_tipus(self):
        return "Belföldi járat"


class NemzetkoziJarat(Jarat):
    def jarat_tipus(self):
        return "Nemzetközi járat"


class LegiTarsasag:
    def __init__(self, nev):
        self._nev = nev
        self._jaratok = []

    @property
    def nev(self):
        return self._nev

    @property
    def jaratok(self):
        return self._jaratok

    def jarat_hozzaadasa(self, jarat):
        self._jaratok.append(jarat)

    def jarat_keresese(self, jaratszam):
        for jarat in self._jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        return None

    def jaratok_listazasa(self):
        print("\nElérhető járatok:")
        for jarat in self._jaratok:
            print(jarat)


class JegyFoglalas:
    _kovetkezo_azonosito = 1

    def __init__(self, utas_nev, jarat, datum):
        self._foglalas_id = JegyFoglalas._kovetkezo_azonosito
        JegyFoglalas._kovetkezo_azonosito += 1

        self._utas_nev = utas_nev
        self._jarat = jarat
        self._datum = datum

    @property
    def foglalas_id(self):
        return self._foglalas_id

    @property
    def utas_nev(self):
        return self._utas_nev

    @property
    def jarat(self):
        return self._jarat

    @property
    def datum(self):
        return self._datum

    def __str__(self):
        return (
            f"Foglalás ID: {self._foglalas_id} | "
            f"Utas: {self._utas_nev} | "
            f"Járat: {self._jarat.jaratszam} | "
            f"Cél: {self._jarat.celallomas} | "
            f"Dátum: {self._datum.strftime('%Y-%m-%d')} | "
            f"Ár: {self._jarat.jegyar} Ft"
        )


class FoglalasiRendszer:
    def __init__(self, legitarsasag):
        self._legitarsasag = legitarsasag
        self._foglalasok = []

    def datum_ervenyes(self, datum_szoveg):
        try:
            datum = datetime.strptime(datum_szoveg, "%Y-%m-%d")
            if datum.date() < datetime.now().date():
                raise ValueError("A foglalás dátuma nem lehet múltbeli.")
            return datum
        except ValueError:
            raise ValueError("Érvénytelen dátum. Használd ezt a formátumot: ÉÉÉÉ-HH-NN")

    def jegy_foglalasa(self, utas_nev, jaratszam, datum_szoveg):
        if not utas_nev.strip():
            raise ValueError("Az utas neve nem lehet üres.")

        jarat = self._legitarsasag.jarat_keresese(jaratszam)

        if jarat is None:
            raise ValueError("Nem létező járatszám.")

        datum = self.datum_ervenyes(datum_szoveg)

        foglalas = JegyFoglalas(utas_nev, jarat, datum)
        self._foglalasok.append(foglalas)

        return jarat.jegyar

    def foglalas_lemondasa(self, foglalas_id):
        for foglalas in self._foglalasok:
            if foglalas.foglalas_id == foglalas_id:
                self._foglalasok.remove(foglalas)
                return True

        raise ValueError("Nem létező foglalási azonosító.")

    def foglalasok_listazasa(self):
        if not self._foglalasok:
            print("\nNincsenek aktuális foglalások.")
        else:
            print("\nAktuális foglalások:")
            for foglalas in self._foglalasok:
                print(foglalas)


def kezdeti_adatok_betoltese():
    legitarsasag = LegiTarsasag("Python Airlines")

    jarat1 = BelfoldiJarat("B101", "Budapest", 18000)
    jarat2 = BelfoldiJarat("B202", "Debrecen", 15000)
    jarat3 = NemzetkoziJarat("N303", "London", 65000)

    legitarsasag.jarat_hozzaadasa(jarat1)
    legitarsasag.jarat_hozzaadasa(jarat2)
    legitarsasag.jarat_hozzaadasa(jarat3)

    rendszer = FoglalasiRendszer(legitarsasag)

    rendszer.jegy_foglalasa("Kiss Anna", "B101", "2026-06-10")
    rendszer.jegy_foglalasa("Nagy Péter", "B202", "2026-06-12")
    rendszer.jegy_foglalasa("Tóth Éva", "N303", "2026-07-01")
    rendszer.jegy_foglalasa("Szabó Márk", "B101", "2026-06-15")
    rendszer.jegy_foglalasa("Varga Dóra", "N303", "2026-07-20")
    rendszer.jegy_foglalasa("Horváth Gábor", "B202", "2026-06-18")

    return rendszer, legitarsasag


def menu():
    rendszer, legitarsasag = kezdeti_adatok_betoltese()

    while True:
        print("\n--- Repülőjegy Foglalási Rendszer ---")
        print("1. Járatok listázása")
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("5. Kilépés")

        valasztas = input("Válassz egy menüpontot: ")

        try:
            if valasztas == "1":
                legitarsasag.jaratok_listazasa()

            elif valasztas == "2":
                utas_nev = input("Utas neve: ")
                jaratszam = input("Járatszám: ")
                datum = input("Utazás dátuma (ÉÉÉÉ-HH-NN): ")

                ar = rendszer.jegy_foglalasa(utas_nev, jaratszam, datum)
                print(f"Sikeres foglalás! A jegy ára: {ar} Ft")

            elif valasztas == "3":
                foglalas_id = int(input("Add meg a foglalás ID-t: "))
                rendszer.foglalas_lemondasa(foglalas_id)
                print("A foglalás sikeresen lemondva.")

            elif valasztas == "4":
                rendszer.foglalasok_listazasa()

            elif valasztas == "5":
                print("Kilépés...")
                break

            else:
                print("Érvénytelen menüpont.")

        except ValueError as hiba:
            print(f"Hiba: {hiba}")
        except Exception as hiba:
            print(f"Váratlan hiba történt: {hiba}")


if __name__ == "__main__":
    menu()