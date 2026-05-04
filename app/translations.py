# app/translations.py
"""UI string translations for EN and DE."""

UI_STRINGS = {
    "en": {
        # Navigation / header
        "logout": "Logout",
        "give_feedback": "Give Feedback",
        "documentation": "Documentation",
        "admin_console": "Admin Console",
        # Map instructions
        "map_instructions": "Left click to expand node.<br>Right click to open context menu.",
        # Input container
        "process_description": "Process Description",
        "process_textarea_placeholder": "Type your process description here...",
        "drag_drop_text": "Drag & drop a process diagram here",
        "browse_or": "or",
        "browse_link": "click to browse",
        "context_hint": "Click the icon to add more context about your process!",
        # Expert panel
        "additional_context": "Additional Context",
        "additional_context_placeholder": "Enter additional context about the company or process",
        "edit_few_shot_btn": "Edit Few Shot Examples",
        # Few-shot modal
        "few_shot_modal_title": "Edit Few Shot Examples",
        "retrieve_few_shot_btn": "Retrieve similar Few Shot Examples",
        # Start button
        "generate_workarounds": "Generate Workarounds",
        # Workaround list
        "workaround_list": "Workaround List",
        "download_workarounds": "Download Workarounds",
    },
    "de": {
        # Navigation / header
        "logout": "Abmelden",
        "give_feedback": "Feedback geben",
        "documentation": "Dokumentation",
        "admin_console": "Admin-Konsole",
        # Map instructions
        "map_instructions": "Linksklick zum Aufklappen.<br>Rechtsklick für das Kontextmenü.",
        # Input container
        "process_description": "Prozessbeschreibung",
        "process_textarea_placeholder": "Geben Sie hier Ihre Prozessbeschreibung ein...",
        "drag_drop_text": "Prozessdiagramm hierher ziehen & ablegen",
        "browse_or": "oder",
        "browse_link": "Datei auswählen",
        "context_hint": "Klicken Sie auf das Symbol, um weitere Informationen zu Ihrem Prozess hinzuzufügen!",
        # Expert panel
        "additional_context": "Zusätzlicher Kontext",
        "additional_context_placeholder": "Zusätzlichen Kontext zum Unternehmen oder Prozess eingeben",
        "edit_few_shot_btn": "Few-Shot-Beispiele bearbeiten",
        # Few-shot modal
        "few_shot_modal_title": "Few-Shot-Beispiele bearbeiten",
        "retrieve_few_shot_btn": "Ähnliche Few-Shot-Beispiele abrufen",
        # Start button
        "generate_workarounds": "Workarounds generieren",
        # Workaround list
        "workaround_list": "Workaround-Liste",
        "download_workarounds": "Workarounds herunterladen",
    },
}

SUPPORTED_LANGUAGES = ("en", "de")
DEFAULT_LANGUAGE = "en"


def get_translations(language: str) -> dict:
    """Return the UI string dictionary for the given language, falling back to EN."""
    return UI_STRINGS.get(language, UI_STRINGS[DEFAULT_LANGUAGE])
