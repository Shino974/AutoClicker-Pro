#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application principale Auto Clicker Pro
======================================

Ce module contient la classe principale de l'application avec l'interface utilisateur.
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

from config.constants import WINDOW_GEOMETRY, WINDOW_MIN_SIZE, WINDOW_BG_COLOR, INTERVAL_RANDOMNESS
from language_manager import lang_manager
from advanced_clicker import AdvancedClicker
from ui.sections import UISections


class AutoClickerApp:
    """
    Application principale de l'Auto Clicker avec interface graphique moderne.

    Cette classe gère l'interface utilisateur, la configuration des paramètres,
    et l'orchestration des différentes méthodes de clic anti-détection.
    """

    def __init__(self, root: tk.Tk):
        """
        Initialise l'application Auto Clicker.

        Args:
            root (tk.Tk): Instance de la fenêtre principale Tkinter
        """
        # Configuration de la fenêtre principale
        self.root = root
        self.root.title(lang_manager.get_text('app_title'))
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.configure(bg=WINDOW_BG_COLOR)
        self.root.resizable(True, True)
        self.root.minsize(*WINDOW_MIN_SIZE)

        # Variables d'état de l'application
        self.is_clicking = False
        self.click_x = 0
        self.click_y = 0
        self.click_thread = None
        self.mouse_listener = None
        self.target_window = None

        # Paramètres anti-détection par défaut
        self.humanize_clicks = True
        self.random_intervals = True
        self.click_method = "windows_api"

        # Initialisation de l'interface et des raccourcis
        self.setup_ui()
        self.setup_hotkeys()

    def setup_ui(self):
        """Configure l'interface utilisateur principale."""
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

        # Container pour titre et drapeaux de langue
        header_content = tk.Frame(header_frame, bg='#2c3e50')
        header_content.pack(fill='both', expand=True, padx=15)

        # Drapeaux de langue (en haut à droite)
        language_frame = tk.Frame(header_content, bg='#2c3e50')
        language_frame.pack(side='right', anchor='ne', pady=(10, 0))

        # Drapeau français
        self.fr_flag_btn = tk.Button(language_frame, text='🇫🇷', font=('Arial', 20),
                                    command=lambda: self.change_language('fr'),
                                    bg='#2c3e50', fg='white', relief='flat', bd=0,
                                    cursor='hand2', activebackground='#34495e')
        self.fr_flag_btn.pack(side='left', padx=2)

        # Drapeau anglais
        self.en_flag_btn = tk.Button(language_frame, text='🇺🇸', font=('Arial', 20),
                                    command=lambda: self.change_language('en'),
                                    bg='#2c3e50', fg='white', relief='flat', bd=0,
                                    cursor='hand2', activebackground='#34495e')
        self.en_flag_btn.pack(side='left', padx=2)

        # Indicateur de langue active
        self.lang_indicator = tk.Label(language_frame, text='●', font=('Arial', 8),
                                      bg='#2c3e50', fg='#27ae60')
        self.lang_indicator.pack(pady=(0, 5))

        # Conteneur pour le titre centré
        title_container = tk.Frame(header_content, bg='#2c3e50')
        title_container.pack(expand=True)

        self.title_label = tk.Label(title_container, text=lang_manager.get_text('app_title'),
                              font=('Arial', 20, 'bold'), bg='#2c3e50', fg='white')
        self.title_label.pack(pady=(15, 0))

        self.subtitle_label = tk.Label(title_container, text=lang_manager.get_text('app_subtitle'),
                                 font=('Arial', 10), bg='#2c3e50', fg='#bdc3c7')
        self.subtitle_label.pack()

        # Container principal pour le scroll
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Canvas avec scrollbar
        canvas = tk.Canvas(main_container, bg='#2c3e50', highlightthickness=0,
                          relief='flat', borderwidth=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview,
                                 style="Vertical.TScrollbar")
        scrollable_frame = tk.Frame(canvas, bg='#2c3e50')

        # Configuration du scroll
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas_width = canvas.winfo_width()
            canvas.itemconfig(window_id, width=canvas_width)

        scrollable_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)

        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame principal
        main_frame = tk.Frame(scrollable_frame, bg='#34495e', relief='flat', bd=0,
                             highlightbackground='#5d6d7e', highlightthickness=1)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Variables pour sections collapsibles
        self.pos_collapsed = tk.BooleanVar(value=False)
        self.freq_collapsed = tk.BooleanVar(value=False)
        self.anti_collapsed = tk.BooleanVar(value=False)
        self.count_collapsed = tk.BooleanVar(value=False)

        self.toggle_buttons = {}

        # Création des sections
        self.create_modern_section(main_frame, "pos", "🎯", lang_manager.get_text('position_section'),
                                  lambda parent: UISections.build_position_content(parent, self),
                                  self.toggle_pos_section)

        self.create_modern_section(main_frame, "freq", "⚡", lang_manager.get_text('frequency_section'),
                                  lambda parent: UISections.build_frequency_content(parent, self),
                                  self.toggle_freq_section)

        self.create_modern_section(main_frame, "anti", "🛡️", lang_manager.get_text('antidetect_section'),
                                  lambda parent: UISections.build_antidetect_content(parent, self),
                                  self.toggle_anti_section)

        self.create_modern_section(main_frame, "count", "🔢", lang_manager.get_text('count_section'),
                                  lambda parent: UISections.build_count_content(parent, self),
                                  self.toggle_count_section)

        # Boutons de contrôle
        self.create_control_buttons(main_frame)

        # Status
        status_container = tk.Frame(main_frame, bg='#34495e')
        status_container.pack(fill='x', padx=15, pady=10)

        self.status_label = tk.Label(status_container, text=lang_manager.get_text('ready_status'),
                                   font=('Arial', 11, 'bold'), bg='#34495e', fg='#2ecc71',
                                   wraplength=400, justify='center')
        self.status_label.pack(pady=5)

        # Footer
        footer_frame = tk.Frame(self.root, bg='#2c3e50', height=35)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        self.footer_label = tk.Label(footer_frame,
                              text=lang_manager.get_text('footer_text'),
                              font=('Arial', 9), bg='#2c3e50', fg='#bdc3c7')
        self.footer_label.pack(pady=8)

        # Bind de la molette de souris
        self.bind_mousewheel_to_canvas(canvas)

        # Références
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame
        self.main_frame = main_frame

        # Mettre à jour l'indicateur de langue
        self.update_language_indicator()

    def create_modern_section(self, parent, section_key, icon, title, content_builder, toggle_func):
        """Crée une section moderne avec header cliquable"""
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

        # Status indicator
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
                try:
                    child.configure(bg='#4a5568')
                except:
                    pass
            title_frame.configure(bg='#4a5568')

        def on_hover_leave(event):
            header.configure(bg='#3e4651')
            header_content.configure(bg='#3e4651')
            for child in header_content.winfo_children():
                try:
                    child.configure(bg='#3e4651')
                except:
                    pass
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
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        def bind_to_mousewheel(widget):
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel)
            widget.bind("<Button-5>", _on_mousewheel)

        bind_to_mousewheel(canvas)
        bind_to_mousewheel(self.root)

        def bind_tree(widget):
            bind_to_mousewheel(widget)
            for child in widget.winfo_children():
                bind_tree(child)

        self.root.after(100, lambda: bind_tree(self.scrollable_frame))

    def create_control_buttons(self, parent):
        """Crée les boutons de contrôle avec design moderne"""
        control_container = tk.Frame(parent, bg='#34495e')
        control_container.pack(fill='x', padx=15, pady=20)

        self.start_btn = tk.Button(control_container, text=lang_manager.get_text('start_button'),
                                  command=self.start_clicking,
                                  bg='#27ae60', fg='white', font=('Arial', 14, 'bold'),
                                  relief='flat', bd=0, padx=20, pady=15, cursor='hand2',
                                  activebackground='#219a52')
        self.start_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

        self.stop_btn = tk.Button(control_container, text=lang_manager.get_text('stop_button'),
                                 command=self.stop_clicking,
                                 bg='#e74c3c', fg='white', font=('Arial', 14, 'bold'),
                                 relief='flat', bd=0, padx=20, pady=15, cursor='hand2',
                                 activebackground='#c0392b')
        self.stop_btn.pack(side='left', fill='x', expand=True, padx=(5, 0))

    # Toggle methods for sections
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
                if hasattr(self, 'freq_display'):
                    self.freq_display.config(text=lang_manager.get_text('clicks_per_minute').format(freq))
            else:
                if hasattr(self, 'freq_display'):
                    self.freq_display.config(text="Invalid")
        except:
            if hasattr(self, 'freq_display'):
                self.freq_display.config(text="Invalid")

    def manual_position_input(self):
        """Saisie manuelle de la position de clic"""
        dialog = tk.Toplevel(self.root)
        dialog.title(lang_manager.get_text('manual_position_title'))
        dialog.geometry("300x150")
        dialog.configure(bg='#34495e')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text=lang_manager.get_text('position_x'), font=('Arial', 10),
                bg='#34495e', fg='white').pack(pady=5)
        x_entry = tk.Entry(dialog, font=('Arial', 10), justify='center')
        x_entry.pack(pady=2)

        tk.Label(dialog, text=lang_manager.get_text('position_y'), font=('Arial', 10),
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
                self.status_label.config(text=lang_manager.get_text('position_manual'), fg='#2ecc71')
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Erreur", lang_manager.get_text('invalid_numbers'))

        tk.Button(dialog, text=lang_manager.get_text('confirm_button'), command=save_position,
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)

    def start_position_selection(self):
        """Lance la sélection de position - l'utilisateur clique où il veut"""
        try:
            self.status_label.config(text=lang_manager.get_text('position_selecting'), fg='#f39c12')

            if self.mouse_listener:
                try:
                    self.mouse_listener.stop()
                except:
                    pass
                self.mouse_listener = None

            self.create_capture_overlay()

        except Exception as e:
            print(f"Erreur lors du démarrage de la sélection: {e}")
            self.status_label.config(text=lang_manager.get_text('position_error'), fg='#e74c3c')

    def create_capture_overlay(self):
        """Crée une fenêtre transparente plein écran pour capturer la position"""
        self.overlay = tk.Toplevel(self.root)
        self.overlay.title("Sélection de position")
        self.overlay.configure(bg='black')
        self.overlay.attributes('-alpha', 0.3)
        self.overlay.attributes('-topmost', True)
        self.overlay.attributes('-fullscreen', True)
        self.overlay.configure(cursor="crosshair")

        self.root.withdraw()

        instruction = tk.Label(self.overlay,
                              text=lang_manager.get_text('overlay_instruction'),
                              font=('Arial', 16, 'bold'),
                              bg='black', fg='white',
                              justify='center')
        instruction.pack(expand=True)

        self.overlay.bind('<Button-1>', self.on_overlay_click)
        self.overlay.bind('<Escape>', self.cancel_position_selection)
        self.overlay.focus_set()

    def on_overlay_click(self, event):
        """Capture la position lors du clic sur l'overlay"""
        try:
            x = self.overlay.winfo_pointerx()
            y = self.overlay.winfo_pointery()

            self.click_x = x
            self.click_y = y

            self.close_overlay()
            self.update_position_ui(x, y)

        except Exception as e:
            print(f"Erreur lors de la capture de position: {e}")
            self.close_overlay()
            self.show_error_ui()

    def cancel_position_selection(self, event=None):
        """Annule la sélection de position"""
        self.close_overlay()
        self.status_label.config(text=lang_manager.get_text('position_cancelled'), fg='#e74c3c')
        self.root.deiconify()

    def close_overlay(self):
        """Ferme la fenêtre overlay"""
        if hasattr(self, 'overlay') and self.overlay:
            self.overlay.destroy()
            self.overlay = None

    def update_position_ui(self, x, y):
        """Met à jour l'interface après sélection de position"""
        self.position_label.config(text=lang_manager.get_text('position_selected').format(x, y), fg='#2ecc71')
        self.status_label.config(text=lang_manager.get_text('position_configured'), fg='#2ecc71')
        self.root.deiconify()

    def show_error_ui(self):
        """Affiche l'erreur dans l'interface"""
        self.status_label.config(text=lang_manager.get_text('position_error'), fg='#e74c3c')
        self.root.deiconify()

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
            messagebox.showwarning("Attention", lang_manager.get_text('select_position_first'))
            return

        try:
            self.is_clicking = True
            self.status_label.config(text=lang_manager.get_text('clicking_status'), fg='#e67e22')
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

        if self.mouse_listener and hasattr(self.mouse_listener, 'running') and self.mouse_listener.running:
            try:
                self.mouse_listener.stop()
                self.mouse_listener.join(timeout=1)
            except:
                pass

        self.status_label.config(text=lang_manager.get_text('stopped_status'), fg='#e74c3c')

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

                self.click_method = self.click_method_var.get()
                self.humanize_clicks = self.humanize_var.get()
                self.random_intervals = self.random_interval_var.get()

                success = False
                if self.click_method == "windows_api":
                    if self.humanize_clicks:
                        success = AdvancedClicker.human_like_click(self.click_x, self.click_y)
                    else:
                        success = AdvancedClicker.simple_click(self.click_x, self.click_y)
                elif self.click_method == "sendmessage":
                    success = AdvancedClicker.sendmessage_click(self.click_x, self.click_y)
                elif self.click_method == "postmessage":
                    success = AdvancedClicker.postmessage_click(self.click_x, self.click_y)

                if success:
                    clicks_done += 1

                # Mettre à jour le statut
                if count > 0:
                    remaining = count - clicks_done
                    self.root.after(0, lambda c=clicks_done, t=count, r=remaining: self.status_label.config(
                        text=lang_manager.get_text('clicks_progress').format(c, t, r), fg='#e67e22'))
                else:
                    self.root.after(0, lambda c=clicks_done: self.status_label.config(
                        text=lang_manager.get_text('clicks_done').format(c), fg='#e67e22'))

                # Calculer l'intervalle d'attente
                base_interval = self.interval_var.get()
                if self.random_intervals:
                    variation = random.uniform(*INTERVAL_RANDOMNESS)
                    actual_interval = base_interval * variation
                else:
                    actual_interval = base_interval

                time.sleep(actual_interval)

            self.is_clicking = False
            self.root.after(0, lambda: self.status_label.config(text=lang_manager.get_text('finished_status'), fg='#2ecc71'))
            self.root.after(0, lambda: self.start_btn.config(state='normal'))
        except Exception as e:
            print(f"Erreur dans la boucle de clics: {e}")
            self.root.after(0, self.stop_clicking)

    def update_language_indicator(self):
        """Met à jour la position de l'indicateur de langue active"""
        if lang_manager.current_language == 'fr':
            self.lang_indicator.place(in_=self.fr_flag_btn, relx=0.5, rely=1.0, anchor='n')
        else:
            self.lang_indicator.place(in_=self.en_flag_btn, relx=0.5, rely=1.0, anchor='n')

    def change_language(self, lang_code):
        """Change la langue de l'application et met à jour l'interface"""
        if lang_manager.set_language(lang_code):
            self.update_interface_language()
            self.update_language_indicator()
            print(f"Langue changée vers: {lang_code}")

    def update_interface_language(self):
        """Met à jour tous les textes de l'interface selon la langue sélectionnée"""
        self.root.title(lang_manager.get_text('app_title'))
        self.title_label.config(text=lang_manager.get_text('app_title'))
        self.subtitle_label.config(text=lang_manager.get_text('app_subtitle'))

        if hasattr(self, 'position_label'):
            if self.click_x == 0 and self.click_y == 0:
                self.position_label.config(text=lang_manager.get_text('no_position'))
            else:
                self.position_label.config(text=lang_manager.get_text('position_selected').format(self.click_x, self.click_y))

        if hasattr(self, 'select_pos_btn'):
            self.select_pos_btn.config(text=lang_manager.get_text('select_position'))

        if hasattr(self, 'position_instruction_label'):
            self.position_instruction_label.config(text=lang_manager.get_text('position_instruction'))

        if hasattr(self, 'presets_label'):
            self.presets_label.config(text=lang_manager.get_text('presets_label'))

        if hasattr(self, 'preset_buttons'):
            for btn in self.preset_buttons:
                if hasattr(btn, 'text_key'):
                    btn.config(text=lang_manager.get_text(btn.text_key))

        if hasattr(self, 'custom_interval_label'):
            self.custom_interval_label.config(text=lang_manager.get_text('custom_interval'))

        if hasattr(self, 'click_method_label'):
            self.click_method_label.config(text=lang_manager.get_text('click_method'))

        if hasattr(self, 'method_radiobuttons'):
            for rb in self.method_radiobuttons:
                if hasattr(rb, 'text_key'):
                    rb.config(text=lang_manager.get_text(rb.text_key))

        if hasattr(self, 'humanize_cb'):
            self.humanize_cb.config(text=lang_manager.get_text('humanize_clicks'))

        if hasattr(self, 'random_interval_cb'):
            self.random_interval_cb.config(text=lang_manager.get_text('random_intervals'))

        if hasattr(self, 'infini_rb'):
            self.infini_rb.config(text=lang_manager.get_text('infinite_clicks'))

        if hasattr(self, 'custom_count_rb'):
            self.custom_count_rb.config(text=lang_manager.get_text('custom_count'))

        if hasattr(self, 'start_btn'):
            self.start_btn.config(text=lang_manager.get_text('start_button'))

        if hasattr(self, 'stop_btn'):
            self.stop_btn.config(text=lang_manager.get_text('stop_button'))

        if self.click_x == 0 and self.click_y == 0:
            if hasattr(self, 'status_label'):
                self.status_label.config(text=lang_manager.get_text('ready_status'))

        if hasattr(self, 'footer_label'):
            self.footer_label.config(text=lang_manager.get_text('footer_text'))

        self.update_frequency_display()
        self.root.update_idletasks()
