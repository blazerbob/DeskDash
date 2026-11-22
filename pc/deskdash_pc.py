"""DeskDash: простая консольная инфопанель компьютера."""

from __future__ import annotations

import os
import time
from typing import TypedDict

import psutil


# Эти настройки удобно менять в одном месте.
UPDATE_SECONDS = 1.0
BAR_LENGTH = 20


class ComputerStats(TypedDict):
    """Форма данных, которые мы показываем в панели."""

    cpu_percent: float
    ram_percent: float
    ram_total_gb: float
    disk_percent: float


def clamp_percent(value: float) -> float:
    """Ограничивает процент диапазоном от 0 до 100."""
    return max(0.0, min(value, 100.0))


def make_bar(percent: float) -> str:
    """Превращает процент в текстовую полоску, например [########------------]."""
    safe_percent = clamp_percent(percent)
    filled = round(safe_percent / 100 * BAR_LENGTH)
    empty = BAR_LENGTH - filled
    return "#" * filled + "-" * empty


def collect_stats() -> ComputerStats:
    """Считывает текущие показатели компьютера."""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage(os.path.abspath(os.sep))

    return {
        "cpu_percent": psutil.cpu_percent(interval=UPDATE_SECONDS),
        "ram_percent": memory.percent,
        "ram_total_gb": memory.total / 1024**3,
        "disk_percent": disk.percent,
    }


def clear_console() -> None:
    """Очищает консоль перед рисованием следующего кадра панели."""
    os.system("cls" if os.name == "nt" else "clear")


def show_panel(stats: ComputerStats) -> None:
    """Показывает один кадр инфопанели."""
    clear_console()

    cpu = stats["cpu_percent"]
    ram = stats["ram_percent"]
    disk = stats["disk_percent"]
    total_ram = stats["ram_total_gb"]

    print("DeskDash — информационная панель ПК")
    print("=" * 42)
    print(f"CPU       [{make_bar(cpu)}] {cpu:5.1f}%")
    print(f"RAM       [{make_bar(ram)}] {ram:5.1f}%")
    print(f"Диск      [{make_bar(disk)}] {disk:5.1f}%")
    print(f"Всего RAM: {total_ram:.1f} ГБ")
    print("\nДля остановки нажми Ctrl+C.")


def main() -> None:
    """Запускает постоянное обновление инфопанели."""
    try:
        while True:
            stats = collect_stats()
            show_panel(stats)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nDeskDash остановлен.")


if __name__ == "__main__":
    main()
