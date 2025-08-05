#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de clics avancés avec fonctionnalités anti-détection
================================================================

Ce module implémente différentes méthodes de simulation de clics
pour contourner les systèmes de détection des jeux et applications.
"""

import time
import random
import win32api
import win32con
import win32gui
from config.constants import (
    MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, MOUSEEVENTF_RIGHTDOWN,
    MOUSEEVENTF_RIGHTUP, POSITION_VARIATION_RANGE, TIMING_VARIATION_RANGE,
    MICRO_PAUSE_RANGE
)


class AdvancedClicker:
    """
    Gestionnaire de clics avancés avec fonctionnalités anti-détection.

    Cette classe implémente différentes méthodes de simulation de clics
    pour contourner les systèmes de détection des jeux et applications.
    """

    @staticmethod
    def human_like_click(x: int, y: int) -> bool:
        """
        Simule un clic humain naturel avec variations de position et timing.

        Cette méthode utilise l'API Windows directe avec des variations
        aléatoires pour imiter le comportement humain et éviter la détection.

        Args:
            x (int): Coordonnée X du clic
            y (int): Coordonnée Y du clic

        Returns:
            bool: True si le clic a réussi, False sinon

        Note:
            - Variation de position: ±2 pixels aléatoires
            - Timing variable entre press et release: 10-50ms
            - Micro-pause avant le clic: 1-3ms
        """
        try:
            # Application des variations de position pour simuler les tremblements humains
            offset_x = random.randint(*POSITION_VARIATION_RANGE)
            offset_y = random.randint(*POSITION_VARIATION_RANGE)
            final_x = x + offset_x
            final_y = y + offset_y

            # Variation du timing entre press et release pour imiter l'humain
            press_duration = random.uniform(*TIMING_VARIATION_RANGE)

            # Séquence de clic avec timing humain
            # 1. Déplacer la souris à la position cible
            win32api.SetCursorPos((final_x, final_y))

            # 2. Micro-pause pour simuler le temps de réaction humain
            time.sleep(random.uniform(*MICRO_PAUSE_RANGE))

            # 3. Simuler press et release avec timing variable
            win32api.mouse_event(MOUSEEVENTF_LEFTDOWN, final_x, final_y, 0, 0)
            time.sleep(press_duration)
            win32api.mouse_event(MOUSEEVENTF_LEFTUP, final_x, final_y, 0, 0)

            return True

        except Exception as e:
            print(f"Erreur dans human_like_click: {e}")
            return False

    @staticmethod
    def sendmessage_click(x: int, y: int, hwnd=None) -> bool:
        """
        Utilise SendMessage pour envoyer directement des messages de clic.

        Cette méthode contourne certaines protections en envoyant les messages
        directement à la fenêtre cible sans passer par le système de souris.

        Args:
            x (int): Coordonnée X du clic
            y (int): Coordonnée Y du clic
            hwnd (int, optional): Handle de la fenêtre cible.
                                 Si None, utilise la fenêtre active.

        Returns:
            bool: True si le clic a réussi, False sinon

        Note:
            - Convertit automatiquement les coordonnées écran en coordonnées client
            - Timing variable pour éviter la détection
            - Méthode synchrone (bloquante)
        """
        try:
            # Obtenir le handle de la fenêtre cible
            if hwnd is None:
                hwnd = win32gui.GetForegroundWindow()

            # Conversion des coordonnées écran vers coordonnées client de la fenêtre
            screen_point = (x, y)
            client_point = win32gui.ScreenToClient(hwnd, screen_point)

            # Création du paramètre lParam pour les coordonnées
            # MAKELONG combine les coordonnées X et Y en un seul paramètre
            lParam = win32api.MAKELONG(client_point[0], client_point[1])

            # Envoi des messages de clic avec timing variable
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            time.sleep(random.uniform(*TIMING_VARIATION_RANGE))
            win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

            return True

        except Exception as e:
            print(f"Erreur dans sendmessage_click: {e}")
            return False

    @staticmethod
    def postmessage_click(x: int, y: int, hwnd=None) -> bool:
        """
        Utilise PostMessage pour des messages asynchrones de clic.

        Méthode non-bloquante qui place les messages dans la queue de la fenêtre.
        Utile pour contourner certaines protections avancées.

        Args:
            x (int): Coordonnée X du clic
            y (int): Coordonnée Y du clic
            hwnd (int, optional): Handle de la fenêtre cible.
                                 Si None, utilise la fenêtre active.

        Returns:
            bool: True si l'envoi a réussi, False sinon

        Note:
            - Messages asynchrones (non-bloquants)
            - Peuvent être traités avec délai par l'application cible
            - Efficace contre certains systèmes anti-bot
        """
        try:
            # Obtenir le handle de la fenêtre cible
            if hwnd is None:
                hwnd = win32gui.GetForegroundWindow()

            # Conversion des coordonnées écran vers coordonnées client
            screen_point = (x, y)
            client_point = win32gui.ScreenToClient(hwnd, screen_point)
            lParam = win32api.MAKELONG(client_point[0], client_point[1])

            # Envoi asynchrone des messages de clic
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            time.sleep(random.uniform(*TIMING_VARIATION_RANGE))
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)

            return True

        except Exception as e:
            print(f"Erreur dans postmessage_click: {e}")
            return False

    @staticmethod
    def simple_click(x: int, y: int) -> bool:
        """
        Clic simple sans humanisation pour des performances maximales.

        Args:
            x (int): Coordonnée X du clic
            y (int): Coordonnée Y du clic

        Returns:
            bool: True si le clic a réussi, False sinon
        """
        try:
            win32api.SetCursorPos((x, y))
            win32api.mouse_event(MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(MOUSEEVENTF_LEFTUP, x, y, 0, 0)
            return True
        except Exception as e:
            print(f"Erreur dans simple_click: {e}")
            return False
