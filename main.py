#!/usr/bin/env python3
"""
Password Manager - A secure password management application.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from password_manager.ui.app import PasswordManagerApp


def main():
    """Entry point for the Password Manager application."""
    try:
        app = PasswordManagerApp()
        app.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
