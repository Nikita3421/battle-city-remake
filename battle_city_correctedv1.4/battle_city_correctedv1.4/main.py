import pygame
import sys
#import sound
from sprite import Player,Button
from abc import abstractmethod,ABC
from screens import ScreenManager

pygame.init()
bullet_img = 'images/bullet.png'
player_img = 'images/tank.png'
  
WIDTH, HEIGHT = 800, 600       
        


class App():
    def __init__(self,win_width=WIDTH,win_height = HEIGHT,FPS=45,name='City Battle'):
        self.window = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.sm = ScreenManager()

    
    def update(self,events):
        self.window.fill((0,29,10))
        self.sm.update(self.window,events)
    
    def run(self):
        while True:
            
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    sys.exit()
            self.update(events)  
                  
            pygame.display.update()
            self.clock.tick(self.FPS)


def main():
    app = App()
    app.run()

main()