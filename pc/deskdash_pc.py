# DeskDash — ПК-часть. Первый маленький шаг.
# Здесь мы собираем показатели компьютера, которые потом отправим на экран ESP32.

import psutil  # библиотека, которая отдаёт данные о состоянии ПК

cpu = psutil.cpu_percent(interval=1)   # загрузка процессора, в процентах
ram = psutil.virtual_memory().percent  # сколько занято оперативной памяти, в процентах

print(f"CPU: {cpu}%")
print(f"RAM: {ram}%")
print(f"Всего памяти: {psutil.virtual_memory().total // (1024**3)} ГБ")