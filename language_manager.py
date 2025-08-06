#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de langues pour Auto Clicker Pro
=============================================

Ce module gère la traduction et le changement de langue de l'application.
"""

class LanguageManager:
    """
    Gestionnaire de langues pour l'application.

    Permet de changer dynamiquement la langue de l'interface utilisateur
    entre français et anglais.
    """

    def __init__(self):
        """Initialise le gestionnaire de langues"""
        self.current_language = 'fr'  # Langue par défaut
        self.languages = {
            'fr': {
                # Interface principale
                'app_title': 'Auto Clicker Pro - Anti-Détection',
                'app_subtitle': '🛡️ Version Anti-Détection',
                'ready_status': '✅ Prêt - Configurez position et fréquence',
                'footer_text': 'F6: Démarrer | F7: Arrêter | By Shino974',

                # Sections
                'position_section': 'Position du clic',
                'frequency_section': 'Fréquence de clic',
                'antidetect_section': 'Options Anti-Détection',
                'count_section': 'Nombre de clics',

                # Position
                'no_position': 'Aucune position sélectionnée',
                'select_position': '🎯 Sélectionner Position',
                'position_instruction': 'Cliquez sur le bouton puis cliquez à l\'endroit désiré',
                'position_selected': 'Position sélectionnée: X={}, Y={}',
                'position_configured': '✅ Position configurée avec succès!',
                'position_manual': '✅ Position configurée manuellement',
                'position_selecting': '🎯 Cliquez à l\'endroit désiré pour définir la position...',
                'position_cancelled': '❌ Sélection annulée',
                'position_error': '❌ Erreur lors de la sélection',

                # Fréquence
                'presets_label': 'Presets:',
                'slow_preset': '🐌 Lent (2s)',
                'normal_preset': '🚶 Normal (1s)',
                'fast_preset': '🏃 Rapide (0.5s)',
                'ultra_preset': '⚡ Ultra (0.1s)',
                'custom_interval': 'Intervalle personnalisé (secondes):',
                'clicks_per_minute': '{:.1f} clics/minute',

                # Anti-détection
                'click_method': 'Méthode de clic:',
                'windows_api_method': '🎯 Windows API (Recommandé)',
                'sendmessage_method': '📨 SendMessage',
                'postmessage_method': '📤 PostMessage',
                'humanize_clicks': '🤖 Humaniser les clics (variations de position)',
                'random_intervals': '⏰ Intervalles aléatoires (±50%)',

                # Nombre de clics
                'infinite_clicks': '∞ Infini',
                'custom_count': 'Nombre personnalisé:',

                # Boutons
                'start_button': '🚀 DÉMARRER',
                'stop_button': '🛑 ARRÊTER',
                'confirm_button': 'Confirmer',
                'language_button': '🌐 Langue',

                # États
                'clicking_status': 'Clics en cours...',
                'stopped_status': 'Arrêté',
                'finished_status': 'Terminé',
                'clicks_progress': 'Clics: {}/{} (Restant: {})',
                'clicks_done': 'Clics effectués: {}',

                # Messages d'erreur
                'select_position_first': 'Veuillez d\'abord sélectionner une position!',
                'invalid_numbers': 'Veuillez entrer des nombres valides',
                'overlay_instruction': 'Cliquez à l\'endroit désiré pour définir la position de clic\nAppuyez sur Échap pour annuler',

                # Dialogue position manuelle
                'manual_position_title': 'Saisie manuelle de position',
                'position_x': 'Position X:',
                'position_y': 'Position Y:',
            },
            'en': {
                # Interface principale
                'app_title': 'Auto Clicker Pro - Anti-Detection',
                'app_subtitle': '🛡️ Anti-Detection Version',
                'ready_status': '✅ Ready - Configure position and frequency',
                'footer_text': 'F6: Start | F7: Stop | By Shino974',

                # Sections
                'position_section': 'Click Position',
                'frequency_section': 'Click Frequency',
                'antidetect_section': 'Anti-Detection Options',
                'count_section': 'Click Count',

                # Position
                'no_position': 'No position selected',
                'select_position': '🎯 Select Position',
                'position_instruction': 'Click the button then click where you want',
                'position_selected': 'Position selected: X={}, Y={}',
                'position_configured': '✅ Position configured successfully!',
                'position_manual': '✅ Position configured manually',
                'position_selecting': '🎯 Click where you want to set the click position...',
                'position_cancelled': '❌ Selection cancelled',
                'position_error': '❌ Selection error',

                # Fréquence
                'presets_label': 'Presets:',
                'slow_preset': '🐌 Slow (2s)',
                'normal_preset': '🚶 Normal (1s)',
                'fast_preset': '🏃 Fast (0.5s)',
                'ultra_preset': '⚡ Ultra (0.1s)',
                'custom_interval': 'Custom interval (seconds):',
                'clicks_per_minute': '{:.1f} clicks/minute',

                # Anti-détection
                'click_method': 'Click method:',
                'windows_api_method': '🎯 Windows API (Recommended)',
                'sendmessage_method': '📨 SendMessage',
                'postmessage_method': '📤 PostMessage',
                'humanize_clicks': '🤖 Humanize clicks (position variations)',
                'random_intervals': '⏰ Random intervals (±50%)',

                # Nombre de clics
                'infinite_clicks': '∞ Infinite',
                'custom_count': 'Custom count:',

                # Boutons
                'start_button': '🚀 START',
                'stop_button': '🛑 STOP',
                'confirm_button': 'Confirm',
                'language_button': '🌐 Language',

                # États
                'clicking_status': 'Clicking in progress...',
                'stopped_status': 'Stopped',
                'finished_status': 'Finished',
                'clicks_progress': 'Clicks: {}/{} (Remaining: {})',
                'clicks_done': 'Clicks performed: {}',

                # Messages d'erreur
                'select_position_first': 'Please select a position first!',
                'invalid_numbers': 'Please enter valid numbers',
                'overlay_instruction': 'Click where you want to set the click position\nPress Escape to cancel',

                # Dialogue position manuelle
                'manual_position_title': 'Manual Position Input',
                'position_x': 'Position X:',
                'position_y': 'Position Y:',
            }
        }

    def get_text(self, key):
        """Récupère un texte dans la langue actuelle"""
        return self.languages.get(self.current_language, {}).get(key, key)

    def set_language(self, lang_code):
        """Change la langue actuelle"""
        if lang_code in self.languages:
            self.current_language = lang_code
            return True
        return False

    def get_available_languages(self):
        """Retourne la liste des langues disponibles avec drapeaux"""
        return {
            'fr': '🇫🇷',
            'en': '🇺🇸'
        }


# Instance globale du gestionnaire de langues
lang_manager = LanguageManager()
