import sys
import os
import site


def is_venv(pref: str, basepref: str) -> bool:
    return pref != basepref

def in_matrix() -> None:
    venv = "Welcome to the construct"
    print(f"MATRIX STATUS: {venv}\n")
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
    print(f"Environment Path: {sys.prefix}")
    elements = site.getsitepackages()
    print(
        "\nSUCCESS: You’re in an isolated environment!\n"
        "Safe to install packages without affecting\n"
        "the global system.\n"
        "\nPackage installation path:\n"
        f"{elements[0]}"
    )
 

def out_matrix() -> None:
    venv = "You’re still plugged in"
    print(f"MATRIX STATUS: {venv}\n")
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected\n")
    print(
        "WARNING: You’re in the global environment!\n"
        "The machines can see everything you install.\n"
    )
    print(
        "To enter the construct, run:\n"
        "python -m venv matrix_env\n"
        "source matrix_env/bin/activate # On Unix\n"
        "matrix_env\\Scripts\\activate # On Windows\n"
        "\nThen run this program again."
    )
    
if __name__ == "__main__":
    if is_venv(sys.prefix, sys.base_prefix):
        in_matrix()
    else:
        out_matrix()
        

