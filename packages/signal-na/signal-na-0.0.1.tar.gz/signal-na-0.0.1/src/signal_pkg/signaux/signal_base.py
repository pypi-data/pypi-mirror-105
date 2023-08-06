#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:43:58 2019

@author: nicolas
"""
import copy
from math import ceil, floor

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from base.temps_base import BaseTemps
from base.frequence_base import BaseFrequence
from base.mesure_base import Mesures


class SignalBase():

    liste_signaux = []
    def __init__(self, base_de_temps, vecteur_signal, nom = ""):
        self.base_de_temps = base_de_temps.copier()
        self.base_de_frequence = BaseFrequence(base_de_temps)
        self.mesures = Mesures()

        assert  base_de_temps.N == len(vecteur_signal), """Erreur dans le module SignalBase:
         -> La base de temps et le signal doivent avoir la même dimension"""

        self.__chercher_nom_valide(nom)
        self.vecteur_signal = vecteur_signal
        self.liste_signaux.append(self)

    def copier(self, nom = ""):
        sortie = copy.deepcopy(self)
        sortie.mesures = Mesures()
        if nom != "":
            sortie.nom = nom + "_copié"
        return sortie

    def calculer_vecteur_t(self, liste_imin_imax):
        return self.base_de_temps.calculer_vecteur_t(liste_imin_imax)

    def calculer_vecteur_f(self, liste_imin_imax):
        return self.base_de_frequence.calculer_vecteur_f(liste_imin_imax)


    def __tester_nom(self):
        for s in self.liste_signaux:
            if s != self and s.nom == self.nom:
                return False
        return True

    def __chercher_nom_valide(self, nom):
        if nom == "":
            nom = "s"
        self.nom = nom
        i = 2
        while self.__tester_nom() == False:
            self.nom = nom + "_" + str(i)
            i = i + 1

if __name__ == "__main__":
    pass
    # Te = 1e-1
    # T = 1

    # liste_tmin_tmax = -1, 3

    # bdt = BaseTemps(liste_tmin_tmax, Te)
    # bdt_periode = BaseTemps([0,T], Te)
    # vecteur_t = bdt.calculer_vecteur_t()
    # vecteur_t_periode = bdt_periode.calculer_vecteur_t()
    # vecteur_signal = np.cos(2*np.pi*vecteur_t)
    # vecteur_periode_signal = np.cos(2*np.pi*vecteur_t_periode)
    # s1 = SignalBase(bdt, vecteur_signal, nom = "s1")
    # s2 = SignalBase(bdt, vecteur_signal, nom = "s2")

    # liste_signaux = []
    # for i in range(10):
    #     liste_signaux.append(SignalBase(bdt, vecteur_signal))

    # print("*"*100)
    # for s in liste_signaux:
    #     print(s.nom)        

