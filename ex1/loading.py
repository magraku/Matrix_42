import importlib
import sys


def analize() -> None:
    import numpy as npy
    import pandas as pds
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")
    n_points = 1000
    rng = npy.random.default_rng()
    data = rng.integers(0, 49, n_points)
    print(f"Processing {n_points} data points...")
    table = pds.DataFrame({"height": data})
    print(table["height"].mean())
    print(table["height"].std())
    print("Generating visualization...\n")
    plt.hist(data)
    plt.title("Matrix data distribution")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig("matrix_analysis.png")
    plt.close()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def pack_dispo(pack_name: str) -> tuple[bool, str]:
    try:
        modulo = importlib.import_module(pack_name)
    except ModuleNotFoundError:
        return False, ""
    else:
        version = getattr(modulo, "__version__", "unknown")
        return True, version


def show_versions(packs: dict[str, str]) -> None:
    print("\nEnvironment comparison:")

    if "pypoetry" in sys.prefix:
        manager = "Poetry"
    else:
        manager = "pip (venv)"
    print(f"Environment: {manager}")
    for name in packs:
        dispo, version = pack_dispo(name)
        print(f"{name}: {version}")
    print(
        "pip:    requirements.txt -> pip install -r requirements.txt"
        "\nPoetry: pyproject.toml + poetry.lock -> poetry install"
    )


def main() -> None:
    packs = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready"
    }
    missing: list[str] = []
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")
    for name, description in packs.items():
        dispo, version = pack_dispo(name)
        if dispo:
            print(
                f"[OK] {name} ({version}) - {description}"
            )
        else:
            print(
                f"[MISSING] {name} - Not installed"
            )
            missing.append(name)
    if missing:
        print(
            "Installation:\nUsing pip:\n"
            "pip install -r requirements.txt"
            "\nUsing Poetry:\n"
            "poetry install"
            )
        sys.exit(1)
    show_versions(packs)
    analize()


if __name__ == "__main__":
    main()
