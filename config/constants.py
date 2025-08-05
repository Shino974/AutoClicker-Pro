#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Constantes et configuration pour Auto Clicker Pro
================================================

Ce module contient toutes les constantes utilisées dans l'application.
"""

# Constantes Windows pour les événements souris bas niveau
MOUSEEVENTF_LEFTDOWN = 0x0002    # Bouton gauche pressé
MOUSEEVENTF_LEFTUP = 0x0004      # Bouton gauche relâché
MOUSEEVENTF_RIGHTDOWN = 0x0008   # Bouton droit pressé
MOUSEEVENTF_RIGHTUP = 0x0010     # Bouton droit relâché
MOUSEEVENTF_ABSOLUTE = 0x8000    # Coordonnées absolues

# Configuration des variations d'humanisation
POSITION_VARIATION_RANGE = (-2, 2)      # Variation position en pixels
TIMING_VARIATION_RANGE = (0.01, 0.05)   # Variation timing press/release (sec)
MICRO_PAUSE_RANGE = (0.001, 0.003)      # Micro-pauses avant clic (sec)
INTERVAL_RANDOMNESS = (0.5, 1.5)        # Multiplicateur d'intervalle aléatoire

# Configuration de l'interface
WINDOW_GEOMETRY = "500x600"
WINDOW_MIN_SIZE = (400, 500)
WINDOW_BG_COLOR = '#2c3e50'
MAIN_FRAME_BG_COLOR = '#34495e'
HEADER_BG_COLOR = '#3e4651'

# Couleurs de l'interface
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#3498db',
    'light': '#ecf0f1',
    'dark': '#2c3e50',
    'muted': '#bdc3c7'
}
