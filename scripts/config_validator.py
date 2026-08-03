from pathlib import Path
from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

REQUIRED_VARIABLES = [
    "APP_NAME",
    "APP_VERSION",
    "HOST",
    "PORT",
    "LOG_LEVEL",
]


def validate_config():
    if not ENV_FILE.exists():
        print(".env file not found.")
        return

    config = dotenv_values(ENV_FILE)

    print("=" * 40)
    print("Configuration Validation")
    print("=" * 40)

    valid = True

    for variable in REQUIRED_VARIABLES:
        if config.get(variable):
            print(f"✓ {variable}")
        else:
            print(f"✗ {variable} (Missing)")
            valid = False

    print("\nResult:")
    if valid:
        print("Configuration is valid.")
    else:
        print("Configuration validation failed.")


if __name__ == "__main__":
    validate_config()