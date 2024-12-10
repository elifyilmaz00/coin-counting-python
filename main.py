import cv2
import numpy as np
import matplotlib.pyplot as plt

# fotoyu okuma
image_path = "C:\\Users\\elifs\\Desktop\\para.jpg"
image = cv2.imread(image_path)

# Görüntüyü gri tonlamaya çevirme
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# İkili (Binary) görüntüye dönüştürme
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
binary = cv2.bitwise_not(binary)  # Siyah-beyaz alanları ters çevir

# Morfolojik işlemler
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(binary, kernel, iterations=2)  # Bitişik nesneleri birbirinden ayırmak için

# Erozyon işlemi
eroded = cv2.erode(dilated, kernel, iterations=1)

# Kontur tespiti
contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sonuçları işleme ve paraların türlerini belirleme
total_amount = 0
for contour in contours:
    if cv2.contourArea(contour) > 100:  # Küçük nesneleri ihmal et
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Yeşil dikdörtgen çiz

        # Dikdörtgenin uzunluğunu
        length = x + w - x

        # Uzunluk büyüklüklerine göre sınıflandırma
        cx, cy = x + w // 2, y + h // 2  # Konturun merkezini hesapla

        if length > 222:  # 1 TL için uzunluk
            total_amount += 1  # 1 TL
            plt.text(cx, cy, '1 TL', color='yellow', fontsize=8)
        elif 190 < length <= 221:  # 50 Kr için uzunluk
            total_amount += 0.5  # 50 Kr
            plt.text(cx, cy, '50 Kr', color='yellow', fontsize=8)
        elif 175 < length <= 190:  # 25 Kr için uzunluk
            total_amount += 0.25  # 25 Kr
            plt.text(cx, cy, '25 Kr', color='yellow', fontsize=8)
        elif 164 < length <= 175:  # 10 Kr için uzunluk
            total_amount += 0.1  # 10 Kr
            plt.text(cx, cy, '10 Kr', color='yellow', fontsize=8)
        else:  # 5 Kr için uzunluk
            total_amount += 0.05  # 5 Kr
            plt.text(cx, cy, '5 Kr', color='yellow', fontsize=8)

# Toplam miktarı yazdırma
plt.title(f'Toplam para miktarı: {total_amount:.2f} TL')

# Sonuçları görselleştirme
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
