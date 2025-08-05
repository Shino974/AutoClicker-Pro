#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Clicker Pro - Point d'entrée principal
==========================================

Un auto-clicker avancé avec système anti-détection pour contourner
les protections des jeux et applications.

Fonctionnalités principales:
- 3 méthodes de clic anti-détection (Windows API, SendMessage, PostMessage)
- Humanisation des clics avec variations de position et timing
- Interface moderne responsive avec sections collapsibles
- Configuration flexible avec presets et options personnalisées
- Raccourcis clavier globaux (F6/F7)
- Système de langues français/anglais avec drapeaux

Auteur: Shino974
Version: 1.0.0
Date: 2025-01-08
License: MIT
"""

import tkinter as tk
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.app import AutoClickerApp
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("Assurez-vous que tous les modules sont présents:")
    print("- config/constants.py")
    print("- language_manager.py")
    print("- advanced_clicker.py")
    print("- ui/app.py")
    print("- ui/sections.py")
    sys.exit(1)


def main():

    try:
        # Créer la fenêtre principale
        root = tk.Tk()

        # Initialiser l'application
        app = AutoClickerApp(root)

        # Lancer la boucle principale
        root.mainloop()

    except KeyboardInterrupt:
        print("Application interrompue par l'utilisateur")
    except Exception as e:
        print(f"Erreur lors du lancement de l'application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
