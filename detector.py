import cv2
import time
import random
import numpy as np
import math

# Настройки стиля
COLOR_SCAN = (0, 255, 0)      # Зеленый
COLOR_TEXT = (255, 255, 255)  # Белый
COLOR_ALERT = (0, 0, 255)     # Красный
COLOR_GLITCH = (255, 0, 255)  # Пурпурный

cap = cv2.VideoCapture(0)
# Оптимальное разрешение для скорости
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

scan_line_y = 0
status = "SCANNING" 
data_flow = [] 
glitch_timer = 0

print("--- TRUEFACE: FINAL SYSTEM READY ---")

while True:
    ret, frame = cap.read()
    if not ret: break
    
    h, w, _ = frame.shape
    frame = cv2.addWeighted(frame, 0.4, np.zeros(frame.shape, frame.dtype), 0, 0)
    
    # ЭФФЕКТ ГЛИТЧА
    glitch_timer += 1
    if random.random() < 0.05 and glitch_timer > 30:
        frame[random.randint(0,h-20):random.randint(0,h), :, 0] = random.randint(0,255)
        glitch_timer = 0

    # Центральная зона
    rw, rh = int(w * 0.4), int(h * 0.6)
    rx, ry = (w - rw) // 2, (h - rh) // 2
    
    pulse = (math.sin(time.time() * 4) + 1) / 2
    overlay = frame.copy()
    cv2.rectangle(overlay, (rx, ry), (rx + rw, ry + rh), (0, 50, 0), -1)
    frame = cv2.addWeighted(overlay, 0.1 * pulse, frame, 0.9, 0)
    
    # Жирные углы
    l, t = 60, 4
    cv2.line(frame, (rx, ry), (rx + l, ry), COLOR_SCAN, t) # ЛВ
    cv2.line(frame, (rx, ry), (rx, ry + l), COLOR_SCAN, t)
    cv2.line(frame, (rx + rw, ry), (rx + rw - l, ry), COLOR_SCAN, t) # ПВ
    cv2.line(frame, (rx + rw, ry), (rx + rw, ry + l), COLOR_SCAN, t)
    cv2.line(frame, (rx, ry + rh), (rx + l, ry + rh), COLOR_SCAN, t) # ЛН
    cv2.line(frame, (rx, ry + rh), (rx, ry + rh - l), COLOR_SCAN, t)
    cv2.line(frame, (rx + rw, ry + rh), (rx + rw - l, ry + rh), COLOR_SCAN, t) # ПН
    cv2.line(frame, (rx + rw, ry + rh), (rx + rw, ry + rh - l), COLOR_SCAN, t)

    # Потоки данных справа
    if random.random() < 0.2:
        hex_data = "".join(random.choice("0123456789ABCDEF") for _ in range(16))
        data_flow.append({"text": f"0x{hex_data}", "y": h - 20, "speed": random.randint(5, 15)})
    
    for data in data_flow[:]:
        cv2.putText(frame, data["text"], (w - 180, data["y"]), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 200, 0), 1)
        data["y"] -= data["speed"]
        if data["y"] < 50: data_flow.remove(data)

    # --- ЛОГИКА ВЕРДИКТА ---
    if status == "VERIFIED":
        display_color = COLOR_SCAN
        # Огромная надпись в центре
        cv2.putText(frame, "VERIFIED: TRUE", (rx + 15, ry + rh // 2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, COLOR_SCAN, 4)
        msg = "IDENTITY CONFIRMED // DATABASE MATCH: 100% // ACCESS GRANTED"
    elif status == "ERROR":
        display_color = COLOR_ALERT
        cv2.putText(frame, "VERIFIED: FALSE", (rx + 15, ry + rh // 2), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, COLOR_ALERT, 4)
        msg = "SYSTEM ERROR // UNKNOWN BIOMETRIC // THREAT DETECTED"
    else:
        display_color = (0, 165, 255)
        msg = f"SCANNING... [THREAD_ID: {random.randint(1000, 9999)}]"

    # Нижняя панель
    cv2.rectangle(frame, (0, h - 60), (w, h), (0, 0, 0), -1)
    cv2.line(frame, (0, h - 60), (w, h - 60), display_color, 2)
    cv2.putText(frame, msg, (20, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, display_color, 2)
    cv2.putText(frame, "TRUEFACE v3.0", (20, h - 80), cv2.FONT_HERSHEY_SIMPLEX, 1.2, COLOR_TEXT, 3)

    # УПРАВЛЕНИЕ
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
    elif key == ord('a'): status = "VERIFIED" # Нажми 'A' для правды
    elif key == ord('e'): status = "ERROR"    # Нажми 'E' для ошибки
    elif key == ord('r'): status = "SCANNING" # Нажми 'R' для сброса

    cv2.imshow('TRUEFACE SYSTEM', frame)

cap.release()
cv2.destroyAllWindows()