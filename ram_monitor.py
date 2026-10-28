#!/usr/bin/env python3
"""Real-time RAM monitoring tool."""

import argparse
import sys
import time

try:
    import psutil
except ImportError:
    sys.exit("psutil o'rnatilmagan. Install: pip install psutil")


def fmt(bytes_num):
    for unit in ("B", "KB", "MB", "GB"):
        if bytes_num < 1024:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024
    return f"{bytes_num:.1f} TB"


def bar(percent, width=30):
    filled = int(width * percent / 100)
    color = "\033[92m" if percent < 70 else ("\033[93m" if percent < 90 else "\033[91m")
    return f"{color}[{'█' * filled}{'░' * (width - filled)}]\033[0m {percent:.1f}%"


def snapshot():
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    print("\033[2J\033[H", end="")  # ekranni tozalash
    print("=== RAM MONITOR ===\n")
    print(f"Jami:      {fmt(mem.total)}")
    print(f"Ishlatilgan: {fmt(mem.used)}")
    print(f"Bo'sh:     {fmt(mem.available)}")
    print(f"RAM:   {bar(mem.percent)}")
    print(f"Swap:  {bar(swap.percent)}")
    print(f"\nYangilandi: {time.strftime('%H:%M:%S')}")
    print("Chiqish uchun: Ctrl+C")


def main():
    p = argparse.ArgumentParser(description="RAM monitor")
    p.add_argument("-i", "--interval", type=float, default=1.0,
                   help="Yangilash oralig'i soniyada (default: 1)")
    p.add_argument("-o", "--once", action="store_true",
                   help="Bir marta ko'rsatib chiqish")
    args = p.parse_args()

    try:
        while True:
            snapshot()
            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nChiqildi.")


if __name__ == "__main__":
    main()
