import os
import sys


def load_config() -> tuple[dict[str, str | None], bool]:
    there_is_override = False
    archive: dict[str, str | None] = {}
    try:
        from dotenv import load_dotenv
        from dotenv import dotenv_values
    except ModuleNotFoundError:
        print(
            "[WARNING] python-dotenv not installed.\n"
            "Install it with:\n"
            "pip install python-dotenv"
              )
    else:
        load_dotenv()
        archive = dotenv_values('.env')
    dict_name = {
        "MATRIX_MODE": "development", "DATABASE_URL": None,
        "API_KEY": None, "LOG_LEVEL": "DEBUG",
        "ZION_ENDPOINT": None
    }
    terminal_dict = os.environ
    for name, value in dict_name.items():
        dict_name[name] = os.getenv(name, value)
        terminal_value = terminal_dict.get(name)
        if terminal_value == archive.get(name):
            pass
        else:
            there_is_override = True
    return dict_name, there_is_override


def security_api(config: dict[str, str | None]) -> None:
    warning_names = [
        "API_KEY", "PASSWORD", "SECRET",
        "TOKEN", "ACCESS_KEY",
    ]
    with open(__file__, "r") as file:
        content = file.read()
    for line in content.splitlines():
        line = line.strip()
        if "=" in line:
            parts = line.split("=", 1)
            if parts[0].startswith("#"):
                parts[0] = parts[0][1:].strip()
            name = parts[0].strip()
            if name.upper() in warning_names:
                print("[WARNING] Potential hardcoded secrets detected")
                return
    print("[OK] No hardcoded secrets detected")


def security_env(config: dict[str, str | None]) -> None:
    missing = [
        "MATRIX_MODE", "DATABASE_URL", "API_KEY",
        "LOG_LEVEL", "ZION_ENDPOINT"
    ]
    if os.path.isfile(".env"):
        try:
            from dotenv import dotenv_values
        except ModuleNotFoundError:
            print(
                "[WARNING] python-dotenv not installed.\n"
                "Install it with:\n"
                "pip install python-dotenv"
            )
        else:
            env_dict = dotenv_values('.env')
            for name, value in env_dict.items():
                if name in missing and value:
                    missing.remove(name)
        if missing:
            print("[WARNING] required configuration missing")
        else:
            print("[OK] .env file properly configured")
    else:
        print("[ERROR] .env file not found")


def missing_config(config: dict[str, str | None]) -> list[str]:
    missing: list[str] = []
    for key, value in config.items():
        if value is None or not value.strip():
            missing.append(key)
    return missing


def show_config(config: dict[str, str | None]) -> None:

    mode = config["MATRIX_MODE"]
    if mode is None or not mode.strip():
        print("Mode: Missing")
    else:
        mode = mode.strip()
        if mode == "development":
            print("Mode: development")
        elif mode == "production":
            print("Mode: production")
        else:
            print("Mode: Incorrect Mode")

    db = config["DATABASE_URL"]
    if db is None or not db.strip():
        print("Database: Missing")
    elif "localhost" in db:
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to remote database")

    api = config["API_KEY"]
    if api is None or not api.strip():
        print("API Access: Missing")
    else:
        print("API Access: Authenticated")
    level = config["LOG_LEVEL"]
    if level is None or not level.strip():
        print("Log Level: Missing")
    else:
        print(f"Log Level: {level}")

    zion = config["ZION_ENDPOINT"]
    if zion is None or not zion.strip():
        print("Zion Network: Offline")
    else:
        print("Zion Network: Online")


if __name__ == "__main__":
    print("ORACLE STATUS: Reading the Matrix...")
    print("\nConfiguration loaded:")
    config, there_is_override = load_config()
    show_config(config)
    missing = missing_config(config)

    print("\nEnvironment security check:")
    mode = config["MATRIX_MODE"]
    if mode == "production" and missing:
        print(
            "[ERROR] MATRIX_MODE=Production and"
            " configurations are missing"
            )
        sys.exit(1)
    security_api(config)
    security_env(config)

    if missing:
        print(f"[WARNING]: Missing configuration: {', '.join(missing)}")

    if there_is_override:
        print("[OK] Production overrides available.")
    else:
        print("[WARNING] Production overrides unavailable/unchecked.")

    print("\nThe Oracle sees all configurations.")
