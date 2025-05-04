import sys, time
import pygame
from pygame.locals import *
from pygamevideo import Video
import string
import random
import threading
import socket
import os
import json

from utility import *
from mechanic import *
from connection import *
from LAN import *

#Screen Settings
FPS = 60
ASSET = fr'assets/'
PACKAGE = fr'package/'
PACKAGE_DATA = fr'package/data/'

#Icon
icon = pygame.image.load(f'{ASSET}/icon.png')
pygame.display.set_icon(icon)

#Caption
pygame.display.set_caption('Knuckle Bones Remastered')

#Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
ALPHA = (0, 255, 0)
GRAY = (204,204,204)

#Misc
SERVER = False
LAN = True
PRIVATE = False
PUBLIC = True
CODE = 1
IP = 2
PORT = 3
DEFAULT_PORT = 1024

def adjust_surface(surface,ratio):
    surface_size = surface.get_size()
    surface = pygame.transform.scale(surface,(surface_size[0]*ratio[0],surface_size[1]*ratio[1]))
    return surface

def adjust_pos(pos,ratio):
    return [pos[0]*ratio[0],pos[1]*ratio[1]]

def adjust_size(size,ratio):
    return [size[0]*ratio[0],size[1]*ratio[1]]

def adjust_rect(rect,ratio):
    pos = adjust_pos([rect[0],rect[1]],ratio)
    size = adjust_size([rect[2],rect[3]],ratio)
    return pygame.Rect([pos[0],pos[1],size[0],size[1]])

def load_settings():
    pass

def save_settings():
    pass

#main game functions
def main():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()
    
    ScreenWidth = 1920
    ScreenHeight = 1080
    screen = pygame.display.set_mode((1320,720),RESIZABLE)
    main_clock = pygame.time.Clock()
    
    class App:
        def __init__(self):
            pygame.init()
            
            self.volume = 1.0
            self.assets = {
                "menu_background": load_image(f"{ASSET}menu_background.png"),
                "menu_button_overlay": load_image(f"{ASSET}menu_button_overlay.png"),
                "menu_button": load_image(f"{ASSET}menu_button.png"),
                "match_setting_background": load_image(f"{ASSET}match_setting_background.png"),
                "online_menu_background": load_image(f"{ASSET}online_menu_background.png"),
                "result_background": load_image(f"{ASSET}result_background.png"),
                "result_quit": load_image(f"{ASSET}result_quit.png"),
                "result_rematch": load_image(f"{ASSET}result_rematch.png"),
                "option_menu_background": load_image(f"{ASSET}option_menu_background.png"),
                "option_resume": load_image(f"{ASSET}option_resume.png"),
                "option_settings": load_image(f"{ASSET}option_settings.png"),
                "option_support": load_image(f"{ASSET}option_support.png"),
                "option_surrender": load_image(f"{ASSET}option_surrender.png"),
                "cancel_waiting": load_image(f"{ASSET}cancel_waiting.png"),
                "match_bar": load_image(f"{ASSET}match_bar.png"),
                "join_mode_0": load_image(f"{ASSET}join_mode_0.png"),
                "join_mode_1": load_image(f"{ASSET}join_mode_1.png"),
                "join_type_0": load_image(f"{ASSET}join_type_0.png"),
                "join_type_1": load_image(f"{ASSET}join_type_1.png"),
                "quit": load_image(f"{ASSET}quit.png"),
                "increase": load_image(f"{ASSET}increase.png"),
                "decrease": load_image(f"{ASSET}decrease.png"),
                "create": load_image(f"{ASSET}create.png"),
                "join": load_image(f"{ASSET}join.png"),
                "save": load_image(f"{ASSET}save.png"),
                "cancel": load_image(f"{ASSET}cancel.png"),
                "reset": load_image(f"{ASSET}reset.png"),
                "volume_line": load_image(f"{ASSET}volume_line.png"),
                "volume_button": load_image(f"{ASSET}volume_button.png"),
                "match_code_input": load_image(f"{ASSET}match_code_input.png"),
                "overlay_shader": load_image(f"{ASSET}overlay_shader.png"),
                "pressed_shader": load_image(f"{ASSET}pressed_shader.png"),
                "dice 1": adjust_surface(load_image(f"{ASSET}one.png"),[3,3]),
                "dice 2": adjust_surface(load_image(f"{ASSET}two.png"),[3,3]),
                "dice 3": adjust_surface(load_image(f"{ASSET}three.png"),[3,3]),
                "dice 4": adjust_surface(load_image(f"{ASSET}four.png"),[3,3]),
                "dice 5": adjust_surface(load_image(f"{ASSET}five.png"),[3,3]),
                "dice 6": adjust_surface(load_image(f"{ASSET}six.png"),[3,3]),
                "dice_box": load_image(f"{ASSET}dice_box.png"),
                "score_box": load_image(f"{ASSET}score_box.png"),
                "table": load_image(f"{ASSET}table.png"),
                "box": load_image(f"{ASSET}box.png"),
                "Create": load_image(f"{ASSET}Create_Match.png"),
                "Join": load_image(f"{ASSET}Join_Match.png"),
                "Filter": load_image(f"{ASSET}Filter.png"),
                "Refresh": load_image(f"{ASSET}Refresh.png"),
                "Quick Match": load_image(f"{ASSET}Quick_Match.png"),
                "Page Up": load_image(f"{ASSET}Page Up.png"),
                "Page Down": load_image(f"{ASSET}Page Down.png")
            }
            self.assets["overlay_shader"].set_alpha(100)
            self.assets["pressed_shader"].set_alpha(80)
            self.grid = 3
            self.screen_size = screen.get_size()
            self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
            
        def settings(self):
            buttons = {
                "quit": [20,18,37,37],
                "save": [1085,980,230,65],
                "cancel": [1353,980,230,65],
                "reset": [1621,980,230,65]
            }
            volume_button = [690,135,20,60]
            setting_font = pygame.font.SysFont("Consolas",73,True)
            typing = False
            line_animationframe = 0
            #################################
            volume_pressed = False
            change = None
            with open("settings.json","r") as file:
                data = json.load(file)
            #################################
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                for button in buttons:
                    if button == "save" or button == "cancel":
                        if not change:
                            continue
                    button_rect = adjust_rect(buttons[button],screen_ratio)
                    screen.blit(adjust_surface(self.assets[button],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                screen.blit(adjust_surface(setting_font.render("Volume:",True,GRAY),screen_ratio),adjust_pos([219,123],screen_ratio))
                screen.blit(adjust_surface(self.assets["volume_line"],screen_ratio),adjust_pos([690,161],screen_ratio))
                screen.blit(adjust_surface(setting_font.render("Resolution:",True,GRAY),screen_ratio),adjust_pos([219,277],screen_ratio))
                #################################
                if volume_pressed:
                    min_pos = 690 * screen_ratio[0]
                    max_pos = 1407 * screen_ratio[0]
                    button_pos = max(min(max_pos,mouse_pos[0]-20*screen_ratio[0]/2),min_pos)
                    self.volume = (button_pos-min_pos)/(max_pos-min_pos)
                    if self.volume != data["volume"]:
                        change = True
                screen.blit(adjust_surface(self.assets["volume_button"],screen_ratio),adjust_pos([690+self.volume*717,135],screen_ratio))#690 1407
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*buttons]:
                                rect = adjust_rect(buttons[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        return 0
                                    elif button == "save":
                                        if change:
                                            data["volume"] = self.volume
                                            data["resolution"] = self.screen_size
                                            with open("settings.json","w") as file:
                                                file.write(json.dumps(data))
                                            change = None
                                    elif button == "cancel":
                                        self.volume = data["volume"]
                                        self.screen_size = data["resolution"]
                                        change = None
                                    elif button == "reset":
                                        self.volume = 1.0
                                        self.screen_size = [1920,1080]
                                        data["volume"] = self.volume
                                        data["resolution"] = self.screen_size
                                        with open("settings.json","w") as file:
                                            file.write(json.dumps(data))
                                        change = None
                            rect = adjust_rect([690+self.volume*717,135,20,60],screen_ratio)
                            if rect.collidepoint(mouse_pos):
                                volume_pressed = True
                            typing = False
                            rect = adjust_rect([810,700,592,66],screen_ratio)
                            if rect.collidepoint(mouse_pos):
                                typing = True

                    if event.type == MOUSEBUTTONUP:
                        volume_pressed = False
                                    
                    if event.type == MOUSEWHEEL:
                        rect = adjust_rect([860,272,233,39],screen_ratio)
                        if rect.collidepoint(mouse_pos):
                            grid = min(max(grid+event.y,3),5)
                                    
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return 0
                        if typing:
                            if event.key == pygame.K_BACKSPACE:
                                line_animationframe = 0
                                code = code[:-1]
                            elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                                code = pygame.scrap.get_text()
                            else:
                                if event.unicode in string.ascii_letters or event.unicode in ["0","1","2","3","4","5","6","7","8","9"]:
                                    line_animationframe = 0
                                    code += event.unicode
                            
                pygame.display.flip()
        
        def menu(self):
            menu_button = {
                "Local Match": [39,51,751,174],
                "Online Match": [58,262,751,174],
                "Settings": [78,474,751,174],
                "Exit": [98,685,751,174],
            }
            button_font = pygame.font.SysFont("Consolas",80)
            #################################
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                for button in [*menu_button]:
                    button_rect = adjust_rect(menu_button[button],screen_ratio)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(adjust_surface(self.assets[f"menu_button_overlay"],screen_ratio),button_rect.topleft)
                    else:
                        screen.blit(adjust_surface(self.assets[f"menu_button"],screen_ratio),button_rect.topleft)
                    screen.blit(adjust_surface(button_font.render(button,True,BLACK),screen_ratio),(button_rect.topleft[0]+42*screen_ratio[0],button_rect.topleft[1]+51*screen_ratio[1]))
                #################################
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*menu_button]:
                                rect = adjust_rect(menu_button[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "Local Match":
                                        rematching = self.local_match()
                                        while rematching:
                                            rematching = self.local_match()
                                    elif button == "Online Match":
                                        self.online_match_menu()
                                    elif button == "Settings":
                                        self.settings()
                                    elif button == "Exit":
                                        pygame.quit()
                                        sys.exit()
                            
                pygame.display.flip()
                
        def local_match_settings(self):
            setting_button = {
                "quit": [20,18,37,37],
                "increase": [1078,272,15,15],
                "decrease": [1078,296,15,15],
                "create": [726,837,468,87]
            }
            setting_font = pygame.font.SysFont("Consolas",48,True)
            typing = False
            #################################
            grid = 3
            code = ""
            #################################
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"match_setting_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                screen.blit(adjust_surface(setting_font.render("Grid:",True,GRAY),screen_ratio),adjust_pos((850,272),screen_ratio))
                screen.blit(adjust_surface(setting_font.render(f"{grid}x{grid}",True,GRAY),screen_ratio),adjust_pos((984,272),screen_ratio))
                for button in setting_button:
                    button_rect = adjust_rect(setting_button[button],screen_ratio)
                    screen.blit(adjust_surface(self.assets[button],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                #################################
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*setting_button]:
                                rect = adjust_rect(setting_button[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        return 0
                                    elif button == "increase":
                                        if grid < 5:
                                            grid += 1
                                    elif button == "decrease":
                                        if grid > 3:
                                            grid -= 1
                                    elif button == "create":
                                        match_property = {
                                            "Player 1 Board": [[0 for j in range(0,grid)] for i in range(0,grid)],
                                            "Player 2 Board": [[0 for j in range(0,grid)] for i in range(0,grid)],
                                            "Player 1 Score": 0,
                                            "Player 2 Score": 0,
                                            "Round": 0
                                        }
                                        self.grid = grid
                                        return match_property
                                    
                    if event.type == MOUSEWHEEL:
                        rect = adjust_rect([860,272,233,39],screen_ratio)
                        if rect.collidepoint(mouse_pos):
                            grid = min(max(grid+event.y,3),5)
                                    
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return 0
                        if typing:
                            if event.key == pygame.K_BACKSPACE:
                                code = code[:-1]
                            elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                                code = pygame.scrap.get_text()
                            else:
                                if event.unicode in string.ascii_letters or event.unicode in ["0","1","2","3","4","5","6","7","8","9"]:
                                    code += event.unicode
                            
                pygame.display.flip()
                
        def online_match_settings(self):
            setting_button = {
                "quit": [20,18,37,37],
                "increase": [1078,347,15,15],
                "decrease": [1078,371,15,15],
                "create": [726,837,468,87],
                "join_mode": [703,723,237,52],
                "join_type": [980,723,237,52]
            }
            input_bar = {
                "name": [748,249,592,66],
                "identifier": [748,625,592,66]
            }
            error_font = pygame.font.SysFont("Consolas",28,True)
            setting_font = pygame.font.SysFont("Consolas",48,True)
            typing = False
            line_animationframe = 0
            #################################
            grid = 3
            create_setting = {
                "name": "",
                "identifier": ""
            }
            mode = SERVER
            type = PUBLIC
            error = ""
            error_frame = 0
            #################################
            press_key_frame = 0
            type_pos = 0
            select_pos = None
            text_backup = [""]
            backup_pos = -1
            #################################
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"match_setting_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                screen.blit(adjust_surface(setting_font.render("Name:",True,GRAY),screen_ratio),adjust_pos((580,254),screen_ratio))
                screen.blit(adjust_surface(self.assets["match_code_input"],screen_ratio),adjust_pos((748,249),screen_ratio))
                screen.blit(adjust_surface(setting_font.render("Grid:",True,GRAY),screen_ratio),adjust_pos((840,342),screen_ratio))
                screen.blit(adjust_surface(setting_font.render(f"{grid}x{grid}",True,GRAY),screen_ratio),adjust_pos((984,343),screen_ratio))
                for button in setting_button:
                    button_rect = adjust_rect(setting_button[button],screen_ratio)
                    if button == "join_mode":
                        screen.blit(adjust_surface(self.assets[f"{button}_{int(mode)}"],screen_ratio),adjust_pos((703,723),screen_ratio))
                    elif button == "join_type":
                        screen.blit(adjust_surface(self.assets[f"{button}_{int(type)}"],screen_ratio),adjust_pos((980,723),screen_ratio))
                    else:
                        screen.blit(adjust_surface(self.assets[button],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                if mode:
                    screen.blit(adjust_surface(setting_font.render("Port:",True,GRAY),screen_ratio),adjust_pos((604,630),screen_ratio))
                else:
                    screen.blit(adjust_surface(setting_font.render("Code:",True,GRAY),screen_ratio),adjust_pos((604,630),screen_ratio))
                screen.blit(adjust_surface(self.assets["match_code_input"],screen_ratio),adjust_pos((748,625),screen_ratio))
                if len(create_setting["name"]) > 22:
                    screen.blit(adjust_surface(setting_font.render(create_setting["name"][-22:],True,GRAY),screen_ratio),adjust_pos((748,259),screen_ratio))
                else:
                    screen.blit(adjust_surface(setting_font.render(create_setting["name"],True,GRAY),screen_ratio),adjust_pos((748,259),screen_ratio))
                if len(create_setting["identifier"]) > 22:
                    screen.blit(adjust_surface(setting_font.render(create_setting["identifier"][-22:],True,GRAY),screen_ratio),adjust_pos((748,635),screen_ratio))
                else:
                    screen.blit(adjust_surface(setting_font.render(create_setting["identifier"],True,GRAY),screen_ratio),adjust_pos((748,635),screen_ratio))
                if typing:
                    if line_animationframe <= 22:
                        if len(create_setting[typing]) > 22:
                            text_end = setting_font.render(create_setting[typing][-22:],True,WHITE).get_size()[0]
                        else:
                            text_end = setting_font.render(create_setting[typing],True,WHITE).get_size()[0]
                        pygame.draw.rect(screen,WHITE,adjust_rect((748+text_end,input_bar[typing][1]+3,2,65),screen_ratio))
                    elif line_animationframe > 60:
                        line_animationframe = 0
                    line_animationframe += 1
                if error != "":
                    error_frame += 1
                    error_text = error_font.render(error,True,(245,214,53))
                    screen.blit(adjust_surface(error_text,screen_ratio),adjust_pos([(1920-error_text.get_size()[0])/2,794],screen_ratio))
                    if error_frame == 180:
                        error_frame = 0
                        error = ""
                #################################
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*setting_button]:
                                rect = adjust_rect(setting_button[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        return 0
                                    elif button == "increase":
                                        if grid < 5:
                                            grid += 1
                                    elif button == "decrease":
                                        if grid > 3:
                                            grid -= 1
                                    elif button == "join_mode":
                                        mode = not mode
                                        if mode:
                                            type = PRIVATE
                                    elif button == "join_type":
                                        if not mode:
                                            type = not type
                                    elif button == "create":
                                        match_property = {
                                            "Grid": grid,
                                            "Match Name": create_setting["name"],
                                            "Identifier": create_setting["identifier"],
                                            "Mode": mode,
                                            "Type": type
                                        }
                                        if match_property["Mode"]:
                                            if int(match_property["Identifier"]) < 0 or int(match_property["Identifier"]) > 65535:
                                                error = "Illegal port number"
                                            else:
                                                host = socket.gethostbyname(socket.gethostname())
                                                threading.Thread(target=start_LAN_sever,args=(host,int(match_property["Identifier"]),match_property["Grid"],match_property["Match Name"])).start()
                                                rematching = self.lan_match(host,int(match_property["Identifier"]))
                                                while rematching:
                                                    rematching = self.lan_match(host,int(match_property["Identifier"]))
                                        else:
                                            match_id = create_match(match_property["Grid"],match_property["Match Name"],match_property["Identifier"],match_property["Type"])
                                            if match_id:
                                                rematching = self.online_match(match_id)
                                                while rematching:
                                                    rematching = self.online_match(match_id)
                                            else:
                                                error = "Match already exists"
                            typing = False
                            select_pos = None
                            for bar in [*input_bar]:
                                rect = adjust_rect(input_bar[bar],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    typing = bar
                                    text_size = setting_font.render(create_setting[typing][-22:],True,GRAY).get_size()
                                    text_rect = adjust_rect([input_bar[bar][0],input_bar[bar][1],text_size[0],input_bar[bar][3]])
                                    if text_rect.collidepoint(mouse_pos):
                                        pass
                                    else:
                                        type_pos = len(create_setting[typing])
                                    
                    if event.type == MOUSEWHEEL:
                        rect = adjust_rect([860,272,233,39],screen_ratio)
                        if rect.collidepoint(mouse_pos):
                            grid = min(max(grid+event.y,3),5)
                                    
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return 0
                        if typing:
                            if event.key == pygame.K_BACKSPACE:
                                if select_pos:
                                    create_setting[typing] = create_setting[typing][0:select_pos[0]] + create_setting[typing][select_pos[1]:]
                                    type_pos = select_pos[0]
                                    select_pos = None
                                else:
                                    if type_pos > 0:
                                        line_animationframe = 0
                                        create_setting[typing] = create_setting[typing][0:type_pos-1] + create_setting[typing][type_pos:]
                                        type_pos -= 1
                            elif event.key == pygame.K_DELETE:
                                if select_pos:
                                    create_setting[typing] = create_setting[typing][0:select_pos[0]] + create_setting[typing][select_pos[1]:]
                                    type_pos = select_pos[0]
                                    select_pos = None
                                else:
                                    if type_pos < len(create_setting[typing]):
                                        line_animationframe = 0
                                        create_setting[typing] = create_setting[typing][0:type_pos] + create_setting[typing][type_pos+1:]
                            elif event.key == pygame.K_RIGHT:
                                if select_pos:
                                    type_pos = select_pos[1]
                                    select_pos = None
                                else:
                                    type_pos = min(type_pos+1,len(create_setting[typing]))
                            elif event.key == pygame.K_RIGHT and event.mod & pygame.KMOD_LSHIFT:
                                if type_pos < len(create_setting[typing]):
                                    if select_pos:
                                        select_pos[select_pos.index(type_pos)] += 1
                                        if select_pos[0] == select_pos[1]:
                                            select_pos = None
                                    else:
                                        select_pos = [type_pos,type_pos+1]
                                    type_pos = min(type_pos+1,len(create_setting[typing]))
                            elif event.key == pygame.K_LEFT:
                                if select_pos:
                                    type_pos = select_pos[0]
                                    select_pos = None
                                else:
                                    type_pos = max(type_pos-1,0)
                            elif event.key == pygame.K_LEFT and event.mod & pygame.KMOD_LSHIFT:
                                if type_pos > 0:
                                    if select_pos:
                                        select_pos[select_pos.index(type_pos)] -= 1
                                        if select_pos[0] == select_pos[1]:
                                            select_pos = None
                                    else:
                                        select_pos = [type_pos-1,type_pos]
                                    type_pos = max(type_pos-1,0)
                            elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                                if select_pos:
                                    text = pygame.scrap.get_text()
                                    create_setting[typing] = create_setting[typing][0:select_pos[0]] + text + create_setting[typing][select_pos[1]:]
                                    type_pos = select_pos[0] + len(text)
                                    select_pos = None
                                else:
                                    create_setting[typing] = create_setting[typing][0:type_pos] + pygame.scrap.get_text() + create_setting[typing][type_pos:] 
                            elif event.key == pygame.K_c and event.mod & pygame.KMOD_CTRL:
                                if select_pos:
                                    pygame.scrap.put_text(create_setting[typing][select_pos[0]:select_pos[1]])
                            elif event.key == pygame.K_x and event.mod & pygame.KMOD_CTRL:
                                if select_pos:
                                    pygame.scrap.put_text(create_setting[typing][select_pos[0]:select_pos[1]])
                                    create_setting[typing] = create_setting[typing][0:select_pos[0]] + create_setting[typing][select_pos[1]:]
                                    type_pos = select_pos[0]
                                    select_pos = None
                            elif event.key == pygame.K_a and event.mod & pygame.KMOD_CTRL:
                                select_pos = [0,len(create_setting[typing])]
                            elif event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL:
                                if backup_pos == -1:
                                    text_backup.append(create_setting[typing])
                                    if len(text_backup) > 10:
                                        text_backup.pop(0)
                                backup_pos = max(backup_pos-1,len(text_backup)*-1)
                                create_setting[typing] = text_backup[backup_pos]
                                select_pos = None
                            elif event.key == pygame.K_z and event.mod & pygame.KMOD_CTRL and event.mod & pygame.KMOD_LSHIFT:
                                backup_pos = min(backup_pos+1,-1)
                                create_setting[typing] = text_backup[backup_pos]
                                select_pos = None
                            else:
                                if select_pos:
                                    line_animationframe = 0
                                    create_setting[typing] = create_setting[typing][0:select_pos[0]] + event.unicode + create_setting[typing][select_pos[1]:]
                                    type_pos = select_pos[0]
                                    select_pos = None
                                else:
                                    line_animationframe = 0
                                    create_setting[typing] = create_setting[typing][0:type_pos] + event.unicode + create_setting[typing][type_pos:]
                                    type_pos += 1
                            
                pygame.display.flip()
                
        def join_match_menu(self):
            setting_button = {
                "quit": [20,18,37,37],
                "join": [726,837,468,87],
                "join_mode": [841,720,237,52]
            }
            input_bar = {
                IP: [664,382,592,66],
                PORT: [664,620,592,66],
                CODE: [664,542,592,66]
            }
            setting_font = pygame.font.SysFont("Consolas",48,True)
            error_font = pygame.font.SysFont("Consolas",28,True)
            typing = False
            line_animationframe = 0
            #################################
            join_setting = {
                IP: "",
                PORT: "",
                CODE: ""
            }
            mode = SERVER
            error = ""
            error_frame = 0
            #################################
            #################################
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"match_setting_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                for button in [*setting_button]:
                    button_rect = adjust_rect(setting_button[button],screen_ratio)
                    if button == "join_mode":
                        screen.blit(adjust_surface(self.assets[f"{button}_{int(mode)}"],screen_ratio),button_rect.topleft)
                    else:
                        screen.blit(adjust_surface(self.assets[button],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                if mode:
                    screen.blit(adjust_surface(setting_font.render("IP Address:",True,GRAY),screen_ratio),adjust_pos((664,307),screen_ratio))
                    screen.blit(adjust_surface(setting_font.render("Port:",True,GRAY),screen_ratio),adjust_pos((664,549),screen_ratio))
                    screen.blit(adjust_surface(self.assets["match_code_input"],screen_ratio),adjust_pos((664,382),screen_ratio))
                    screen.blit(adjust_surface(self.assets["match_code_input"],screen_ratio),adjust_pos((664,620),screen_ratio))
                else:
                    screen.blit(adjust_surface(setting_font.render("Match Code:",True,GRAY),screen_ratio),adjust_pos((664,472),screen_ratio))
                    screen.blit(adjust_surface(self.assets["match_code_input"],screen_ratio),adjust_pos((664,542),screen_ratio))
                if mode:
                    if len(join_setting[IP]) > 22:
                        screen.blit(adjust_surface(setting_font.render(join_setting[IP][-22:],True,GRAY),screen_ratio),adjust_pos((664,392),screen_ratio))
                    else:
                        screen.blit(adjust_surface(setting_font.render(join_setting[IP],True,GRAY),screen_ratio),adjust_pos((664,392),screen_ratio))
                    screen.blit(adjust_surface(setting_font.render(join_setting[PORT],True,GRAY),screen_ratio),adjust_pos((664,630),screen_ratio))
                else:
                    if len(join_setting[CODE]) > 22:
                        screen.blit(adjust_surface(setting_font.render(join_setting[CODE][-22:],True,GRAY),screen_ratio),adjust_pos((664,552),screen_ratio))
                    else:
                        screen.blit(adjust_surface(setting_font.render(join_setting[CODE],True,GRAY),screen_ratio),adjust_pos((664,552),screen_ratio))
                if typing:
                    if line_animationframe <= 22:
                        if len(join_setting[typing]) > 22:
                            text_end = setting_font.render(join_setting[typing][-22:],True,WHITE).get_size()[0]
                        else:
                            text_end = setting_font.render(join_setting[typing],True,WHITE).get_size()[0]
                        pygame.draw.rect(screen,WHITE,adjust_rect((664+text_end,input_bar[typing][1]+3,2,65),screen_ratio))
                    elif line_animationframe > 60:
                        line_animationframe = 0
                    line_animationframe += 1
                if error != "":
                    error_frame += 1
                    error_text = error_font.render(error,True,(245,214,53))
                    screen.blit(adjust_surface(error_text,screen_ratio),adjust_pos([(1920-error_text.get_size()[0])/2,794],screen_ratio))
                    if error_frame == 180:
                        error_frame = 0
                        error = ""
                #################################
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*setting_button]:
                                rect = adjust_rect(setting_button[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        return 0
                                    elif button == "join":
                                        if mode:
                                            try:
                                                rematching = self.lan_match(join_setting[IP],int(join_setting[PORT]))
                                                while rematching:
                                                    rematching = self.lan_match(join_setting[IP],int(join_setting[PORT]))
                                            except:
                                                error = "No further connection"
                                        else:
                                            match_property = get_match(join_setting[CODE])
                                            if match_property == "None":
                                                error = "Match doesn't exist"
                                            elif match_property == "Full":
                                                error = "Match is full"
                                            elif match_property == "Ended":
                                                error = "Match has ended"
                                            rematching = self.online_match(join_setting[CODE])
                                            while rematching:
                                                rematching = self.online_match(join_setting[CODE])
                                    elif button == "join_mode":
                                        mode = not mode
                            typing = False
                            for bar in [*input_bar]:
                                rect = adjust_rect(input_bar[bar],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if bar == CODE:
                                        if not mode:
                                            typing = bar
                                    else:
                                        if mode:
                                            typing = bar
                                    
                    if event.type == MOUSEWHEEL:
                        rect = adjust_rect([860,272,233,39],screen_ratio)
                        if rect.collidepoint(mouse_pos):
                            grid = min(max(grid+event.y,3),5)
                                    
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return 0
                        if typing:
                            if event.key == pygame.K_BACKSPACE:
                                line_animationframe = 0
                                join_setting[typing] = join_setting[typing][:-1]
                            elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                                join_setting[typing] = pygame.scrap.get_text()
                            else:
                                line_animationframe = 0
                                join_setting[typing] += event.unicode
                            
                pygame.display.flip()

        def online_match_menu(self):
            buttons = {
                "quit": [20,18,37,37],
                "Refresh": [308,83,122,40],
                "Quick Match": [435,83,122,40],
                "Create": [563,83,122,40],
                "Join": [690,83,122,40],
                "Filter": [817,83,122,40],
                "Page Up": [1553,968,18,29],
                "Page Down": [1608,968,18,29]
            }
            setting_font = pygame.font.SysFont("Consolas",48,True)
            page_font = pygame.font.SysFont("Consolas",29,True)
            typing = False
            line_animationframe = 0
            #################################
            name_font = pygame.font.SysFont("Consolas",29,True)
            mode_font = pygame.font.SysFont("Consolas",16,True)
            size_font = pygame.font.SysFont("Consolas",21,True)
            filters = "None"
            page = 1
            matches = resolve_matches_string(fetch_matches(page))
            #################################
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                ################################# Menu
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"online_menu_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                for button in [*buttons]:
                    button_rect = adjust_rect(buttons[button],screen_ratio)
                    screen.blit(adjust_surface(self.assets[button],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                screen.blit(adjust_surface(page_font.render(str(page),True,GRAY),screen_ratio),adjust_pos((1608-9-16*len(str(page)),968),screen_ratio))
                for i in range(0,len(matches)):
                    bar_pos = [326,147+i*17]
                    screen.blit(adjust_surface(self.assets[f"match_bar"],screen_ratio),adjust_pos((bar_pos[0],bar_pos[1]),screen_ratio))
                    screen.blit(adjust_surface(name_font.render(matches[i]["name"],True,GRAY),screen_ratio),adjust_pos((bar_pos[0]+15,bar_pos[1]+11),screen_ratio))
                    screen.blit(adjust_surface(mode_font.render("Grid:",True,GRAY),screen_ratio),adjust_pos((bar_pos[0]+15,bar_pos[1]+61),screen_ratio))
                    screen.blit(adjust_surface(mode_font.render(f"{matches[i]["grid"]}x{matches[i]["grid"]}",True,GRAY),screen_ratio),adjust_pos((bar_pos[0]+60,bar_pos[1]+61),screen_ratio))
                    screen.blit(adjust_surface(size_font.render(f"{matches[i]["player"]}/{matches[i]["size"]}",True,GRAY),screen_ratio),adjust_pos((bar_pos[0]+1236,bar_pos[1]+32),screen_ratio))
                    bar_rect = adjust_rect([bar_pos[0],bar_pos[1],1282,88],screen_ratio)
                    if bar_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"pressed_shader"],bar_rect.size),bar_rect.topleft)
                #################################
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*buttons]:
                                rect = adjust_rect(buttons[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        return 0
                                    elif button == "Create":
                                        self.online_match_settings()
                                    elif button == "Join":
                                        self.join_match_menu()
                                    elif button == "Refresh":
                                        page = 1
                                        matches = resolve_matches_string(fetch_matches(page))
                                    elif button == "Quick Match":
                                        matches = resolve_matches_string(fetch_matches(1))
                                        match_code = matches[random.randint(0,len(matches)-1)]["code"]
                                        rematching = self.online_match(match_code)
                                        while rematching:
                                            rematching = self.online_match(match_code)
                                    elif button == "Filter":
                                        pass
                                    elif button == "Page Up":
                                        page = max(page-1,1)
                                        buttons["Page Up"][0] = buttons["Page Down"][0]-18-16*len(str(page))-buttons["Page Up"][2]
                                        matches = resolve_matches_string(fetch_matches(page))
                                    elif button == "Page Down":
                                        page += 1
                                        buttons["Page Up"][0] = buttons["Page Down"][0]-18-16*len(str(page))-buttons["Page Up"][2]
                                        matches = resolve_matches_string(fetch_matches(page))
                            for i in range(0,len(matches)):
                                bar_rect = adjust_rect([326,147+i*17,1282,88],screen_ratio)
                                if bar_rect.collidepoint(mouse_pos):
                                    match_code = matches[i]["code"]
                                    rematching = self.online_match(match_code)
                                    while rematching:
                                        rematching = self.online_match(match_code)
                            typing = False
                            rect = adjust_rect([810,700,592,66],screen_ratio)
                            if rect.collidepoint(mouse_pos):
                                typing = True
                                    
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return 0
                        if typing:
                            if event.key == pygame.K_BACKSPACE:
                                line_animationframe = 0
                                code = code[:-1]
                            elif event.key == pygame.K_v and event.mod & pygame.KMOD_CTRL:
                                code = pygame.scrap.get_text()
                            else:
                                if event.unicode in string.ascii_letters or event.unicode in ["0","1","2","3","4","5","6","7","8","9"]:
                                    line_animationframe = 0
                                    code += event.unicode
                            
                pygame.display.flip()

        def match_waiting(self,match_id):
            match_property = resolve_match_string(get_match(match_id))
            dot_animation = 0
            dot_frame = 0
            buffer_delay = 60
            delay = 0
            wait_font = pygame.font.SysFont("Consolas",64,True)
            player_font = pygame.font.SysFont("Consolas",48,True)
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"online_menu_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                screen.blit(adjust_surface(wait_font.render(f"Waiting for the match to start{"."*(dot_animation%4)}",True,GRAY),screen_ratio),adjust_pos((379,440),screen_ratio))
                dot_frame += 1
                if dot_frame >= 30:
                    dot_frame = 0
                    dot_animation += 1
                screen.blit(adjust_surface(player_font.render(f"{match_property["Player"]}/{match_property["Size"]}",True,GRAY),screen_ratio),adjust_pos((921,571),screen_ratio))
                screen.blit(adjust_surface(self.assets[f"cancel_waiting"],screen_ratio),adjust_pos((726,837),screen_ratio))
                rect = adjust_rect([726,837,468,87],screen_ratio)
                if rect.collidepoint(mouse_pos):
                    screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],rect.size),rect.topleft)
                #################################
                delay += 1
                if delay == buffer_delay:
                    delay = 0
                    match_property = resolve_match_string(get_match(match_id))
                    if match_property["Player"] == match_property["Size"]:
                        update_match(match_id,"Type","Private")
                        return 1
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            rect = adjust_rect([726,837,468,87],screen_ratio)
                            if rect.collidepoint(mouse_pos):
                                match_property = resolve_match_string(get_match(match_id))
                                if match_property["Player"] - 1 > 0:
                                    update_match(match_id,"Player",match_property["Player"]-1)
                                else:
                                    delete_match(match_id)
                                return 0
                            
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            match_property = resolve_match_string(get_match(match_id))
                            if match_property["Player"] - 1 > 0:
                                update_match(match_id,"Player",match_property["Player"]-1)
                            else:
                                delete_match(match_id)
                            return 0
                            
                pygame.display.flip()
                
        def LAN_match_waiting(self,address):
            match_property = resolve_match_string(get_LAN_match(address))
            dot_animation = 0
            dot_frame = 0
            buffer_delay = 30
            delay = 0
            wait_font = pygame.font.SysFont("Consolas",64,True)
            player_font = pygame.font.SysFont("Consolas",48,True)
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"online_menu_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                screen.blit(adjust_surface(wait_font.render(f"Waiting for the match to start{"."*(dot_animation%4)}",True,GRAY),screen_ratio),adjust_pos((379,440),screen_ratio))
                dot_frame += 1
                if dot_frame >= 30:
                    dot_frame = 0
                    dot_animation += 1
                screen.blit(adjust_surface(player_font.render(f"{match_property["Player"]}/{match_property["Size"]}",True,GRAY),screen_ratio),adjust_pos((921,571),screen_ratio))
                screen.blit(adjust_surface(self.assets[f"cancel_waiting"],screen_ratio),adjust_pos((726,837),screen_ratio))
                rect = adjust_rect([726,837,468,87],screen_ratio)
                if rect.collidepoint(mouse_pos):
                    screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],rect.size),rect.topleft)
                #################################
                delay += 1
                if delay == buffer_delay:
                    delay = 0
                    match_property = resolve_match_string(get_LAN_match(address))
                    if match_property["Player"] == match_property["Size"]:
                        return 1
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            rect = adjust_rect([726,837,468,87],screen_ratio)
                            if rect.collidepoint(mouse_pos):
                                match_property = resolve_match_string(get_LAN_match(address))
                                if match_property["Player"] - 1 > 0:
                                    update_LAN_match(address,"Player",match_property["Player"]-1)
                                else:
                                    delete_LAN_match(address)
                                return 0
                            
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            match_property = resolve_match_string(get_LAN_match(address))
                            if match_property["Player"] - 1 > 0:
                                update_LAN_match(address,"Player",match_property["Player"]-1)
                            else:
                                delete_LAN_match(address)
                            return 0
                            
                pygame.display.flip()
                
        def end_local_match(self,match_property):
            buttons = {
                "quit": [398,794,468,87],
                "rematch": [1054,794,468,87]
            }
            result_font = pygame.font.SysFont("Consolas",69,True)
            score_font = pygame.font.SysFont("Consolas",40,True)
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                ################################# Menu
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"result_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                for button in [*buttons]:
                    button_rect = adjust_rect(buttons[button],screen_ratio)
                    screen.blit(adjust_surface(self.assets[f"result_{button}"],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                if match_property["Player 1 Score"] > match_property["Player 2 Score"]:
                    screen.blit(adjust_surface(result_font.render("Player 1 wins",True,(234,237,151)),screen_ratio),adjust_pos((744,250),screen_ratio))
                elif match_property["Player 1 Score"] < match_property["Player 2 Score"]:
                    screen.blit(adjust_surface(result_font.render("Player 2 wins",True,(234,237,151)),screen_ratio),adjust_pos((744,250),screen_ratio))
                else:
                    screen.blit(adjust_surface(result_font.render("Tie",True,GRAY),screen_ratio),adjust_pos((910,250),screen_ratio))
                screen.blit(adjust_surface(score_font.render(f"Player 1 score: {match_property["Player 1 Score"]}",True,GRAY),screen_ratio),adjust_pos((794,364),screen_ratio))
                screen.blit(adjust_surface(score_font.render(f"Player 2 score: {match_property["Player 2 Score"]}",True,GRAY),screen_ratio),adjust_pos((794,423),screen_ratio))
                #################################
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*buttons]:
                                rect = adjust_rect(buttons[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        return 0
                                    elif button == "rematch":
                                        return 1
                            
                pygame.display.flip()
        
        def end_online_match(self,match_id,player):
            match_property = resolve_match_string(get_ended_match(match_id))
            buttons = {
                "quit": [398,794,468,87],
                "rematch": [1054,794,468,87]
            }
            result_font = pygame.font.SysFont("Consolas",69,True)
            score_font = pygame.font.SysFont("Consolas",40,True)
            player_font = pygame.font.SysFont("Consolas",47,True)
            rematch_pressed = False
            buffer_delay = 30
            delay = 0
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                ################################# Menu
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"result_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                for button in [*buttons]:
                    button_rect = adjust_rect(buttons[button],screen_ratio)
                    screen.blit(adjust_surface(self.assets[f"result_{button}"],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                other_player = (player-1) * -1
                if match_property[f"Player {player+1} Score"] > match_property[f"Player {other_player+1} Score"]:
                    screen.blit(adjust_surface(result_font.render("Win",True,(234,237,151)),screen_ratio),adjust_pos((910,250),screen_ratio))
                elif match_property[f"Player {player+1} Score"] < match_property[f"Player {other_player+1} Score"]:
                    screen.blit(adjust_surface(result_font.render("Lose",True,(132,139,196)),screen_ratio),adjust_pos((884,250),screen_ratio))
                else:
                    screen.blit(adjust_surface(result_font.render("Tie",True,GRAY),screen_ratio),adjust_pos((910,250),screen_ratio))
                player_1_score = match_property["Player 1 Score"] if match_property["Player 1 Score"] != -999 else "Surrender"
                player_2_score = match_property["Player 2 Score"] if match_property["Player 2 Score"] != -999 else "Surrender"
                screen.blit(adjust_surface(score_font.render(f"Player 1 score: {player_1_score}",True,GRAY),screen_ratio),adjust_pos((794,364),screen_ratio))
                screen.blit(adjust_surface(score_font.render(f"Player 2 score: {player_2_score}",True,GRAY),screen_ratio),adjust_pos((794,423),screen_ratio))
                screen.blit(adjust_surface(player_font.render(f"{match_property["Rematch"]}/{match_property["Size"]}",True,GRAY),screen_ratio),adjust_pos((1255,731),screen_ratio))
                #################################
                delay += 1
                if delay == buffer_delay:
                    delay = 0
                    match_property = resolve_match_string(get_ended_match(match_id))
                    if match_property == "None":
                        if get_match(match_id) != "None":
                            return 1
                        else:
                            return 0
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*buttons]:
                                rect = adjust_rect(buttons[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        if not rematch_pressed:
                                            delete_match(match_id)
                                    elif button == "rematch":
                                        if not rematch_pressed:
                                            rematch(match_id)
                                            rematch_pressed = True
                            
                pygame.display.flip()
                
        def end_lan_match(self,address,player):
            match_property = resolve_match_string(get_LAN_match(address))
            buttons = {
                "quit": [398,794,468,87],
                "rematch": [1054,794,468,87]
            }
            result_font = pygame.font.SysFont("Consolas",69,True)
            score_font = pygame.font.SysFont("Consolas",40,True)
            player_font = pygame.font.SysFont("Consolas",47,True)
            rematch_pressed = False
            buffer_delay = 30
            delay = 0
            menu = True
            while menu:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                ################################# Menu
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                screen.blit(adjust_surface(self.assets[f"result_background"],screen_ratio),adjust_pos((307,125),screen_ratio))
                for button in [*buttons]:
                    button_rect = adjust_rect(buttons[button],screen_ratio)
                    screen.blit(adjust_surface(self.assets[f"result_{button}"],screen_ratio),button_rect.topleft)
                    if button_rect.collidepoint(mouse_pos):
                        screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                other_player = (player-1) * -1
                if match_property[f"Player {player+1} Score"] > match_property[f"Player {other_player+1} Score"]:
                    screen.blit(adjust_surface(result_font.render("Win",True,(234,237,151)),screen_ratio),adjust_pos((910,250),screen_ratio))
                elif match_property[f"Player {player+1} Score"] < match_property[f"Player {other_player+1} Score"]:
                    screen.blit(adjust_surface(result_font.render("Lose",True,(132,139,196)),screen_ratio),adjust_pos((884,250),screen_ratio))
                else:
                    screen.blit(adjust_surface(result_font.render("Tie",True,GRAY),screen_ratio),adjust_pos((910,250),screen_ratio))
                player_1_score = match_property["Player 1 Score"] if match_property["Player 1 Score"] != -999 else "Surrender"
                player_2_score = match_property["Player 2 Score"] if match_property["Player 2 Score"] != -999 else "Surrender"
                screen.blit(adjust_surface(score_font.render(f"Player 1 score: {player_1_score}",True,GRAY),screen_ratio),adjust_pos((794,364),screen_ratio))
                screen.blit(adjust_surface(score_font.render(f"Player 2 score: {player_2_score}",True,GRAY),screen_ratio),adjust_pos((794,423),screen_ratio))
                screen.blit(adjust_surface(score_font.render(f"{match_property["Rematch"]}/{match_property["Size"]}",True,GRAY),screen_ratio),adjust_pos((1255,731),screen_ratio))
                #################################
                delay += 1
                if delay == buffer_delay:
                    delay = 0
                    match_property = resolve_match_string(get_LAN_match(address))
                    if match_property["Rematch"] == match_property["Size"]:
                        return 1
                    else:
                        if match_property["Rematch"] < 0:
                            if match_property["Player"] - 1 > 0:
                                update_LAN_match(address,"Player",match_property["Player"]-1)
                            else:
                                delete_LAN_match(address)
                            return 0
                        
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            for button in [*buttons]:
                                rect = adjust_rect(buttons[button],screen_ratio)
                                if rect.collidepoint(mouse_pos):
                                    if button == "quit":
                                        if not rematch_pressed:
                                            update_LAN_match(address,"Rematch",match_property["Size"]*-1)
                                    elif button == "rematch":
                                        if not rematch_pressed:
                                            LAN_rematch(address)
                                            rematch_pressed = True
                            
                pygame.display.flip()        
        
        def local_match(self):
            match_property = self.local_match_settings()
            if match_property:
                screen_size = screen.get_size()
                screen_ratio = [screen_size[0]/ScreenWidth,screen_size[1]/ScreenHeight]
                box_ratio = 3/self.grid
                #################################
                box_size = [168*box_ratio,159*box_ratio]
                player1_box_rect = calculate_rect(self.grid,[547,569])
                player2_box_rect = calculate_rect(self.grid,[547,13])
                match_turn = random.randint(0,1)
                dice = random.randint(1,6)
                #################################
                place_animation_frame = 8
                animation_ratio = 7/6
                player1_animation_frame = 0
                player2_animation_frame = 0
                player1_placed = None
                player2_placed = None
                x = random.randint(0,408-138)
                y = random.randint(0,189-138)
                score_font = pygame.font.SysFont("Consolas",55,True)
                #################################
                game = True
                while game:

                    main_clock.tick(FPS)
                    #################################
                    mouse_pos = pygame.mouse.get_pos()
                    screen_size = self.screen_size
                    screen_ratio = self.screen_ratio
                    #################################
                    screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                    for i in range(0,len(player1_box_rect)):
                        for j in range(0,len(player1_box_rect[i])):
                            box = player1_box_rect[i][j]
                            number = match_property["Player 1 Board"][i][j]
                            screen.blit(adjust_surface(pygame.transform.scale(self.assets["box"],box_size),screen_ratio),adjust_pos((box[0],box[1]),screen_ratio))
                            if number:
                                if player1_placed and i == player1_placed[0] and j == player1_placed[1]:
                                    temp_ratio = animation_ratio-((animation_ratio-1)/place_animation_frame)*(place_animation_frame-player1_animation_frame)
                                    screen.blit(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[box_ratio*temp_ratio,box_ratio*temp_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio*temp_ratio,box[1]+10*box_ratio*temp_ratio),screen_ratio))
                                    player1_animation_frame -= 1
                                    if not player1_animation_frame:
                                        player1_placed = None
                                else:
                                    screen.blit(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[box_ratio,box_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio,box[1]+10*box_ratio),screen_ratio))
                    for i in range(0,len(player2_box_rect)):
                        for j in range(0,len(player2_box_rect[i])):
                            box = player2_box_rect[i][j]
                            number = match_property["Player 2 Board"][i][j]
                            screen.blit(adjust_surface(pygame.transform.scale(self.assets["box"],box_size),screen_ratio),adjust_pos((box[0],box[1]),screen_ratio))
                            if number:
                                if player2_placed and i == player2_placed[0] and j == player2_placed[1]:
                                    temp_ratio = animation_ratio-((animation_ratio-1)/place_animation_frame)*(place_animation_frame-player2_animation_frame)
                                    screen.blit(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[box_ratio*temp_ratio,box_ratio*temp_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio*temp_ratio,box[1]+10*box_ratio*temp_ratio),screen_ratio))
                                    player2_animation_frame -= 1
                                    if not player2_animation_frame:
                                        player2_placed = None
                                else:
                                    screen.blit(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[box_ratio,box_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio,box[1]+10*box_ratio),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"dice_box"],screen_ratio),adjust_pos((15,855),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"dice_box"],screen_ratio),adjust_pos((1465,17),screen_ratio))
                    if match_turn == 0:
                        screen.blit(adjust_surface(self.assets[f"dice {dice}"],screen_ratio),adjust_pos((31+x,864+y),screen_ratio))
                    else:
                        screen.blit(adjust_surface(self.assets[f"dice {dice}"],screen_ratio),adjust_pos((1481+x,26+y),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"score_box"],screen_ratio),adjust_pos((54,14),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"score_box"],screen_ratio),adjust_pos((1518,844),screen_ratio))
                    score_size = score_font.render(str(match_property["Player 1 Score"]),True,GRAY).get_size()
                    screen.blit(adjust_surface(score_font.render(str(match_property["Player 1 Score"]),True,GRAY),screen_ratio),adjust_pos((1529+(327-score_size[0])/2,924+(132-score_size[1])/2),screen_ratio))
                    score_size = score_font.render(str(match_property["Player 2 Score"]),True,GRAY).get_size()
                    screen.blit(adjust_surface(score_font.render(str(match_property["Player 2 Score"]),True,GRAY),screen_ratio),adjust_pos((65+(327-score_size[0])/2,94+(132-score_size[1])/2),screen_ratio))
                    #################################
                    
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        if event.type == VIDEORESIZE:
                            self.screen_size = screen.get_size()
                            self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                            
                        if event.type == MOUSEBUTTONDOWN:
                            if event.button == 1:
                                if match_turn == 0:
                                    for i in range(0,len(player1_box_rect)):
                                        for j in range(0,len(player1_box_rect[i])):
                                            rect = adjust_rect(player1_box_rect[i][j],screen_ratio)
                                            if rect.collidepoint(mouse_pos):
                                                if not match_property["Player 1 Board"][i][j]:
                                                    match_property["Player 1 Board"][i][j] = dice
                                                    remove_dice(match_property["Player 2 Board"],j,dice)
                                                    match_property["Round"] += 1
                                                    dice = random.randint(1,6)
                                                    match_turn = 1
                                                    player1_placed = [i,j]
                                                    player1_animation_frame = place_animation_frame
                                                    match_property["Player 1 Score"]  = calculate_score(match_property["Player 1 Board"])
                                                    match_property["Player 2 Score"]  = calculate_score(match_property["Player 2 Board"])
                                                    x = random.randint(0,408-138)
                                                    y = random.randint(0,189-138)
                                    if finish_board(match_property["Player 1 Board"]):
                                        game = False
                                        return self.end_local_match(match_property)
                                else:
                                    for i in range(0,len(player2_box_rect)):
                                        for j in range(0,len(player2_box_rect[i])):
                                            rect = adjust_rect(player2_box_rect[i][j],screen_ratio)
                                            if rect.collidepoint(mouse_pos):
                                                if not match_property["Player 2 Board"][i][j]:
                                                    match_property["Player 2 Board"][i][j] = dice
                                                    remove_dice(match_property["Player 1 Board"],j,dice)
                                                    match_property["Round"] += 1
                                                    dice = random.randint(1,6)
                                                    match_turn = 0
                                                    player2_placed = [i,j]
                                                    player2_animation_frame = place_animation_frame
                                                    match_property["Player 1 Score"]  = calculate_score(match_property["Player 1 Board"])
                                                    match_property["Player 2 Score"]  = calculate_score(match_property["Player 2 Board"])
                                                    x = random.randint(0,408-138)
                                                    y = random.randint(0,189-138)
                                    if finish_board(match_property["Player 2 Board"]):
                                        game = False
                                        return self.end_local_match(match_property)
                                        
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                return 0

                                
                    pygame.display.flip()
            else:
                return 0
            
        def online_match(self,match_id):
            match_property = get_match(match_id)
            if match_property != "None" and match_property != "Ended":
                match_property = resolve_match_string(match_property)
                if match_property["Player"] == match_property["Size"]:
                    return "Full"
                player = match_property["Player"]
                update_match(match_id,"Player",player+1)
                start = self.match_waiting(match_id)
                if not start:
                    return 0
                #################################
                box_ratio = 3/match_property["Grid"]
                box_size = [168*box_ratio,159*box_ratio]
                if player == 0:
                    boards = [resolve_board_string(match_property["Player 1 Board"]),flip_board(resolve_board_string(match_property["Player 2 Board"]))]
                    box_rects = [calculate_rect(match_property["Grid"],[547,569]),calculate_rect(match_property["Grid"],[547,13])]
                else:
                    boards = [flip_board(resolve_board_string(match_property["Player 1 Board"])),resolve_board_string(match_property["Player 2 Board"])]
                    box_rects = [calculate_rect(match_property["Grid"],[547,13]),calculate_rect(match_property["Grid"],[547,569])]
                #################################
                place_animation_frame = 8
                animation_ratio = 7/6
                animation_frames = [0,0]
                placed = resolve_placed_string(match_property["Placed"])
                x = random.randint(0,408-138)
                y = random.randint(0,189-138)
                score_font = pygame.font.SysFont("Consolas",55,True)
                buffer_delay = 30
                delay = 0
                menu = False
                option_button = {
                    "resume": [743,401,433,81],
                    "settings": [743,500,433,81],
                    "support": [743,598,433,81],
                    "surrender": [743,697,433,81]
                }
                #################################
                game = True
                while game:

                    main_clock.tick(FPS)
                    #################################
                    mouse_pos = pygame.mouse.get_pos()
                    screen_size = self.screen_size
                    screen_ratio = self.screen_ratio
                    #################################
                    screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                    for b in range(0,len(boards)):
                        for i in range(0,len(box_rects[b])):
                            for j in range(0,len(box_rects[b][i])):
                                box = box_rects[b][i][j]
                                number = boards[b][i][j]
                                screen.blit(adjust_surface(pygame.transform.scale(self.assets["box"],box_size),screen_ratio),adjust_pos((box[0],box[1]),screen_ratio))
                                if number:
                                    if i == placed[b][0] and j == placed[b][1] and animation_frames[b] > 0:
                                        temp_ratio = animation_ratio-((animation_ratio-1)/place_animation_frame)*(place_animation_frame-animation_frames[b])
                                        screen.blit(adjust_surface(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[temp_ratio,temp_ratio]),[box_ratio,box_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio*temp_ratio,box[1]+10*box_ratio*temp_ratio),screen_ratio))
                                        animation_frames[b] -= 1
                                        if not animation_frames[b]:
                                            update_match(match_id,"Placed",[player,-1])
                                    else:
                                        screen.blit(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[box_ratio,box_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio,box[1]+10*box_ratio),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"score_box"],screen_ratio),adjust_pos((54,14),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"score_box"],screen_ratio),adjust_pos((1518,844),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"dice_box"],screen_ratio),adjust_pos((15,855),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"dice_box"],screen_ratio),adjust_pos((1465,17),screen_ratio))
                    if player == 0:
                        score_size = score_font.render(str(match_property["Player 1 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 1 Score"]),True,GRAY),screen_ratio),adjust_pos((1529+(327-score_size[0])/2,924+(132-score_size[1])/2),screen_ratio))
                        score_size = score_font.render(str(match_property["Player 2 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 2 Score"]),True,GRAY),screen_ratio),adjust_pos((65+(327-score_size[0])/2,94+(132-score_size[1])/2),screen_ratio))
                    else:
                        score_size = score_font.render(str(match_property["Player 2 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 2 Score"]),True,GRAY),screen_ratio),adjust_pos((1529+(327-score_size[0])/2,924+(132-score_size[1])/2),screen_ratio))
                        score_size = score_font.render(str(match_property["Player 1 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 1 Score"]),True,GRAY),screen_ratio),adjust_pos((65+(327-score_size[0])/2,94+(132-score_size[1])/2),screen_ratio))
                    if match_property["Turn"] == player:
                        screen.blit(adjust_surface(self.assets[f"dice {match_property["Dice"]}"],screen_ratio),adjust_pos((31+x,864+y),screen_ratio))
                    else:
                        screen.blit(adjust_surface(self.assets[f"dice {match_property["Dice"]}"],screen_ratio),adjust_pos((1481+x,26+y),screen_ratio))
                    if menu:
                        screen.blit(adjust_surface(self.assets[f"option_menu_background"],screen_ratio),adjust_pos((727,293),screen_ratio))
                        for button in [*option_button]:
                            button_rect = adjust_rect(option_button[button],screen_ratio)
                            screen.blit(adjust_surface(self.assets[f"option_{button}"],screen_ratio),button_rect.topleft)
                            if button_rect.collidepoint(mouse_pos):
                                screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                    #################################
                    delay += 1
                    if delay == buffer_delay:
                        delay = 0
                        match_property = resolve_match_string(get_match(match_id))
                        if match_property == "Ended":
                            game = False
                            return self.end_online_match(match_id,player)
                        elif match_property:
                            if player == 0:
                                boards = [resolve_board_string(match_property["Player 1 Board"]),flip_board(resolve_board_string(match_property["Player 2 Board"]))]
                            else:
                                boards = [flip_board(resolve_board_string(match_property["Player 1 Board"])),resolve_board_string(match_property["Player 2 Board"])]
                        placing = resolve_placed_string(match_property["Placed"])
                        for i in range(0,len(placing)):
                            if placing[i] != placed[i] and placed[i] == [-1,-1]:
                                animation_frames[i] = place_animation_frame
                            placed[i] = placing[i]
                    
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()
                            
                        if event.type == VIDEORESIZE:
                            self.screen_size = screen.get_size()
                            self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                            
                        if event.type == MOUSEBUTTONDOWN:
                            if event.button == 1:
                                if menu:
                                    for button in [*option_button]:
                                        rect = adjust_rect(option_button[button],screen_ratio)
                                        if rect.collidepoint(mouse_pos):
                                            if button == "resume":
                                                menu = False
                                            elif button == "settings":
                                                self.settings()
                                            elif button == "support":
                                                pass
                                            elif button == "surrender":
                                                update_match(match_id,f"Player {player+1} Score",-999)
                                                end_match(match_id)
                                else:
                                    for i in range(0,len(box_rects[player])):
                                        for j in range(0,len(box_rects[player][i])):
                                            rect = adjust_rect(box_rects[player][i][j],screen_ratio)
                                            if rect.collidepoint(mouse_pos) and match_property["Turn"] == player:
                                                if not boards[player][i][j]:
                                                    update_match(match_id,f"Player {player+1} Board",(i,j))
                                                    placed[player] = [i,j]
                                                    animation_frames[player] = place_animation_frame
                                                    x = random.randint(0,408-138)
                                                    y = random.randint(0,189-138)
                                                    
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                menu = not menu
                                
                    pygame.display.flip()
            else:
                return 0
            
        def lan_match(self,ip,port):
            address = (ip,port)
            match_property = resolve_match_string(get_LAN_match(address))
            #################################
            player = match_property["Player"]
            update_LAN_match(address,"Player",player+1)
            start = self.LAN_match_waiting(address)
            if not start:
                return 0
            #################################
            box_ratio = 3/match_property["Grid"]
            box_size = [168*box_ratio,159*box_ratio]
            if player == 0:
                boards = [resolve_board_string(match_property["Player 1 Board"]),flip_board(resolve_board_string(match_property["Player 2 Board"]))]
                box_rects = [calculate_rect(self.grid,[547,569]),calculate_rect(self.grid,[547,13])]
            else:
                boards = [flip_board(resolve_board_string(match_property["Player 1 Board"])),resolve_board_string(match_property["Player 2 Board"])]
                box_rects = [calculate_rect(self.grid,[547,13]),calculate_rect(self.grid,[547,569])]
            #################################
            place_animation_frame = 8
            animation_ratio = 7/6
            animation_frames = [0,0]
            placed = resolve_placed_string(match_property["Placed"])
            x = random.randint(0,408-138)
            y = random.randint(0,189-138)
            score_font = pygame.font.SysFont("Consolas",55,True)
            buffer_delay = 60
            delay = 0
            menu = False
            option_button = {
                "resume": [743,401,433,81],
                "settings": [743,500,433,81],
                "support": [743,598,433,81],
                "surrender": [743,697,433,81]
            }
            #################################
            game = True
            while game:

                main_clock.tick(FPS)
                #################################
                mouse_pos = pygame.mouse.get_pos()
                screen_size = self.screen_size
                screen_ratio = self.screen_ratio
                #################################
                screen.blit(pygame.transform.scale(self.assets["menu_background"],screen.get_size()),(0,0))
                for b in range(0,len(boards)):
                    for i in range(0,len(box_rects[b])):
                        for j in range(0,len(box_rects[b][i])):
                            box = box_rects[b][i][j]
                            number = boards[b][i][j]
                            screen.blit(adjust_surface(pygame.transform.scale(self.assets["box"],box_size),screen_ratio),adjust_pos((box[0],box[1]),screen_ratio))
                            if number:
                                if i == placed[b][0] and j == placed[b][1] and animation_frames[b] > 0:
                                    temp_ratio = animation_ratio-((animation_ratio-1)/place_animation_frame)*(place_animation_frame-animation_frames[b])
                                    screen.blit(adjust_surface(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[temp_ratio,temp_ratio]),[box_ratio,box_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio*temp_ratio,box[1]+10*box_ratio*temp_ratio),screen_ratio))
                                    animation_frames[b] -= 1
                                    if not animation_frames[b]:
                                        update_LAN_match(address,"Placed",[player,-1])
                                else:
                                    screen.blit(adjust_surface(adjust_surface(self.assets[f"dice {number}"],[box_ratio,box_ratio]),screen_ratio),adjust_pos((box[0]+15*box_ratio,box[1]+10*box_ratio),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"score_box"],screen_ratio),adjust_pos((54,14),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"score_box"],screen_ratio),adjust_pos((1518,844),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"dice_box"],screen_ratio),adjust_pos((15,855),screen_ratio))
                    screen.blit(adjust_surface(self.assets[f"dice_box"],screen_ratio),adjust_pos((1465,17),screen_ratio))
                    if player == 0:
                        score_size = score_font.render(str(match_property["Player 1 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 1 Score"]),True,GRAY),screen_ratio),adjust_pos((1529+(327-score_size[0])/2,924+(132-score_size[1])/2),screen_ratio))
                        score_size = score_font.render(str(match_property["Player 2 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 2 Score"]),True,GRAY),screen_ratio),adjust_pos((65+(327-score_size[0])/2,94+(132-score_size[1])/2),screen_ratio))
                    else:
                        score_size = score_font.render(str(match_property["Player 2 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 2 Score"]),True,GRAY),screen_ratio),adjust_pos((1529+(327-score_size[0])/2,924+(132-score_size[1])/2),screen_ratio))
                        score_size = score_font.render(str(match_property["Player 1 Score"]),True,GRAY).get_size()
                        screen.blit(adjust_surface(score_font.render(str(match_property["Player 1 Score"]),True,GRAY),screen_ratio),adjust_pos((65+(327-score_size[0])/2,94+(132-score_size[1])/2),screen_ratio))
                    if match_property["Turn"] == player:
                        screen.blit(adjust_surface(self.assets[f"dice {match_property["Dice"]}"],screen_ratio),adjust_pos((31+x,864+y),screen_ratio))
                    else:
                        screen.blit(adjust_surface(self.assets[f"dice {match_property["Dice"]}"],screen_ratio),adjust_pos((1481+x,26+y),screen_ratio))
                    if menu:
                        screen.blit(adjust_surface(self.assets[f"option_menu_background"],screen_ratio),adjust_pos((727,293),screen_ratio))
                        for button in [*option_button]:
                            button_rect = adjust_rect(option_button[button],screen_ratio)
                            screen.blit(adjust_surface(self.assets[f"option_{button}"],screen_ratio),button_rect.topleft)
                            if button_rect.collidepoint(mouse_pos):
                                screen.blit(pygame.transform.scale(self.assets[f"overlay_shader"],button_rect.size),button_rect.topleft)
                #################################
                delay += 1
                if delay == buffer_delay:
                    delay = 0
                    match_property = resolve_match_string(get_LAN_match(address))
                    if match_property["Ended"]:
                        game = False
                        return self.end_lan_match(address,player)
                    elif match_property:
                        if player == 0:
                            boards = [resolve_board_string(match_property["Player 1 Board"]),flip_board(resolve_board_string(match_property["Player 2 Board"]))]
                        else:
                            boards = [flip_board(resolve_board_string(match_property["Player 1 Board"])),resolve_board_string(match_property["Player 2 Board"])]
                    placing = resolve_placed_string(match_property["Placed"])
                    for i in range(0,len(placing)):
                        if placing[i] != placed[i] and placed[i] == [-1,-1]:
                            animation_frames[i] = place_animation_frame
                        placed[i] = placing[i]
                
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == VIDEORESIZE:
                        self.screen_size = screen.get_size()
                        self.screen_ratio = [self.screen_size[0]/ScreenWidth,self.screen_size[1]/ScreenHeight]
                        
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if menu:
                                for button in [*option_button]:
                                    rect = adjust_rect(option_button[button],screen_ratio)
                                    if rect.collidepoint(mouse_pos):
                                        if button == "resume":
                                            menu = False
                                        elif button == "settings":
                                            self.settings()
                                        elif button == "support":
                                            pass
                                        elif button == "surrender":
                                            update_LAN_match(address,f"Player {player+1} Score",-999)
                                            end_LAN_match(address)
                            else:
                                for i in range(0,len(box_rects[player])):
                                    for j in range(0,len(box_rects[player][i])):
                                        rect = adjust_rect(box_rects[player][i][j],screen_ratio)
                                        if rect.collidepoint(mouse_pos) and match_property["Turn"] == player:
                                            if not boards[player][i][j]:
                                                update_LAN_match(address,f"Player {player+1} Board",(i,j))
                                                animation_frames[player] = place_animation_frame
                                                placed[player] = [i,j]
                                                x = random.randint(0,408-138)
                                                y = random.randint(0,189-138)
                                                
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            menu = not menu
                            
                pygame.display.flip()
        
    App().menu()


#run game
if __name__ == '__main__':    
    main()