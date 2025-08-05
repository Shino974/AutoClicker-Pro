#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto Clicker Pro - Version Anti-Détection
==========================================

Un auto-clicker avancé avec système anti-détection pour contourner
les protections des jeux et applications.

Fonctionnalités principales:
- 3 méthodes de clic anti-détection (Windows API, SendMessage, PostMessage)
- Humanisation des clics avec variations de position et timing
- Interface moderne responsive avec sections collapsibles
- Configuration flexible avec presets et options personnalisées
- Raccourcis clavier globaux (F6/F7)

Auteur: Shino974
Version: 1.0.0
Date: 2025-01-08
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import win32api
import win32con
import win32gui
import keyboard

# ==============================================================================
# CONSTANTES ET CONFIGURATION
# ==============================================================================

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

# ==============================================================================
# CLASSES PRINCIPALES
# ==============================================================================

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


class AutoClickerApp:
    """
    Application principale de l'Auto Clicker avec interface graphique moderne.

    Cette classe gère l'interface utilisateur, la configuration des paramètres,
    et l'orchestration des différentes méthodes de clic anti-détection.

    Attributes:
        root (tk.Tk): Fenêtre principale de l'application
        is_clicking (bool): État de l'auto-clicker
        click_x (int): Coordonnée X de la position de clic
        click_y (int): Coordonnée Y de la position de clic
        click_thread (threading.Thread): Thread d'exécution des clics
        mouse_listener: Listener pour la capture de position (non utilisé actuellement)
        humanize_clicks (bool): Active/désactive l'humanisation
        random_intervals (bool): Active/désactive les intervalles aléatoires
        click_method (str): Méthode de clic sélectionnée
    """

    def __init__(self, root: tk.Tk):
        """
        Initialise l'application Auto Clicker.

        Args:
            root (tk.Tk): Instance de la fenêtre principale Tkinter
        """
        # Configuration de la fenêtre principale
        self.root = root
        self.root.title("Auto Clicker Pro - Anti-Detection")
        self.root.geometry("500x600")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        self.root.minsize(400, 500)

        # Variables d'état de l'application
        self.is_clicking = False           # État de l'auto-clicker
        self.click_x = 0                   # Position X du clic
        self.click_y = 0                   # Position Y du clic
        self.click_thread = None           # Thread d'exécution
        self.mouse_listener = None         # Listener souris (legacy)
        self.target_window = None          # Fenêtre cible (future feature)

        # Paramètres anti-détection par défaut
        self.humanize_clicks = True        # Humanisation activée
        self.random_intervals = True       # Intervalles aléatoires
        self.click_method = "windows_api"  # Méthode par défaut

        # Initialisation de l'interface et des raccourcis
        self.setup_ui()
        self.setup_hotkeys()

    def setup_ui(self):
        """
        Configure l'interface utilisateur principale.

        Crée et organise tous les éléments de l'interface, y compris les sections
        collapsibles, les boutons de contrôle, et les affichages d'état.
        """
        # Style amélioré
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'), background='#2c3e50', foreground='white')
        style.configure('Custom.TButton', font=('Arial', 10, 'bold'))
        style.configure('Green.TButton', background='#27ae60', foreground='white')
        style.configure('Red.TButton', background='#e74c3c', foreground='white')

        # Configuration de la scrollbar moderne
        style.configure("Vertical.TScrollbar",
                       background='#34495e',
                       troughcolor='#2c3e50',
                       bordercolor='#34495e',
                       arrowcolor='#ecf0f1',
                       darkcolor='#34495e',
                       lightcolor='#34495e')

        # Header avec titre et sous-titre
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text="Auto Clicker Pro",
                              font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        title_label.pack(pady=(15, 0))

        subtitle_label = tk.Label(header_frame, text="🛡️ Version Anti-Détection",
                                 font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7')
        subtitle_label.pack()

        # Container principal pour le scroll
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Canvas avec scrollbar améliorée
        canvas = tk.Canvas(main_container, bg='#2c3e50', highlightthickness=0,
                          relief='flat', borderwidth=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview,
                                 style="Vertical.TScrollbar")
        scrollable_frame = tk.Frame(canvas, bg='#2c3e50')

        # Configuration du scroll améliorée
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ajuster la largeur du frame scrollable à celle du canvas
            canvas_width = canvas.winfo_width()
            canvas.itemconfig(window_id, width=canvas_width)

        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)

        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack du canvas et scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame principal avec design moderne
        main_frame = tk.Frame(scrollable_frame, bg='#34495e', relief='flat', bd=0,
                             highlightbackground='#5d6d7e', highlightthickness=1)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Variables pour sections collapsibles avec animations
        self.pos_collapsed = tk.BooleanVar(value=False)
        self.freq_collapsed = tk.BooleanVar(value=False)
        self.anti_collapsed = tk.BooleanVar(value=False)
        self.count_collapsed = tk.BooleanVar(value=False)

        # Store toggle buttons for icon updates
        self.toggle_buttons = {}

        # Section 1: Position du clic (design amélioré)
        self.create_modern_section(main_frame, "pos", "🎯", "Position du clic",
                                  self.build_position_content, self.toggle_pos_section)

        # Section 2: Fréquence de clic
        self.create_modern_section(main_frame, "freq", "⚡", "Fréquence de clic",
                                  self.build_frequency_content, self.toggle_freq_section)

        # Section 3: Options Anti-Détection
        self.create_modern_section(main_frame, "anti", "🛡️", "Options Anti-Détection",
                                  self.build_antidetect_content, self.toggle_anti_section)

        # Section 4: Nombre de clics
        self.create_modern_section(main_frame, "count", "🔢", "Nombre de clics",
                                  self.build_count_content, self.toggle_count_section)

        # Boutons de contrôle avec design moderne
        self.create_control_buttons(main_frame)

        # Status avec design amélioré
        status_container = tk.Frame(main_frame, bg='#34495e')
        status_container.pack(fill='x', padx=15, pady=10)

        self.status_label = tk.Label(status_container, text="✅ Prêt - Configurez position et fréquence",
                                   font=('Arial', 11, 'bold'), bg='#34495e', fg='#2ecc71',
                                   wraplength=400, justify='center')
        self.status_label.pack(pady=5)

        # Footer avec instructions (fixe, pas dans le scroll)
        footer_frame = tk.Frame(self.root, bg='#2c3e50', height=35)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        instructions = tk.Label(footer_frame,
                              text="F6: Démarrer | F7: Arrêter | By Shino974",
                              font=('Arial', 9), bg='#2c3e50', fg='#bdc3c7')
        instructions.pack(pady=8)

        # Bind améliorés pour la molette de souris (support universel)
        self.bind_mousewheel_to_canvas(canvas)

        # Store references
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame
        self.main_frame = main_frame

    def create_modern_section(self, parent, section_key, icon, title, content_builder, toggle_func):
        """
        Crée une section moderne avec header cliquable

        Cette méthode crée une section avec un en-tête qui peut être cliqué
        pour afficher ou masquer le contenu. Utilisé pour organiser les paramètres
        en sections collapsibles.

        Args:
            parent (tk.Frame): Le conteneur parent dans lequel la section est ajoutée
            section_key (str): Clé unique pour identifier la section
            icon (str): Icône à afficher dans l'en-tête
            title (str): Titre de la section
            content_builder (callable): Fonction pour construire le contenu de la section
            toggle_func (callable): Fonction à appeler lors du basculement de la section
        """
        # Container de la section
        section_container = tk.Frame(parent, bg='#34495e')
        section_container.pack(fill='x', padx=10, pady=8)

        # Header avec hover effect
        header = tk.Frame(section_container, bg='#3e4651', relief='flat', bd=1,
                         highlightbackground='#5d6d7e', highlightthickness=1)
        header.pack(fill='x')

        # Header content
        header_content = tk.Frame(header, bg='#3e4651')
        header_content.pack(fill='x', padx=12, pady=8)

        # Toggle button avec animation
        toggle_btn = tk.Label(header_content, text="▼", font=('Arial', 12, 'bold'),
                             bg='#3e4651', fg='#3498db', cursor='hand2', width=2)
        toggle_btn.pack(side='left', padx=(0, 10))

        # Icon et title
        title_frame = tk.Frame(header_content, bg='#3e4651')
        title_frame.pack(side='left', fill='x', expand=True)

        title_label = tk.Label(title_frame, text=f"{icon} {title}",
                              font=('Arial', 12, 'bold'), fg='white', bg='#3e4651')
        title_label.pack(side='left')

        # Status indicator (petit point coloré)
        status_dot = tk.Label(header_content, text="●", font=('Arial', 16),
                             bg='#3e4651', fg='#27ae60')
        status_dot.pack(side='right')

        # Content frame
        content_frame = tk.Frame(section_container, bg='#34495e',
                               relief='flat', bd=1, highlightbackground='#5d6d7e', highlightthickness=1)
        content_frame.pack(fill='x', pady=(0, 0))

        # Build content
        content_builder(content_frame)

        # Store references
        setattr(self, f"{section_key}_section", content_frame)
        setattr(self, f"{section_key}_toggle_btn", toggle_btn)
        self.toggle_buttons[section_key] = toggle_btn

        # Bind click events
        def on_header_click(event):
            toggle_func()

        def on_hover_enter(event):
            header.configure(bg='#4a5568')
            header_content.configure(bg='#4a5568')
            for child in header_content.winfo_children():
                child.configure(bg='#4a5568')
            title_frame.configure(bg='#4a5568')

        def on_hover_leave(event):
            header.configure(bg='#3e4651')
            header_content.configure(bg='#3e4651')
            for child in header_content.winfo_children():
                child.configure(bg='#3e4651')
            title_frame.configure(bg='#3e4651')

        header.bind("<Button-1>", on_header_click)
        header_content.bind("<Button-1>", on_header_click)
        toggle_btn.bind("<Button-1>", on_header_click)
        title_label.bind("<Button-1>", on_header_click)

        header.bind("<Enter>", on_hover_enter)
        header.bind("<Leave>", on_hover_leave)

    def bind_mousewheel_to_canvas(self, canvas):
        """Bind universel pour la molette de souris"""
        def _on_mousewheel(event):
            # Support pour Windows
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            # Support pour Linux
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        def bind_to_mousewheel(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)  # Windows
            widget.bind("<Button-4>", _on_mousewheel)    # Linux scroll up
            widget.bind("<Button-5>", _on_mousewheel)    # Linux scroll down

        # Bind to canvas and all its children recursively
        bind_to_mousewheel(canvas)
        bind_to_mousewheel(self.root)

        def bind_tree(widget):
            bind_to_mousewheel(widget)
            for child in widget.winfo_children():
                bind_tree(child)

        # Bind après un délai pour inclure les widgets créés dynamiquement
        self.root.after(100, lambda: bind_tree(self.scrollable_frame))

    def build_position_content(self, parent):
        """Construit le contenu de la section position"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        self.position_label = tk.Label(content, text="Aucune position sélectionnée",
                                     font=('Arial', 11), bg='#34495e', fg='#e74c3c')
        self.position_label.pack(pady=(0, 15))

        select_pos_btn = tk.Button(content, text="🎯 Sélectionner Position",
                                  command=self.start_position_selection,
                                  bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                  relief='flat', bd=0, padx=20, pady=10,
                                  cursor='hand2', activebackground='#2980b9')
        select_pos_btn.pack(pady=(0, 10))

        instruction_label = tk.Label(content, text="Cliquez sur le bouton puis cliquez à l'endroit désiré",
                                    font=('Arial', 9), bg='#34495e', fg='#bdc3c7',
                                    wraplength=350, justify='center')
        instruction_label.pack()

    def build_frequency_content(self, parent):
        """Construit le contenu de la section fréquence"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        # Options de fréquence prédéfinies
        freq_preset_frame = tk.Frame(content, bg='#34495e')
        freq_preset_frame.pack(pady=5)

        tk.Label(freq_preset_frame, text="Presets:", font=('Arial', 9, 'bold'),
                bg='#34495e', fg='white').pack(anchor='w')

        preset_buttons_frame = tk.Frame(freq_preset_frame, bg='#34495e')
        preset_buttons_frame.pack()

        presets = [
            ("🐌 Lent (2s)", 2.0),
            ("🚶 Normal (1s)", 1.0),
            ("🏃 Rapide (0.5s)", 0.5),
            ("⚡ Ultra (0.1s)", 0.1)
        ]

        for text, value in presets:
            btn = tk.Button(preset_buttons_frame, text=text,
                           command=lambda v=value: self.set_interval_preset(v),
                           bg='#2c3e50', fg='white', font=('Arial', 8),
                           relief='raised', bd=1, width=12)
            btn.pack(side='left', padx=2)

        # Intervalle personnalisé
        custom_frame = tk.Frame(content, bg='#34495e')
        custom_frame.pack(pady=10)

        tk.Label(custom_frame, text="Intervalle personnalisé (secondes):",
                font=('Arial', 10, 'bold'), bg='#34495e', fg='white').pack()

        interval_control_frame = tk.Frame(custom_frame, bg='#34495e')
        interval_control_frame.pack()

        self.interval_var = tk.DoubleVar(value=1.0)

        # Entry pour saisie directe
        self.interval_entry = tk.Entry(interval_control_frame, textvariable=self.interval_var,
                                      width=8, font=('Arial', 12), justify='center')
        self.interval_entry.pack(side='left', padx=5)

        # Scale pour ajustement visuel
        interval_scale = tk.Scale(interval_control_frame, from_=0.01, to=10.0, resolution=0.01,
                                orient='horizontal', variable=self.interval_var,
                                bg='#34495e', fg='white', highlightbackground='#34495e',
                                length=200)
        interval_scale.pack(side='left', padx=5)

        # Affichage fréquence en clics/minute
        self.freq_display = tk.Label(custom_frame, text="60 clics/minute",
                                    font=('Arial', 9), bg='#34495e', fg='#f39c12')
        self.freq_display.pack(pady=2)

        # Liaison pour mise à jour automatique
        self.interval_var.trace('w', self.update_frequency_display)

    def build_antidetect_content(self, parent):
        """Construit le contenu de la section anti-détection"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        # Méthode de clic
        method_frame = tk.Frame(content, bg='#34495e')
        method_frame.pack(pady=5)

        tk.Label(method_frame, text="Méthode de clic:", font=('Arial', 10, 'bold'),
                bg='#34495e', fg='white').pack(anchor='w')

        self.click_method_var = tk.StringVar(value="windows_api")
        methods = [
            ("🎯 Windows API (Recommandé)", "windows_api"),
            ("📨 SendMessage", "sendmessage"),
            ("📤 PostMessage", "postmessage")
        ]

        for text, value in methods:
            rb = tk.Radiobutton(method_frame, text=text, variable=self.click_method_var, value=value,
                               bg='#34495e', fg='white', selectcolor='#2c3e50',
                               font=('Arial', 9), command=self.update_click_method)
            rb.pack(anchor='w')

        # Options d'humanisation
        humanize_frame = tk.Frame(content, bg='#34495e')
        humanize_frame.pack(pady=5)

        self.humanize_var = tk.BooleanVar(value=True)
        humanize_cb = tk.Checkbutton(humanize_frame, text="🤖 Humaniser les clics (variations de position)",
                                    variable=self.humanize_var, bg='#34495e', fg='white',
                                    selectcolor='#2c3e50', font=('Arial', 9))
        humanize_cb.pack(anchor='w')

        self.random_interval_var = tk.BooleanVar(value=True)
        random_cb = tk.Checkbutton(humanize_frame, text="⏰ Intervalles aléatoires (±50%)",
                                  variable=self.random_interval_var, bg='#34495e', fg='white',
                                  selectcolor='#2c3e50', font=('Arial', 9))
        random_cb.pack(anchor='w')

    def build_count_content(self, parent):
        """Construit le contenu de la section nombre de clics"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        self.count_var = tk.IntVar(value=0)

        # Option infini
        infini_frame = tk.Frame(content, bg='#34495e')
        infini_frame.pack(pady=(0, 10))

        self.count_mode_var = tk.StringVar(value="infini")

        infini_rb = tk.Radiobutton(infini_frame, text="∞ Infini",
                                  variable=self.count_mode_var, value="infini",
                                  bg='#34495e', fg='white', selectcolor='#2c3e50',
                                  font=('Arial', 11, 'bold'),
                                  command=lambda: self.count_var.set(0))
        infini_rb.pack(anchor='w')

        # Saisie personnalisée
        custom_frame = tk.Frame(content, bg='#34495e')
        custom_frame.pack()

        custom_rb = tk.Radiobutton(custom_frame, text="Nombre personnalisé:",
                                  variable=self.count_mode_var, value="custom",
                                  bg='#34495e', fg='white', selectcolor='#2c3e50',
                                  font=('Arial', 11, 'bold'))
        custom_rb.pack(anchor='w', pady=(0, 5))

        count_entry = tk.Entry(custom_frame, textvariable=self.count_var, width=15,
                              font=('Arial', 12), justify='center')
        count_entry.pack(pady=(0, 5))

        # Bind pour activer le mode custom quand on tape dans le champ
        def on_entry_focus(event):
            self.count_mode_var.set("custom")

        count_entry.bind("<FocusIn>", on_entry_focus)
        count_entry.bind("<KeyPress>", on_entry_focus)

    def create_control_buttons(self, parent):
        """Crée les boutons de contrôle avec design moderne"""
        control_container = tk.Frame(parent, bg='#34495e')
        control_container.pack(fill='x', padx=15, pady=20)

        # Buttons avec design moderne
        self.start_btn = tk.Button(control_container, text="🚀 DÉMARRER",
                                  command=self.start_clicking,
                                  bg='#27ae60', fg='white', font=('Arial', 14, 'bold'),
                                  relief='flat', bd=0, padx=20, pady=15, cursor='hand2',
                                  activebackground='#219a52')
        self.start_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

        self.stop_btn = tk.Button(control_container, text="🛑 ARRÊTER",
                                 command=self.stop_clicking,
                                 bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'),
                                 relief='flat', bd=0, padx=20, pady=15, cursor='hand2',
                                 activebackground='#c0392b')
        self.stop_btn.pack(side='left', fill='x', expand=True, padx=(5, 0))

        # Shortcuts info
        shortcut_frame = tk.Frame(control_container, bg='#34495e')
        shortcut_frame.pack(fill='x', pady=(10, 0))

    def toggle_pos_section(self):
        """Toggle la section position avec animation d'icône"""
        if self.pos_collapsed.get():
            self.pos_section.pack(fill='x', pady=(0, 0))
            self.pos_collapsed.set(False)
            self.pos_toggle_btn.config(text="▼")
        else:
            self.pos_section.pack_forget()
            self.pos_collapsed.set(True)
            self.pos_toggle_btn.config(text="▶")
        self._update_scroll_region()

    def toggle_freq_section(self):
        """Toggle la section fréquence avec animation d'icône"""
        if self.freq_collapsed.get():
            self.freq_section.pack(fill='x', pady=(0, 0))
            self.freq_collapsed.set(False)
            self.freq_toggle_btn.config(text="▼")
        else:
            self.freq_section.pack_forget()
            self.freq_collapsed.set(True)
            self.freq_toggle_btn.config(text="▶")
        self._update_scroll_region()

    def toggle_anti_section(self):
        """Toggle la section anti-détection avec animation d'icône"""
        if self.anti_collapsed.get():
            self.anti_section.pack(fill='x', pady=(0, 0))
            self.anti_collapsed.set(False)
            self.anti_toggle_btn.config(text="▼")
        else:
            self.anti_section.pack_forget()
            self.anti_collapsed.set(True)
            self.anti_toggle_btn.config(text="▶")
        self._update_scroll_region()

    def toggle_count_section(self):
        """Toggle la section nombre de clics avec animation d'icône"""
        if self.count_collapsed.get():
            self.count_section.pack(fill='x', pady=(0, 0))
            self.count_collapsed.set(False)
            self.count_toggle_btn.config(text="▼")
        else:
            self.count_section.pack_forget()
            self.count_collapsed.set(True)
            self.count_toggle_btn.config(text="▶")
        self._update_scroll_region()

    def _update_scroll_region(self):
        """Met à jour la région de scroll avec animation fluide"""
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Smooth scroll to keep current view
        self.canvas.yview_moveto(self.canvas.canvasy(0) / max(1, self.canvas.bbox("all")[3]))

    def set_interval_preset(self, value):
        """Définit un preset d'intervalle de clic"""
        self.interval_var.set(value)

    def update_frequency_display(self, *args):
        """Met à jour l'affichage de la fréquence en fonction de l'intervalle"""
        try:
            interval = self.interval_var.get()
            if interval > 0:
                freq = 60 / interval
                self.freq_display.config(text=f"{freq:.1f} clics/minute")
            else:
                self.freq_display.config(text="Invalid")
        except:
            self.freq_display.config(text="Invalid")

    def manual_position_input(self):
        """Saisie manuelle de la position de clic"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Saisie manuelle de position")
        dialog.geometry("300x150")
        dialog.configure(bg='#34495e')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Position X:", font=('Arial', 10),
                bg='#34495e', fg='white').pack(pady=5)
        x_entry = tk.Entry(dialog, font=('Arial', 10), justify='center')
        x_entry.pack(pady=2)

        tk.Label(dialog, text="Position Y:", font=('Arial', 10),
                bg='#34495e', fg='white').pack(pady=5)
        y_entry = tk.Entry(dialog, font=('Arial', 10), justify='center')
        y_entry.pack(pady=2)

        def save_position():
            """Sauvegarde la position saisie manuellement"""
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                self.click_x = x
                self.click_y = y
                self.position_label.config(text=f"Position: X={x}, Y={y}", fg='#2ecc71')
                self.status_label.config(text="✅ Position configurée manuellement", fg='#2ecc71')
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")

        tk.Button(dialog, text="Confirmer", command=save_position,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)

    def start_position_selection(self):
        """Lance la sélection de position - l'utilisateur clique où il veut"""
        try:
            self.status_label.config(text="🎯 Cliquez à l'endroit désiré pour définir la position...", fg='#f39c12')

            # Arrêter proprement l'ancien listener s'il existe
            if self.mouse_listener:
                try:
                    self.mouse_listener.stop()
                except:
                    pass
                self.mouse_listener = None

            # Créer une fenêtre transparente plein écran pour capturer le clic
            self.create_capture_overlay()

        except Exception as e:
            print(f"Erreur lors du démarrage de la sélection: {e}")
            self.status_label.config(text="❌ Erreur lors de la sélection", fg='#e74c3c')

    def create_capture_overlay(self):
        """Crée une fenêtre transparente plein écran pour capturer la position"""
        # Créer une fenêtre overlay
        self.overlay = tk.Toplevel(self.root)
        self.overlay.title("Sélection de position")
        self.overlay.configure(bg='black')
        self.overlay.attributes('-alpha', 0.3)  # Semi-transparent
        self.overlay.attributes('-topmost', True)  # Toujours au premier plan
        self.overlay.attributes('-fullscreen', True)  # Plein écran
        self.overlay.configure(cursor="crosshair")  # Curseur en croix

        # Masquer la fenêtre principale
        self.root.withdraw()

        # Label d'instruction
        instruction = tk.Label(self.overlay,
                              text="Cliquez à l'endroit désiré pour définir la position de clic\nAppuyez sur Échap pour annuler",
                              font=('Arial', 16, 'bold'),
                              bg='black', fg='white',
                              justify='center')
        instruction.pack(expand=True)

        # Bind les événements
        self.overlay.bind('<Button-1>', self.on_overlay_click)
        self.overlay.bind('<Escape>', self.cancel_position_selection)
        self.overlay.focus_set()  # Focus pour capturer Échap

    def on_overlay_click(self, event):
        """Capture la position lors du clic sur l'overlay"""
        try:
            # Récupérer les coordonnées absolues de l'écran
            x = self.overlay.winfo_pointerx()
            y = self.overlay.winfo_pointery()

            self.click_x = x
            self.click_y = y

            # Fermer l'overlay
            self.close_overlay()

            # Mettre à jour l'interface
            self.update_position_ui(x, y)

        except Exception as e:
            print(f"Erreur lors de la capture de position: {e}")
            self.close_overlay()
            self.show_error_ui()

    def cancel_position_selection(self, event=None):
        """Annule la sélection de position"""
        self.close_overlay()
        self.status_label.config(text="❌ Sélection annulée", fg='#e74c3c')
        self.root.deiconify()

    def close_overlay(self):
        """Ferme la fenêtre overlay"""
        if hasattr(self, 'overlay') and self.overlay:
            self.overlay.destroy()
            self.overlay = None

    def update_position_ui(self, x, y):
        """Met à jour l'interface après sélection de position"""
        self.position_label.config(text=f"Position sélectionnée: X={x}, Y={y}", fg='#2ecc71')
        self.status_label.config(text="✅ Position configurée avec succès!", fg='#2ecc71')
        self.root.deiconify()  # Réafficher la fenêtre

    def show_error_ui(self):
        """Affiche l'erreur dans l'interface"""
        self.status_label.config(text="❌ Erreur lors de la sélection", fg='#e74c3c')
        self.root.deiconify()  # Réafficher la fenêtre

    def setup_hotkeys(self):
        """Configure les raccourcis clavier globaux"""
        try:
            keyboard.add_hotkey('f6', self.start_clicking)
            keyboard.add_hotkey('f7', self.stop_clicking)
        except Exception as e:
            print(f"Erreur lors de la configuration des raccourcis: {e}")

    def start_clicking(self):
        """Démarre le processus de clics automatiques"""
        if self.is_clicking:
            return

        if self.click_x == 0 and self.click_y == 0:
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner une position!")
            return

        try:
            self.is_clicking = True
            self.status_label.config(text="Clics en cours...", fg='#e67e22')
            self.start_btn.config(state='disabled')

            self.click_thread = threading.Thread(target=self.clicking_loop)
            self.click_thread.daemon = True
            self.click_thread.start()
        except Exception as e:
            print(f"Erreur lors du démarrage des clics: {e}")
            self.stop_clicking()

    def stop_clicking(self):
        """Arrête le processus de clics automatiques"""
        self.is_clicking = False
        self.start_btn.config(state='normal')

        # Arrêter proprement le listener de souris s'il existe
        if self.mouse_listener and self.mouse_listener.running:
            try:
                self.mouse_listener.stop()
                self.mouse_listener.join(timeout=1)
            except:
                pass

        self.status_label.config(text="Arrêté", fg='#e74c3c')

    def update_click_method(self):
        """Met à jour la méthode de clic sélectionnée"""
        self.click_method = self.click_method_var.get()
        print(f"Méthode de clic changée: {self.click_method}")

    def clicking_loop(self):
        """Boucle principale d'exécution des clics"""
        try:
            count = self.count_var.get()
            clicks_done = 0

            while self.is_clicking:
                if count > 0 and clicks_done >= count:
                    break

                # Mettre à jour les paramètres depuis l'interface
                self.click_method = self.click_method_var.get()
                self.humanize_clicks = self.humanize_var.get()
                self.random_intervals = self.random_interval_var.get()

                # Choisir la méthode de clic appropriée
                success = False
                if self.click_method == "windows_api":
                    if self.humanize_clicks:
                        success = AdvancedClicker.human_like_click(self.click_x, self.click_y)
                    else:
                        # Clic simple sans humanisation
                        try:
                            win32api.SetCursorPos((self.click_x, self.click_y))
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, self.click_x, self.click_y, 0, 0)
                            time.sleep(0.01)
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, self.click_x, self.click_y, 0, 0)
                            success = True
                        except:
                            success = False

                elif self.click_method == "sendmessage":
                    success = AdvancedClicker.sendmessage_click(self.click_x, self.click_y)
                elif self.click_method == "postmessage":
                    success = AdvancedClicker.postmessage_click(self.click_x, self.click_y)

                if success:
                    clicks_done += 1

                # Mettre à jour le statut de manière thread-safe
                if count > 0:
                    remaining = count - clicks_done
                    self.root.after(0, lambda c=clicks_done, t=count, r=remaining: self.status_label.config(
                        text=f"Clics: {c}/{t} (Restant: {r})", fg='#e67e22'))
                else:
                    self.root.after(0, lambda c=clicks_done: self.status_label.config(
                        text=f"Clics effectués: {c}", fg='#e67e22'))

                # Calculer l'intervalle d'attente
                base_interval = self.interval_var.get()
                if self.random_intervals:
                    # Variation aléatoire de ±50%
                    variation = random.uniform(*INTERVAL_RANDOMNESS)
                    actual_interval = base_interval * variation
                else:
                    actual_interval = base_interval

                time.sleep(actual_interval)

            self.is_clicking = False
            self.root.after(0, lambda: self.status_label.config(text="Terminé", fg='#2ecc71'))
            self.root.after(0, lambda: self.start_btn.config(state='normal'))
        except Exception as e:
            print(f"Erreur dans la boucle de clics: {e}")
            self.root.after(0, self.stop_clicking)

def main():
    root = tk.Tk()
    app = AutoClickerApp(root)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
