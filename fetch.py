# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///

"""
Fetch the numbers once, save the raw reply to data/, and never fetch again.

    uv run fetch.py

Fetch NASA POWER's daily solar-radiation data for Hong Kong in 2025.  This is
the raw source file for the ``solar-rhythm`` project; the plotting script must
read this committed file rather than make another network request.
"""

from pathlib import Path

import requests

URL = (
    "https://power.larc.nasa.gov/api/temporal/daily/point"
    "?parameters=ALLSKY_SFC_SW_DWN"
    "&community=RE"
    "&longitude=114.1694"
    "&latitude=22.3193"
    "&start=20250101"
    "&end=20251231"
    "&format=CSV"
)
FILE = "nasa-power-hong-kong-daily-solar-radiation-2025.csv"
HERE = Path(__file__).parent
DATA = HERE / "data"


def fetch(url, path):
    """Ask for the file once. If it is already in data/, do nothing."""
    if path.exists():
        print(f"data/{path.name} is already here ({path.stat().st_size // 1024} KB). "
              "Delete it to fetch again.")
        return path
    DATA.mkdir(exist_ok=True)
    print(f"asking {url}")
    reply = requests.get(url, timeout=60, headers={"User-Agent": "SD5913 PolyU student"})
    reply.raise_for_status()
    path.write_bytes(reply.content)      # the raw reply, byte for byte: what arrived is what gets committed
    print(f"saved data/{path.name} ({path.stat().st_size // 1024} KB). Now: git add data")
    return path


if __name__ == "__main__":
    fetch(URL, DATA / FILE)
