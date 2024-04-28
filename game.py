import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'

#importing all required modules
import pygame
import random
from player import player
from menu import Menu
from levels import Levels
from paused_screen import Pause
from coin import Coin
from hammer import Hammer
from bomb import Bomb
from key import Key
from settings import Settings
from button import Button

#initializing pygame and music
pygame.init()
pygame.mixer.init()
bgm1='music/bgm1.mp3'
pygame.mixer.music.load(bgm1)
pygame.mixer.music.play(-1,0,500)
Settings=Settings()
bg_img=pygame.transform.scale(pygame.image.load('images/mc.jpg'),(Settings.win_width,Settings.win_height))
muted=False

win=pygame.display.set_mode((Settings.win_width,Settings.win_height))
pygame.display.set_caption("Lost in Hell")

#timer event
TIMEREVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMEREVENT, 1000)

clock=pygame.time.Clock()

#this class is sound button but also handles events due to a bug
class SoundButton():
    #initializing button class with x,y coordinates and image
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.action=False

    #drawing the button and checking for clicks
    def draw(self,win):
        global playing,countdown,menu_open,mus_file
        pos=pygame.mouse.get_pos()
        
        #checking for click and setting action=True if clicked
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(pos):
                    self.action = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if playing and event.type==TIMEREVENT:
                    countdown-=1
                    if countdown==0 or lives==0:
                        
                        playing=False
                        game_lost=True


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                        man.left = False
                elif event.key == pygame.K_RIGHT:
                        man.right = False
                if menu_open and event.key==pygame.K_m:
                    mus_file=input("Enter your music file path: \n")
                    
                    if os.path.isfile(mus_file):
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load(mus_file)
                        pygame.mixer.music.play(-1,0,500)
                    else:
                        print("Sorry! No Such File")
        win.blit(self.image,(self.rect.x,self.rect.y))

lvls=Levels()
lives=Settings.life
eye_taken=False

#algorithm to randomly generate maze using dfs for a given width and height
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]  # Initialize with walls

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height and maze[y][x] == 1

    def backtrack(x, y):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2*dx, y + 2*dy
            if is_valid(nx, ny):
                maze[ny][nx] = 0  # Set cell as path
                maze[y + dy][x + dx] = 0  # Set intermediate cell as path
                backtrack(nx, ny)

    # Start generation from a random cell
    start_x, start_y = 0,0
    maze[start_y][start_x] = 0  # Set starting cell as path
    backtrack(start_x, start_y)

    # Set entrance and exit
    maze[0][0] = 0  # Set entrance as path
    maze[height - 1][width - 1] = 0  # Set exit as path

    return maze

#finding a path in a given maze from a given start to end
def find_path(maze,start,end):
    start = start
    end = end

    def dfs(x, y, path):
        if (x, y) == end:
            return path + [(x, y)]
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in path:
                result = dfs(nx, ny, path + [(x, y)])
                if result:
                    return result
        return None

    return dfs(start[0], start[1], [])

#saving the path to a given file in the required format
def save_path(filename,path):
    updownlist=list()
    for i in range(len(path)-1):
        first=path[i]
        second=path[i+1]
        if second[0]-first[0]==1:
            updownlist.append('R')
        elif second[0]-first[0]==-1:
            updownlist.append('L')
        elif second[1]-first[1]==1:
            updownlist.append('D')
        elif second[1]-first[1]==-1:
            updownlist.append('U')

    with open(filename,'w') as f:
        f.write(str(updownlist))


#generating the maze for level 1 by placing coins,bombs,hammers as desired
def generate_maze1(width,height):

    maze=generate_maze(width,height)
    path=find_path(maze,(0,0),(len(maze)-1,len(maze[0])-1))
    possible_key=list()
    for i in range(len(maze)):
        for j in range (len(maze[i])):
                if maze[i][j]==0 and (j,i) not in path:
                    possible_key.append((i,j))

    
    cho=random.choice(possible_key)
    
    
    path_to_key=find_path(maze,(0,0),(cho[1],cho[0]))
    path_to_end=find_path(maze,(cho[1],cho[0]),(width-1,height-1))
    path_fin=path_to_key+path_to_end
    save_path('path.txt',path_fin)
    maze[cho[0]][cho[1]]=9

    #placing the bomb
    bomb_chose=random.choices(path_fin,k=lives-2)

    for i in bomb_chose:
        maze[i[1]][i[0]]=4

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0 and (j,i) not in path_fin:
                placeBomb=random.choices([0,4],weights=(0.92,0.08))[0]
                if placeBomb==4:
                    maze[i][j]=placeBomb

    #placing coins

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0:
                placeCoin=random.choices([1,0],weights=(0.2,0.8))[0]
                if placeCoin==1:
                    maze[i][j]=2

    #placing hammers
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0:
                placeHammer=random.choices([0,3],weights=(0.98,0.02))[0]
                if placeHammer==3:
                    maze[i][j]=placeHammer
    
    #placing the key out of path
    possible_path=list()
    for i in range(len(maze)):
        for j in range (len(maze[i])):
                if maze[i][j]==0 and (i,j)!=(len(maze),len(maze[i])):
                    possible_path.append((i,j))
    #placing eye
    ey=random.choice(possible_path)
    maze[ey[0]][ey[1]]=5

    
    maze[height-1][width-1]=10
    return maze

#generating maze for level 2 with different probabilities of coins, hammers,etc
def generate_maze2(width,height):

    maze=generate_maze(width,height)
    path=find_path(maze,(0,0),(len(maze)-1,len(maze[0])-1))
    possible_key=list()
    for i in range(len(maze)):
        for j in range (len(maze[i])):
                if maze[i][j]==0 and (j,i) not in path:
                    possible_key.append((i,j))

    
    cho=random.choice(possible_key)
    
    
    path_to_key=find_path(maze,(0,0),(cho[1],cho[0]))
    path_to_end=find_path(maze,(cho[1],cho[0]),(width-1,height-1))
    path_fin=path_to_key+path_to_end
    save_path('path.txt',path_fin)
    maze[cho[0]][cho[1]]=9

    bomb_chose=random.choices(path_fin,k=lives-2)

    for i in bomb_chose:
        maze[i[1]][i[0]]=4

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0 and (j,i) not in path_fin:
                placeBomb=random.choices([0,4],weights=(0.91,0.09))[0]
                if placeBomb==4:
                    maze[i][j]=placeBomb

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0:
                placeCoin=random.choices([1,0],weights=(0.2,0.8))[0]
                if placeCoin==1:
                    maze[i][j]=2
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0:
                placeHammer=random.choices([0,3],weights=(0.98,0.02))[0]
                if placeHammer==3:
                    maze[i][j]=placeHammer
    possible_path=list()
    for i in range(len(maze)):
        for j in range (len(maze[i])):
                if maze[i][j]==0:
                    possible_path.append((i,j))
    #placing eye
    ey=random.choice(possible_path)
    maze[ey[0]][ey[1]]=5

    maze[height-1][width-1]=10

    return maze

#generating maze for level 3
def generate_maze3(width,height):
    maze=generate_maze(width,height)
    path=find_path(maze,(0,0),(len(maze)-1,len(maze[0])-1))
    possible_key=list()
    for i in range(len(maze)):
        for j in range (len(maze[i])):
                if maze[i][j]==0 and (j,i) not in path:
                    possible_key.append((i,j))

    
    cho=random.choice(possible_key)
    
    
    path_to_key=find_path(maze,(0,0),(cho[1],cho[0]))
    path_to_end=find_path(maze,(cho[1],cho[0]),(width-1,height-1))
    path_fin=path_to_key+path_to_end
    save_path('path.txt',path_fin)
    maze[cho[0]][cho[1]]=9

    bomb_chose=random.choices(path_fin,k=lives-1)

    for i in bomb_chose:
        maze[i[1]][i[0]]=4

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0 and (j,i) not in path_fin:
                placeBomb=random.choices([0,4],weights=(0.97,0.03))[0]
                if placeBomb==4:
                    maze[i][j]=placeBomb
    
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0:
                placeCoin=random.choices([1,0],weights=(0.2,0.8))[0]
                if placeCoin==1:
                    maze[i][j]=2

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j]==0:
                placeHammer=random.choices([0,3],weights=(0.99,0.01))[0]
                if placeHammer==3:
                    maze[i][j]=placeHammer

    possible_path=list()
    for i in range(len(maze)):
        for j in range (len(maze[i])):
                if maze[i][j]==0:
                    possible_path.append((i,j))
    #placing eye
    ey=random.choice(possible_path)
    maze[ey[0]][ey[1]]=5

    maze[height-1][width-1]=10
    return maze

    


#checking walls in all directions
def notWall(direction):
            player_pos = (man.x // Settings.TILE_SIZE, man.y // Settings.TILE_SIZE) 
            if direction == 'left' and player_pos[0] > 0:
                return maze_structure[player_pos[1]][player_pos[0] - 1] != 1
            elif direction == 'right' and player_pos[0] < len(maze_structure[0]) - 1:
                return maze_structure[player_pos[1]][player_pos[0] + 1] != 1
            elif direction == 'up' and player_pos[1] > 0:
                return  maze_structure[player_pos[1] - 1][player_pos[0]] != 1
            elif direction == 'down' and player_pos[1] < len(maze_structure) - 1:
                return maze_structure[player_pos[1] + 1][player_pos[0]] != 1
            return False


#rendering some text on screen with given text,font,text-color,and coordinates
def draw_text(text,font,text_col,x,y):
     txt=font.render(text,True,text_col)
     win.blit(txt,(x,y))
     

#initializing the player class
man = player(0, 0,Settings.TILE_SIZE,Settings.TILE_SIZE)

#fonts
header_font=pygame.font.Font("fonts/Curse.ttf",65)
text_font=pygame.font.Font("fonts/HelpMe.ttf",25)
text_font2=pygame.font.Font("fonts/HelpMe.ttf",45)
win_font1=pygame.font.Font("fonts/storm.ttf",50)
win_font2=pygame.font.Font("fonts/storm.ttf",30)

#game_states
lvl_open=False
playing=False
menu_open=True
game_won=False
game_lost=False
high_score_page_open=False
pause_open=False

coins=dict()
hammers=dict()
bombs=dict()
keyes=dict()

totalCoinsCollected=0
score=0
hammer_collected=False
key_collected=False

# drawing game window while playing
def redrawGameWindow():
    global pause_open,playing,muted
    
    win.blit(bg_img,(0,0))
    for i in range(int(lives)):
        win.blit(pygame.transform.scale(pygame.image.load('images/heart.png'),(40,40)),(950+50*i,120))
    for i in range(len(maze_structure)):
        for j in range(len(maze_structure[i])):
            if maze_structure[i][j]==2 and not coins_drawn:
                coins[(i,j)]=Coin(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
            if maze_structure[i][j]==3 and not hammer_drawn:
                hammers[(i,j)]=Hammer(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
            if maze_structure[i][j]==4 and not bomb_drawn:
                bombs[(i,j)]=Bomb(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
            if maze_structure[i][j]==9 and not key_drawn:
                keyes[(i,j)]=Key(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
                
            #showing only a specific area near player
            if (man.y-2*Settings.TILE_SIZE<=i*Settings.TILE_SIZE<=man.y+2*Settings.TILE_SIZE) and (man.x-2*Settings.TILE_SIZE<=j*Settings.TILE_SIZE<=man.x+2*Settings.TILE_SIZE):
                
                if maze_structure[i][j] == 1:
                
                    # Draw a wall
                    win.blit(pygame.transform.scale(pygame.image.load('images/wall.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))

                elif maze_structure[i][j]==2:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    coins[(i,j)].draw(win)
                elif maze_structure[i][j]==3:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    hammers[(i,j)].draw(win)
                elif maze_structure[i][j]==4:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    bombs[(i,j)].draw(win)
                elif maze_structure[i][j]==9:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    
                    keyes[(i,j)].draw(win)
                elif maze_structure[i][j]==10:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    win.blit(pygame.transform.scale(pygame.image.load('images/treasure-chest.png'), (Settings.TILE_SIZE, Settings.TILE_SIZE)),(j * Settings.TILE_SIZE, i * Settings.TILE_SIZE))
                elif maze_structure[i][j]==5:
                    if not eye_taken:
                        pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                        
                        win.blit(pygame.transform.scale(pygame.image.load('images/search.png'), (Settings.TILE_SIZE, Settings.TILE_SIZE)),(j * Settings.TILE_SIZE, i * Settings.TILE_SIZE))
                    else:
                        pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    
                else:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))

            else:
                # Draw an open space
                pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
    

    if hammer_collected:
        win.blit(pygame.transform.scale(pygame.image.load('images/hammer.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(1000,600))
    if key_collected:
        win.blit(pygame.transform.scale(pygame.image.load('images/key.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(1000,700))
    # Draw the player
    man.draw(win)
    

    #draw pause button
    pause_img=pygame.transform.scale(pygame.image.load('images/pause.png'),(60,60))
    pause=Button(1000,20,pause_img)
    pause.draw(win)
    if pause.action:
        pause_open=True
        playing=False

    #draw sound mute button
    if not muted:
        audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
        audio_but=SoundButton(1100,15,audio_img)
        audio_but.draw(win)
        if audio_but.action:
            pygame.mixer.music.pause()
            muted=True

    else:
        mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
        mute_but=SoundButton(1100,15,mute_img)
        mute_but.draw(win)
        if mute_but.action:
            pygame.mixer.music.unpause()
            muted=False
        
    #draw the timer
    if countdown>5:
        pygame.draw.rect(win,"green",pygame.Rect(950,180,170,50))
        draw_text("0."+str(countdown),text_font,"black",1000,200)
    else:
        pygame.draw.rect(win,"red",pygame.Rect(950,180,170,50))
        draw_text("0."+str(countdown),text_font,"black",1000,200)

    #no of coins collected
    win.blit(pygame.transform.scale(pygame.image.load('images/coin.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(1000,390))
    draw_text(str(totalCoinsCollected),text_font,"white",1050,400)
    pygame.display.update()


#animating and adding sound effects for bomb explosion
def bomb_explode(x,y):
    if not muted:
        bomb_music=pygame.mixer.Sound('music/bomb_exp.mp3')
        bomb_music.play()
    bomb_imgs=[]
    for i in range(1,14):
        img=pygame.transform.scale(pygame.image.load(f"images/bomb_explode/{i}.png"),(Settings.TILE_SIZE,Settings.TILE_SIZE))
        bomb_imgs.append(img)
    
    img_no=0
    exp_clk=pygame.time.Clock()
    while(img_no<13):
        exp_clk.tick(13)
        win.blit(bomb_imgs[img_no],(x,y))
        img_no+=1
        pygame.display.update()


#checking for a high score and updating in the high score file
def check_high_score(score):

    global highest_score
    highest_score=False
    scores=list()
    with open('.high_scores.txt', 'r+') as hs_file:
        
        hs_file.seek(0) 
        for line in hs_file:
            scores.append(int(line.strip()))  
        if not scores or score >= max(scores):
            highest_score = True
        scores.append(score)
        scores.sort(reverse=True)
        scores = scores[:5]  
        hs_file.seek(0)  
        for s in scores:
            hs_file.write(str(s) + '\n') 
        hs_file.truncate()  

    
#showing the complete maze for 1.5s when eye acquired by using redrawGameWindow without hiding 
def showMaze():
    global pause_open,playing,muted
    for i in range(2):
        
        win.blit(bg_img,(0,0))
        for i in range(int(lives)):
            win.blit(pygame.transform.scale(pygame.image.load('images/heart.png'),(40,40)),(950+50*i,120))
        for i in range(len(maze_structure)):
            for j in range(len(maze_structure[i])):
                if maze_structure[i][j]==2 and not coins_drawn:
                    coins[(i,j)]=Coin(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
                if maze_structure[i][j]==3 and not hammer_drawn:
                    hammers[(i,j)]=Hammer(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
                if maze_structure[i][j]==4 and not bomb_drawn:
                    bombs[(i,j)]=Bomb(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
                if maze_structure[i][j]==9 and not key_drawn:
                    keyes[(i,j)]=Key(j*Settings.TILE_SIZE,i*Settings.TILE_SIZE)
                    
            
                    
                if maze_structure[i][j] == 1:
                
                    # Draw a wall
                    win.blit(pygame.transform.scale(pygame.image.load('images/wall.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))

                elif maze_structure[i][j]==2:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    coins[(i,j)].draw(win)
                elif maze_structure[i][j]==3:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    hammers[(i,j)].draw(win)
                elif maze_structure[i][j]==4:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    bombs[(i,j)].draw(win)
                elif maze_structure[i][j]==9:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    
                    keyes[(i,j)].draw(win)
                elif maze_structure[i][j]==10:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    win.blit(pygame.transform.scale(pygame.image.load('images/treasure-chest.png'), (Settings.TILE_SIZE, Settings.TILE_SIZE)),(j * Settings.TILE_SIZE, i * Settings.TILE_SIZE))
                elif maze_structure[i][j]==5:
                    if not eye_taken:
                        pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                        
                        win.blit(pygame.transform.scale(pygame.image.load('images/search.png'), (Settings.TILE_SIZE, Settings.TILE_SIZE)),(j * Settings.TILE_SIZE, i * Settings.TILE_SIZE))
                    else:
                        pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
                    
                else:
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))

            else:
                    # Draw an open space
                    pygame.draw.rect(win, (0, 0, 0), (j * Settings.TILE_SIZE, i * Settings.TILE_SIZE, Settings.TILE_SIZE, Settings.TILE_SIZE))
        

        if hammer_collected:
            win.blit(pygame.transform.scale(pygame.image.load('images/hammer.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(1000,600))
        if key_collected:
            win.blit(pygame.transform.scale(pygame.image.load('images/key.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(1000,700))
        # Draw the player
        man.draw(win)
        

        #draw pause button
        pause_img=pygame.transform.scale(pygame.image.load('images/pause.png'),(60,60))
        pause=Button(1000,20,pause_img)
        pause.draw(win)
        if pause.action:
            pause_open=True
            playing=False

        #draw sound mute button
        if not muted:
            audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
            audio_but=SoundButton(1100,15,audio_img)
            audio_but.draw(win)
            if audio_but.action:
                pygame.mixer.music.pause()
                muted=True

        else:
            mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
            mute_but=SoundButton(1100,15,mute_img)
            mute_but.draw(win)
            if mute_but.action:
                pygame.mixer.music.unpause()
                muted=False
            
        #draw the timer
        if countdown>5:
            pygame.draw.rect(win,"green",pygame.Rect(950,180,170,50))
            draw_text("0."+str(countdown),text_font,"white",1000,200)
        else:
            pygame.draw.rect(win,"red",pygame.Rect(950,180,170,50))
            draw_text("0."+str(countdown),text_font,"white",1000,200)

        #no of coins collected
        win.blit(pygame.transform.scale(pygame.image.load('images/coin.png'),(Settings.TILE_SIZE,Settings.TILE_SIZE)),(1000,390))
        draw_text(str(totalCoinsCollected),text_font,"white",1050,400)
        pygame.display.update()
        pygame.time.delay(500)


#variables to determine collection of powerups and some functionalities
run=True
maze_drawn=False
coins_drawn=False
hammer_drawn=False
bomb_drawn=False
key_drawn=False
win_open=True

#function to reset all varibles changed during game execution when game is played again
def reset():
     global man,maze_structure,maze_drawn,totalCoinsCollected,coins_drawn,hammer_collected,hammer_drawn,coins,hammers,bombs,keyes,bomb_drawn,lives,key_drawn,key_collected,highest_score,win_open,eye_taken
     lvls.act=False
     lvls.back=False
     keyes=dict()
     coins=dict()
     bombs=dict()
     hammers=dict()
     man = player(0, 0, Settings.TILE_SIZE,Settings.TILE_SIZE)
     maze_drawn=False
     totalCoinsCollected=0
     key_drawn=False
     coins_drawn=False
     hammer_collected=False
     hammer_drawn=False
     bomb_drawn=False
     lives=Settings.life
     key_collected=False
     highest_score=False
     win_open=True
     eye_taken=False


#the main run loop
while(run):
        
        win.fill((122,73,3))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #if the game is actually played
        if playing:
            clock.tick(27)
            pygame.time.delay(80)
            #draw maze according to level
            if maze_drawn==False:
                if lvls.level==1: 
                    countdown=Settings.countdown1
                    maze_structure=generate_maze1(15,15)
                    maze_drawn=True
                    
                if lvls.level==2:
                    countdown=Settings.countdown2
                    maze_structure=generate_maze2(21,21)
                    maze_drawn=True
                    
                if lvls.level==3:
                    countdown=Settings.countdown3
                    maze_structure=generate_maze3(25,25)
                    maze_drawn=True
                
            
            
                
            redrawGameWindow()
                
            #check for key presses and move accordingly avoiding collision with walls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and man.x>0 and notWall('left'):
                man.x -= man.vel
                man.left = True
                man.right = False
            elif keys[pygame.K_RIGHT] and man.x < (len(maze_structure)-1)*Settings.TILE_SIZE and notWall('right') :
                man.x += man.vel
                man.right = True
                man.left = False
                        
            elif keys[pygame.K_UP] and man.y>0 and notWall('up'):
                man.y-=man.vel
                man.right = False
                man.left = False
                man.walkCount =0
            elif keys[pygame.K_DOWN] and man.y< (len(maze_structure)-1)*Settings.TILE_SIZE and notWall('down'):
                man.y+=man.vel
                man.right = False
                man.left = False
                man.walkCount = 0

            #implementing hammer functions                
            elif keys[pygame.K_DOWN] and keys[pygame.K_SPACE] and hammer_collected==True and man.y<(len(maze_structure)-1)*Settings.TILE_SIZE:
                if maze_structure[(man.y//Settings.TILE_SIZE)+1][man.x//Settings.TILE_SIZE]==1:
                    maze_structure[man.y//Settings.TILE_SIZE+1][man.x//Settings.TILE_SIZE]=0
                    hammer_collected=False

            elif keys[pygame.K_UP] and keys[pygame.K_SPACE] and hammer_collected==True and man.y>0:
                if maze_structure[man.y//Settings.TILE_SIZE-1][man.x//Settings.TILE_SIZE]==1:
                    maze_structure[man.y//Settings.TILE_SIZE-1][man.x//Settings.TILE_SIZE]=0
                hammer_collected=False

            elif keys[pygame.K_LEFT] and keys[pygame.K_SPACE] and hammer_collected==True and man.x>0:
                if maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE-1]==1:
                    maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE-1]=0
                hammer_collected=False

            elif keys[pygame.K_RIGHT] and keys[pygame.K_SPACE] and hammer_collected==True and man.x<(len(maze_structure)-1)*Settings.TILE_SIZE:
                if maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE+1]==1:
                    maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE+1]=0
                hammer_collected=False

            #implementing coins collection
            if maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE]==2 and coins[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken==False:
                coins[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken=True
                coin_mus=pygame.mixer.Sound('music/coin.mp3')
                redrawGameWindow()
                if not muted:
                    coin_mus.play()
                totalCoinsCollected+=1

            #hammer collection
            if maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE]==3 and hammers[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken==False:
                hammers[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken=True
                hammer_collected=True

            #key collection
            if maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE]==9 and keyes[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken==False:
                keyes[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken=True
                key_collected=True

            #bomb collision
            if maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE]==4 and bombs[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken==False:
                bombs[(man.y//Settings.TILE_SIZE,man.x//Settings.TILE_SIZE)].taken=True
                lives-=1
                redrawGameWindow()
                bomb_explode(man.x,man.y)
            if maze_structure[man.y//Settings.TILE_SIZE][man.x//Settings.TILE_SIZE]==5 and eye_taken==False:
                eye_taken=True
                showMaze()

            #winning the game if condition is fulfilled
            if man.x==(len(maze_structure)-1)*Settings.TILE_SIZE and man.y==(len(maze_structure)-1)*Settings.TILE_SIZE and key_collected:
                pygame.time.delay(150)
                win_mus=pygame.mixer.Sound('music/win.mp3')
                if not muted:
                    win_mus.play()
                playing=False  
                game_won=True   
            if lives==0:
                playing=False
                game_lost=True
            coins_drawn=True
            hammer_drawn=True
            bomb_drawn=True
            key_drawn=True

        #if main menu is open    
        if menu_open==True:
            menu=Menu()
            menu.open_menu(win)
            draw_text("LOST IN HELL",header_font,(237,188,74),425,50)
            draw_text("Dont't like the music?",text_font,(237,188,74),800,900)
            draw_text("Press M to change it",text_font,(237,188,74),800,930)  
            if menu.playing==True:
                lvl_open=True
                menu_open=False
            elif menu.q==True:
                run=False
                pygame.quit()
                break
            elif menu.hs==True:
                menu_open=False
                high_score_page_open=True
                #draw sound mute button
            if not muted:
                audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
                audio_but=SoundButton(1100,15,audio_img)
                audio_but.draw(win)
                if audio_but.action:
                    pygame.mixer.music.pause()
                    muted=True

            else:
                mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
                mute_but=SoundButton(1100,15,mute_img)
                mute_but.draw(win)
                if mute_but.action:
                    pygame.mixer.music.unpause()
                    muted=False

        #if level selection screen is open
        elif lvl_open==True:
            reset()
            lvls.lvl_screen(win)
            draw_text("LEVEL",header_font,(237,188,74),520,200)
            if lvls.act:
                 playing=True
                 lvl_open=False
            if lvls.back:
                lvl_open=False
                menu_open=True
                #draw sound mute button
            if not muted:
                audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
                audio_but=SoundButton(1100,15,audio_img)
                audio_but.draw(win)
                if audio_but.action:
                    pygame.mixer.music.pause()
                    muted=True

            else:
                mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
                mute_but=SoundButton(1100,15,mute_img)
                mute_but.draw(win)
                if mute_but.action:
                    pygame.mixer.music.unpause()
                    muted=False

        #if high scores page is open
        elif high_score_page_open==True:
            win.blit(bg_img,(0,0))
            draw_text("HIGH SCORES",text_font2,"white",450,200)
            h_scores=list()
            with open('.high_scores.txt', 'r+') as hs_file:
                hs_file.seek(0) 
                for line in hs_file:
                    h_scores.append(int(line.strip()))  
                for i in range(len(h_scores)):
                    draw_text(str(h_scores[i]),text_font2,"white",560,300+80*i)
            back_img=pygame.transform.scale(pygame.image.load('images/back.png'),(100,100))
            back_but=Button(20,20,back_img)
            back_but.draw(win)
            if back_but.action:
                high_score_page_open=False
                menu_open=True
                #draw sound mute button
            if not muted:
                audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
                audio_but=SoundButton(1100,15,audio_img)
                audio_but.draw(win)
                if audio_but.action:
                    pygame.mixer.music.pause()
                    muted=True

            else:
                mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
                mute_but=SoundButton(1100,15,mute_img)
                mute_but.draw(win)
                if mute_but.action:
                    pygame.mixer.music.unpause()
                    muted=False
        
        #if game winning screen is open
        elif game_won==True:
            score=totalCoinsCollected+lives*3+countdown*2
            if win_open:
                check_high_score(score)
                win_open=False
            win_img=pygame.transform.scale(pygame.image.load('images/exit.jpeg'),(Settings.win_width,Settings.win_height))
            win.blit(win_img,(0,0))
            draw_text("Congratulations",win_font1,(250,151,62),450,220)
            draw_text("Score: ",win_font1,(181,27,16),510,440)
            draw_text(str(score),text_font2,(181,27,16),660,450)
            draw_text("Press space to play again",win_font2,(117,66,245),490,550)
            draw_text("Press M for main menu",win_font2,(117,66,245),500,600)
            if highest_score:
                draw_text("High Score",win_font1,(10,89,105),510,320)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_won=False
                lvl_open=True
                reset()
            elif keys[pygame.K_m]:
                game_won=False
                menu_open=True
                reset()
                #draw sound mute button
            if not muted:
                audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
                audio_but=SoundButton(1100,15,audio_img)
                audio_but.draw(win)
                if audio_but.action:
                    pygame.mixer.music.pause()
                    muted=True

            else:
                mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
                mute_but=SoundButton(1100,15,mute_img)
                mute_but.draw(win)
                if mute_but.action:
                    pygame.mixer.music.unpause()
                    muted=False

        #if paused screen is open
        elif pause_open:
            pause_sc=Pause()
            pause_sc.pause_game(win)
            if pause_sc.playing:
                playing=True
                pause_open=False
            elif pause_sc.op_menu:
                pause_open=False
                menu_open=True
                reset()
            elif pause_sc.rest:
                pause_open=False
                reset()
                playing=True
                #draw sound mute button
            if not muted:
                audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
                audio_but=SoundButton(1100,15,audio_img)
                audio_but.draw(win)
                if audio_but.action:
                    pygame.mixer.music.pause()
                    muted=True

            else:
                mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
                mute_but=SoundButton(1100,15,mute_img)
                mute_but.draw(win)
                if mute_but.action:
                    pygame.mixer.music.unpause()
                    muted=False

        #if game losing screen is open
        elif game_lost==True:
            los_img=pygame.transform.scale(pygame.image.load('images/entry.jpg'),(Settings.win_width,Settings.win_height))
            win.blit(los_img,(0,0))
            draw_text("press space to play again",text_font,(235,150,228),450,450)
            draw_text("GAME OVER",text_font2,(237,196,100),500,320)
            draw_text("Press M for main menu",text_font,(235,150,228),450,510)
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_lost=False
                lvl_open=True
                reset()
            elif keys[pygame.K_m]:
                game_lost=False
                menu_open=True
                reset()
                #draw sound mute button
            if not muted:
                audio_img=pygame.transform.scale(pygame.image.load('images/audio.png'),(60,60))
                audio_but=SoundButton(1100,15,audio_img)
                audio_but.draw(win)
                if audio_but.action:
                    pygame.mixer.music.pause()
                    muted=True

            else:
                mute_img=pygame.transform.scale(pygame.image.load('images/mute.png'),(60,60))
                mute_but=SoundButton(1100,15,mute_img)
                mute_but.draw(win)
                if mute_but.action:
                    pygame.mixer.music.unpause()
                    muted=False
        
        pygame.display.update()

#quitting the pygame window
pygame.quit()