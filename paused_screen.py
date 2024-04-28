import pygame
from button import Button
from settings import Settings

set=Settings()

class Pause():
    def __init__(self) -> None:
        pass

    #drawing the paused screen
    def pause_game(self,win):
        
        bg_img=pygame.transform.scale(pygame.image.load('images/mc.jpg'),(set.win_width,set.win_height))
        win.blit(bg_img,(0,0))

        #drawing resume button
        play_but_img=pygame.transform.scale(pygame.image.load('images/resume.png'),(200,90))
        play_but=Button(440,200,play_but_img)
        play_but.draw(win)

        #drawing main menu button
        menu_but_img=pygame.transform.scale(pygame.image.load('images/menu.png'),(200,90))
        menu_but=Button(440,310,menu_but_img)
        menu_but.draw(win)

        #drawing restart button
        restart_but_img=pygame.transform.scale(pygame.image.load('images/reset.png'),(200,90))
        restart_but=Button(440,420,restart_but_img)
        restart_but.draw(win)
        
        self.playing=play_but.action
        self.op_menu=menu_but.action
        self.rest=restart_but.action
