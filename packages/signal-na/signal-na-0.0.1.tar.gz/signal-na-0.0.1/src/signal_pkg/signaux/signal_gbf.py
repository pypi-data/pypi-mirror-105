#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 15:43:58 2019

@author: nicolas
"""

import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import base.constantes_base as cst

from signaux.signal_base import SignalBase
from base.temps_base import BaseTemps
from signaux.signal_complet import SignalComplet

import numpy as np


__all__ = ["SignalGBF"]


def periodiser(N, vecteur_signal_periode):
    Nperiode = len(vecteur_signal_periode)
    Pperiodes = int(np.ceil(N/Nperiode))
    return np.concatenate([vecteur_signal_periode]*Pperiodes)[0:N]

class SignalSinus(SignalComplet):
    def __init__(self, F, Vpp, offset, phi, tr, liste_tmin_tmax, Te, nom):
        base_de_temps_periode = BaseTemps([0, 1/F], Te)
        base_de_temps = BaseTemps(liste_tmin_tmax, Te)

        Nperiode = base_de_temps_periode.convertir_n_vers_i(base_de_temps_periode.Nmax)
        Nsignal = base_de_temps.convertir_n_vers_i(base_de_temps.Nmax)

        Nretard = base_de_temps.calculer_n(tr) - base_de_temps.Nmin
        decalage_retard = Nretard % Nperiode

        vecteur_t_periode = base_de_temps_periode.calculer_vecteur_t()
        vecteur_signal_periode = np.roll(offset + Vpp*np.cos(2*np.pi*F*vecteur_t_periode + phi)/2, decalage_retard)

        SignalComplet.__init__(self, base_de_temps, periodiser(Nsignal, vecteur_signal_periode), nom)
        self.mesures.T_th = 1/F

class SignalCarre(SignalComplet):
    def __init__(self, F, Vpp, offset, alpha, tr, liste_tmin_tmax, Te, nom):
        base_de_temps_periode = BaseTemps([0, 1/F], Te)
        base_de_temps = BaseTemps(liste_tmin_tmax, Te)

        Nperiode = base_de_temps_periode.convertir_n_vers_i(base_de_temps_periode.Nmax)
        Nsignal = base_de_temps.convertir_n_vers_i(base_de_temps.Nmax)

        Nalpha = int(np.round(alpha*Nperiode))
        Nretard = base_de_temps.calculer_n(tr) - base_de_temps.Nmin
        decalage_retard = Nretard % Nperiode

        vecteur_signal_periode = np.roll(np.concatenate([np.ones(Nalpha)/2, -np.ones(Nperiode-Nalpha)/2])*Vpp+offset, decalage_retard)

        SignalComplet.__init__(self, base_de_temps, periodiser(Nsignal, vecteur_signal_periode), nom)
        self.mesures.T_th = 1/F

class SignalTriangle(SignalComplet):
    def __init__(self, F, Vpp, offset, alpha, tr, liste_tmin_tmax, Te, nom):
        assert 0. < alpha < 1.
        base_de_temps_periode = BaseTemps([0, 1/F], Te)
        base_de_temps = BaseTemps(liste_tmin_tmax, Te)

        Nperiode = base_de_temps_periode.convertir_n_vers_i(base_de_temps_periode.Nmax)
        Nsignal = base_de_temps.convertir_n_vers_i(base_de_temps.Nmax)

        Nalpha = int(np.round(alpha*Nperiode))
        Nretard = base_de_temps.calculer_n(tr) - base_de_temps.Nmin
        decalage_retard = Nretard % Nperiode

        vecteur_signal_periode = np.roll(np.concatenate([np.linspace(-0.5, 0.5,Nalpha), np.linspace(0.5, -0.5, Nperiode-Nalpha)])*Vpp+offset, decalage_retard)

        SignalComplet.__init__(self, base_de_temps, periodiser(Nsignal, vecteur_signal_periode), nom)
        self.mesures.T_th = 1/F

class SignalGBF(SignalComplet):
    def __init__(self, type_signal = "cosinus", F=1, Vpp= 1, offset = 0, tr=0., phi = 0., alpha = 0.5, liste_tmin_tmax = cst.liste_tmin_tmax, Te = cst.Te, nom = ""):
        assert type_signal in cst.liste_types_signaux_gbf
        if type_signal == "cosinus":
            SignalSinus.__init__(self, F, Vpp, offset, phi, tr, liste_tmin_tmax, Te, nom)
        elif type_signal == "carre":
            SignalCarre.__init__(self, F, Vpp, offset, alpha, tr, liste_tmin_tmax, Te, nom)
        elif type_signal == "triangle":
            SignalTriangle.__init__(self, F, Vpp, offset, alpha, tr, liste_tmin_tmax, Te, nom)
        elif type_signal == "rampe":
            SignalTriangle.__init__(self, F, Vpp, offset, 1-cst.Ta/2, tr, liste_tmin_tmax, Te, nom)

if __name__ == "__main__":
    liste_tmin_tmax=[0, 1]
    F = 2
    phi = 0.2
    tr = phi/(2*np.pi*F)
    s1 = SignalGBF("carre", 3, 2, 1, tr = 0.1, phi = 3, nom="$s_1$")
    
    s1.tracer_signal()


    print("fin")