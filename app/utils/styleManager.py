import json
import os
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, Any

class StylePreferences(BaseModel):
    """Model for code style preferences"""
    indentation: str = "spaces"
    indent_size: int = 4
    max_line_length: int = 80
    naming_convention: str = "snake_case"

class StyleManager:
    """
    Manages user style preferences for code generation and translation.
    Handles loading and saving style preferences to a JSON file.
    """
    def __init__(self):
        self.preferences_dir = Path("preferences")
        self.preferences_file = self.preferences_dir / "style_preferences.json"
        self._ensure_preferences_dir()
        self._load_or_create_default()

    def _ensure_preferences_dir(self):
        """Make sure the preferences directory exists"""
        if not self.preferences_dir.exists():
            self.preferences_dir.mkdir(parents=True)
    
    def _load_or_create_default(self):
        """Load existing preferences or create default ones"""
        if not self.preferences_file.exists():
            default_prefs = StylePreferences()
            self.save_preferences(default_prefs)
            self.preferences = default_prefs
        else:
            self.load_preferences()
    
    def load_preferences(self) -> StylePreferences:
        """Load preferences from file"""
        try:
            with open(self.preferences_file, 'r') as f:
                data = json.load(f)
                self.preferences = StylePreferences(**data)
                return self.preferences
        except (json.JSONDecodeError, FileNotFoundError):
            self.preferences = StylePreferences()
            self.save_preferences(self.preferences)
            return self.preferences
    
    def save_preferences(self, preferences: StylePreferences) -> None:
        """Save preferences to file"""
        with open(self.preferences_file, 'w') as f:
            json.dump(preferences.dict(), f, indent=2)
        self.preferences = preferences
    
    def get_preferences_dict(self) -> Dict[str, Any]:
        """Get current style preferences as a dictionary"""
        try:
            prefs = self.load_preferences()
            return {
                "indentation": prefs.indentation,
                "indent_size": prefs.indent_size,
                "max_line_length": prefs.max_line_length,
                "naming_convention": prefs.naming_convention
            }
        except Exception as e:
            return {
                "indentation": "spaces",
                "indent_size": 4,
                "max_line_length": 80,
                "naming_convention": "snake_case"
            }

# Create a singleton instance
style_manager = StyleManager()