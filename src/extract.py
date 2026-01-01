"""
Step 1 — Extract / Raw Validation (PoC → Historical Ready)

This script validates the presence of raw Arbetsförmedlingen job ad data.
Raw data is treated as immutable.
"""

from pathlib import Path

RAW_BASE_DIR = Path("data/raw/arbetsformedlingen")


def validate_raw_base(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Raw base directory not found at {path}. "
            "Place historical datasets before continuing."
        )

    print(f"Raw base directory found: {path}")


def list_available_years(base_dir: Path) -> None:
    years = sorted(p.name for p in base_dir.iterdir() if p.is_dir())
    print("Available raw years:", ", ".join(years))


if __name__ == "__main__":
    validate_raw_base(RAW_BASE_DIR)
    list_available_years(RAW_BASE_DIR)
