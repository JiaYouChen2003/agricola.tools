import pyautogui
from PIL import ImageGrab
import numpy as np
import cv2
from classify import imgclassify
import keyboard

press = 0
def shot():
    pos_x = pyautogui.position().x
    pos_y = pyautogui.position().y
    img = ImageGrab.grab(bbox=(pos_x - 45, pos_y - 25, pos_x + 45, pos_y + 25))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    imgclassify(img)

while True:
    if keyboard.is_pressed("q"):
        shot()