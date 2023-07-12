from simulator import *

import pygame, sys, json
from pygame import gfxdraw
import win32api

pygame.init()
settings :dict= json.load(open(".\\data\\settings.json", "r", encoding='utf8'))
ValueLinks = settings.get("ValueLinks", [])

def texload(path:str) -> pygame.surface.Surface:
    return pygame.image.load(path).convert_alpha()

# ===================== Pygame =====================
window = pygame.display.set_mode((1440,810))
pygame.display.set_caption("Auto Drive", "Auto Drive Simulator")
clock = pygame.time.Clock()
icon = texload(".\\data\\car.png").convert_alpha()
pygame.display.set_icon(icon)
world = pygame.surface.Surface((1086, 768), pygame.SRCALPHA)
world_tex = texload(".\\data\\world.png").convert_alpha()

offsetx, offsety = 38, 21
# ==================================================


# ==================== functions ===================
def calculate():
    s = 100-PositionSlider.actual
    v0 = Velocity0Slider.actual
    v = VelocitySlider.actual

    t = CalcTime(v, v0 , s)
    ac = CalcAcceleration(v, v0, s)

    TimeValueViewer.value = t
    AccelerationValueViewer.value = ac

def play():
    stop()
    System.timer = time.time()
    Car.moving = True
    Car.speed = Velocity0Slider.actual

def stop():
    Car.moving = False
    Car.velocity = 0.
    Car.speed = 0.
    System.pos = 800
    Car.pos[0] = int(800 - 514*PositionSlider.percentage)
# ==================================================

class System:
    timer = time.time()
    speed = 0
    pos = 800

    def event():
        calculate()
        system.CursorChanged = False

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()
    
    def display():
        fps = clock.get_fps()
        window.fill((28, 33, 38))
        window.blit(world_tex, (offsetx, offsety))
        pygame.draw.line(window, (132, 140, 144, 50), (286+318, offsety), (286+318, 768+offsety), 1)
        pygame.draw.line(window, (87, 169, 65, 50), (Car.pos[0] + 318, offsety), (Car.pos[0] + 318, 768+offsety), 1)
        Car.draw(window, fps)

        for link in ValueLinks: # value links
            try: exec(link)
            except Exception as e: print(e)

        # ==================================================
        for object in system.objects: object.draw(
                mpos=pygame.mouse.get_pos()
        )

        # pygame.draw.line(window, (0, 255, 0), (286+318, 0), (286+318, 810), 1)
        # pygame.draw.line(window, (255, 0, 0), (0, Car.pos[1] + offsety), (1440, Car.pos[1] + offsety), 1)
        # pygame.draw.circle(window, (255, 0, 0), (Car.pos[0] + 318, Car.pos[1] + offsety), 5)
        # system.draw.text(str(Car.pos), font("NanumSquareNeo-cBd", 10), window, Car.pos[0] + 318+5, Car.pos[1] + offsety+5, "left", (255, 0, 0))
        system.draw.text(str(round(clock.get_fps(), 1))+ " fps", font("NanumSquareNeo-cBd", 10), window, 5, 5, "left", (255, 255, 255))
        system.draw.text(str(round(Car.velocity, 2)) + " m/s", font("NanumSquareNeo-cBd", 16), window, Car.pos[0]+318+ 10, Car.pos[1]+offsety-150, "cenleft", (0, 0, 0))
        
        # ==================================================

        if (not system.CursorChanged): pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if (Velocity0Slider.moving): stop()
        if (VelocitySlider.moving): stop()

Car = car([800, 600], (318, offsety))
PositionSlider = system.ui.slider(window, (28 + offsetx, 80 + offsety), (230, 2), "Position", unit="m", ValueMultiplier=100)
Velocity0Slider = system.ui.slider(window, (28 + offsetx, 80 + 80*1 + offsety), (230, 2), "Velocity0", unit="m/s", ValueMultiplier=50, percentage=1.)
VelocitySlider = system.ui.slider(window, (28 + offsetx, 80 + 80*2 + offsety), (230, 2), "Velocity", unit="m/s", ValueMultiplier=50, percentage=.2)
TimeValueViewer = system.ui.value_viewer(window, (28 + offsetx, 80 + 80*3 + 63*0 + offsety), "Calculated Time", unit="s")
AccelerationValueViewer = system.ui.value_viewer(window, (28 + offsetx, 80 + 80*3 + 63*1 + offsety), "Calculated Acceleration", unit="m/s²")
PositionValueViewer = system.ui.value_viewer(window, (28 + offsetx, 80 + 80*3 + 63*2 + offsety), "Current Position", unit="m")
VelocityValueViewer = system.ui.value_viewer(window, (28 + offsetx, 80 + 80*3 + 63*3 + offsety), "Current Velocity", unit="m/s")

button1 = system.ui.button(window, (84 + 60*0 + offsetx, 738+offsety), (50, 20), (248, 250, 254), .9,
                           text="Play", function=play) 
button2 = system.ui.button(window, (84 + 60*1 + offsetx, 738+offsety), (50, 20), (248, 250, 254), .9,
                           text="Stop", function=stop)


while __name__ == "__main__":
    System.event()
    System.display()
    pygame.display.flip()
    clock.tick(settings.get("fps", 240))