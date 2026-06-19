import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from password_manager.ui.app import PasswordManagerApp


def main():
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
