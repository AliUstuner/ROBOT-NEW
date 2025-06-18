import pygame
import serial
import time

# Arduino seri bağlantı portu (gerekiyorsa /dev/ttyUSB0 olarak değiştir)
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)  # Arduino'nun açılmasını bekle

# Pygame başlat
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Gamepad kontrolü başladı. Çıkmak için CTRL+C.")

def send(cmd, speed=255):
    message = f"{cmd}:{speed}\n"
    arduino.write(message.encode())

while True:
    pygame.event.pump()  # Girdi güncelle
    x = joystick.get_axis(0)  # Sol/sağ
    y = joystick.get_axis(1)  # İleri/geri
    btn_stop = joystick.get_button(1)  # B tuşu

    if btn_stop:
        send('S', 0)
    elif y < -0.5:
        send('F', int(abs(y) * 255))
    elif y > 0.5:
        send('B', int(abs(y) * 255))
    elif x < -0.5:
        send('L', int(abs(x) * 255))
    elif x > 0.5:
        send('R', int(abs(x) * 255))
    else:
        send('S', 0)

    time.sleep(0.1)
