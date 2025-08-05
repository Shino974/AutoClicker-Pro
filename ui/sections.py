#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sections de l'interface utilisateur
==================================

Ce module contient les classes pour construire les différentes sections
de l'interface utilisateur (position, fréquence, anti-détection, etc.)
"""

import tkinter as tk
from tkinter import ttk
from language_manager import lang_manager


class UISections:
    """Classe pour construire les sections de l'interface utilisateur"""

    @staticmethod
    def build_position_content(parent, app_instance):
        """Construit le contenu de la section position"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        app_instance.position_label = tk.Label(content, text=lang_manager.get_text('no_position'),
                                     font=('Arial', 11), bg='#34495e', fg='#e74c3c')
        app_instance.position_label.pack(pady=(0, 15))

        app_instance.select_pos_btn = tk.Button(content, text=lang_manager.get_text('select_position'),
                                  command=app_instance.start_position_selection,
                                  bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                  relief='flat', bd=0, padx=20, pady=10,
                                  cursor='hand2', activebackground='#2980b9')
        app_instance.select_pos_btn.pack(pady=(0, 10))

        app_instance.position_instruction_label = tk.Label(content, text=lang_manager.get_text('position_instruction'),
                                    font=('Arial', 9), bg='#34495e', fg='#bdc3c7',
                                    wraplength=350, justify='center')
        app_instance.position_instruction_label.pack()

    @staticmethod
    def build_frequency_content(parent, app_instance):
        """Construit le contenu de la section fréquence"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        # Options de fréquence prédéfinies
        freq_preset_frame = tk.Frame(content, bg='#34495e')
        freq_preset_frame.pack(pady=5)

        app_instance.presets_label = tk.Label(freq_preset_frame, text=lang_manager.get_text('presets_label'),
                                     font=('Arial', 9, 'bold'), bg='#34495e', fg='white')
        app_instance.presets_label.pack(anchor='w')

        preset_buttons_frame = tk.Frame(freq_preset_frame, bg='#34495e')
        preset_buttons_frame.pack()

        # Stocker les boutons presets pour la mise à jour
        app_instance.preset_buttons = []

        presets = [
            ('slow_preset', 2.0),
            ('normal_preset', 1.0),
            ('fast_preset', 0.5),
            ('ultra_preset', 0.1)
        ]

        for text_key, value in presets:
            btn = tk.Button(preset_buttons_frame, text=lang_manager.get_text(text_key),
                           command=lambda v=value: app_instance.set_interval_preset(v),
                           bg='#2c3e50', fg='white', font=('Arial', 8),
                           relief='raised', bd=1, width=12)
            btn.pack(side='left', padx=2)
            btn.text_key = text_key
            app_instance.preset_buttons.append(btn)

        # Intervalle personnalisé
        custom_frame = tk.Frame(content, bg='#34495e')
        custom_frame.pack(pady=10)

        app_instance.custom_interval_label = tk.Label(custom_frame, text=lang_manager.get_text('custom_interval'),
                font=('Arial', 10, 'bold'), bg='#34495e', fg='white')
        app_instance.custom_interval_label.pack()

        interval_control_frame = tk.Frame(custom_frame, bg='#34495e')
        interval_control_frame.pack()

        app_instance.interval_var = tk.DoubleVar(value=1.0)

        # Entry pour saisie directe
        app_instance.interval_entry = tk.Entry(interval_control_frame, textvariable=app_instance.interval_var,
                                      width=8, font=('Arial', 12), justify='center')
        app_instance.interval_entry.pack(side='left', padx=5)

        # Scale pour ajustement visuel
        interval_scale = tk.Scale(interval_control_frame, from_=0.01, to=10.0, resolution=0.01,
                                orient='horizontal', variable=app_instance.interval_var,
                                bg='#34495e', fg='white', highlightbackground='#34495e',
                                length=200)
        interval_scale.pack(side='left', padx=5)

        # Affichage fréquence en clics/minute
        app_instance.freq_display = tk.Label(custom_frame, text="60 clics/minute",
                                    font=('Arial', 9), bg='#34495e', fg='#f39c12')
        app_instance.freq_display.pack(pady=2)

        # Liaison pour mise à jour automatique
        app_instance.interval_var.trace('w', app_instance.update_frequency_display)

    @staticmethod
    def build_antidetect_content(parent, app_instance):
        """Construit le contenu de la section anti-détection"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        # Méthode de clic
        method_frame = tk.Frame(content, bg='#34495e')
        method_frame.pack(pady=5)

        app_instance.click_method_label = tk.Label(method_frame, text=lang_manager.get_text('click_method'),
                                          font=('Arial', 10, 'bold'), bg='#34495e', fg='white')
        app_instance.click_method_label.pack(anchor='w')

        app_instance.click_method_var = tk.StringVar(value="windows_api")

        # Stocker les radiobuttons pour la mise à jour
        app_instance.method_radiobuttons = []

        methods = [
            ('windows_api_method', "windows_api"),
            ('sendmessage_method', "sendmessage"),
            ('postmessage_method', "postmessage")
        ]

        for text_key, value in methods:
            rb = tk.Radiobutton(method_frame, text=lang_manager.get_text(text_key),
                               variable=app_instance.click_method_var, value=value,
                               bg='#34495e', fg='white', selectcolor='#2c3e50',
                               font=('Arial', 9), command=app_instance.update_click_method)
            rb.pack(anchor='w')
            rb.text_key = text_key
            app_instance.method_radiobuttons.append(rb)

        # Options d'humanisation
        humanize_frame = tk.Frame(content, bg='#34495e')
        humanize_frame.pack(pady=5)

        app_instance.humanize_var = tk.BooleanVar(value=True)
        app_instance.humanize_cb = tk.Checkbutton(humanize_frame, text=lang_manager.get_text('humanize_clicks'),
                                    variable=app_instance.humanize_var, bg='#34495e', fg='white',
                                    selectcolor='#2c3e50', font=('Arial', 9))
        app_instance.humanize_cb.pack(anchor='w')

        app_instance.random_interval_var = tk.BooleanVar(value=True)
        app_instance.random_interval_cb = tk.Checkbutton(humanize_frame, text=lang_manager.get_text('random_intervals'),
                                  variable=app_instance.random_interval_var, bg='#34495e', fg='white',
                                  selectcolor='#2c3e50', font=('Arial', 9))
        app_instance.random_interval_cb.pack(anchor='w')

    @staticmethod
    def build_count_content(parent, app_instance):
        """Construit le contenu de la section nombre de clics"""
        content = tk.Frame(parent, bg='#34495e', padx=15, pady=15)
        content.pack(fill='x')

        app_instance.count_var = tk.IntVar(value=0)

        # Option infini
        infini_frame = tk.Frame(content, bg='#34495e')
        infini_frame.pack(pady=(0, 10))

        app_instance.count_mode_var = tk.StringVar(value="infini")

        app_instance.infini_rb = tk.Radiobutton(infini_frame, text=lang_manager.get_text('infinite_clicks'),
                                  variable=app_instance.count_mode_var, value="infini",
                                  bg='#34495e', fg='white', selectcolor='#2c3e50',
                                  font=('Arial', 11, 'bold'),
                                  command=lambda: app_instance.count_var.set(0))
        app_instance.infini_rb.pack(anchor='w')

        # Saisie personnalisée
        custom_frame = tk.Frame(content, bg='#34495e')
        custom_frame.pack()

        app_instance.custom_count_rb = tk.Radiobutton(custom_frame, text=lang_manager.get_text('custom_count'),
                                  variable=app_instance.count_mode_var, value="custom",
                                  bg='#34495e', fg='white', selectcolor='#2c3e50',
                                  font=('Arial', 11, 'bold'))
        app_instance.custom_count_rb.pack(anchor='w', pady=(0, 5))

        count_entry = tk.Entry(custom_frame, textvariable=app_instance.count_var, width=15,
                              font=('Arial', 12), justify='center')
        count_entry.pack(pady=(0, 5))

        # Bind pour activer le mode custom quand on tape dans le champ
        def on_entry_focus(event):
            app_instance.count_mode_var.set("custom")

        count_entry.bind("<FocusIn>", on_entry_focus)
        count_entry.bind("<KeyPress>", on_entry_focus)
