import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def pacsound():
    acound = os.path.join('src','dyno','assets','acsound.wav')
    pygame.mixer.init()
    pygame.mixer.music.load(acound)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
