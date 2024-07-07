#This code aims to recreate the ping pong game. It is inspired from Anthony's game
# The ping pong ball goes in very random directions when starting and after being hit
# The scorebaord also features a current streak and longest streak counter. The only issue is that if you hit the top or bottom of the paddle the 'streak' counter treats it as many hits. 
# Can't believe I managed to code this!! omg   5/7/2024
import pygame, random 
pygame.init()


# Setting the working directory
import os
os.chdir('') #update with your working directory

# Create our display surface
width=800
height=800
display_surface=pygame.display.set_mode((width,height))
pygame.display.set_caption("Ping Pong!")

#Set Frames per seconnd and clock. Means the code isn't run as fast as the computer allows. The while loop will be run at most 60 times (the FPS) per second. 
FPS=60
clock=pygame.time.Clock()

#Game values 
velocity=5      #this is the paddle speed 
x_velocity=2 #starting x velocity for the ball
y_velocity=4 #starting y velocity for the ball
left_score=0
right_score=0
current_streak=0
longest_streak=0
best_of=5 #ie first to what score

# Load sound effects 
pong=pygame.mixer.Sound('pong.wav')

#Loading fonts
system_font=pygame.font.SysFont('candara', 143)
system_font_small=pygame.font.SysFont('candara', 23)


#Scoring Text 
left_points=system_font.render("{}".format(left_score), True, (255,255,255))
left_points_rect=left_points.get_rect()
left_points_rect.center=(width//4,height//2-340)   

right_points=system_font.render("{}".format(right_score), True, (255,255,255))
right_points_rect=right_points.get_rect()
right_points_rect.center=((width*0.75),height//2-340)   

#streaks text
streak=system_font_small.render("Current Streak: {}".format(current_streak), True, (255,255,255))
streak_rect=streak.get_rect()
streak_rect.center=(width//4, height//2-270)

long_streak=system_font_small.render("Longest Streak: {}".format(longest_streak), True, (255,255,255))
long_streak_rect=long_streak.get_rect()
long_streak_rect.center=(width*0.75, height//2-270)

#Replay text 
replay_text=system_font_small.render("Press any key to play again", True, (255,255,255))
replay_text_rect=replay_text.get_rect()
replay_text_rect.center=(width//2,height//2+200)

#Load in images
paddle_1=pygame.image.load("rectangle.png")        #yes this is just a snipping tool rectangle of white space
paddle_2=pygame.image.load("rectangle.png")        #yes these are identical
ball=pygame.image.load("ping_pong_ball.png")

#resizing images
new_size=(25,100)      #can change this to alter the paddle size
paddle_2=pygame.transform.scale(paddle_1,new_size)  #left paddle
paddle_1=pygame.transform.scale(paddle_2,new_size) #right paddle
ball_size=(20,20)
ball=pygame.transform.scale(ball,ball_size)


#the rects of the rectangles lol
paddle_1_rect=paddle_1.get_rect()                  #getting the rects (ie rectangles) for the rectangles haha
paddle_2_rect=paddle_2.get_rect()
ball_rect=ball.get_rect()
paddle_1_rect.center=(30,height//2)     #trying to position them in the middle left and middle right. 
paddle_2_rect.center=(770,height//2)
ball_rect.center=(width//2,height//2)

# I was thinking about being lazy copying a dashed line in but I will try and create the dashed line using the class function to duplicate rectangles. 
class dash(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()      #The Super class is our sprite class. The sprite class does not need any parameter to be initialised. 
        self.image=pygame.image.load("rectangle.png")
        self.rect=self.image.get_rect()
        self.image=pygame.transform.scale(self.image,(9,20))       #re size images to be size 80 pixels by 80 pixels
        self.rect.center=(x,y)   #ie the x and y coordinate that were passed in

#Create a dashed line group and added in the dashes
dashed_group=pygame.sprite.Group()          #now we have a group we can add Sprites too
for i in range(40):
    dashed_line=dash(width//2+12, 40*i)  #I'm a bit unsure about why I need the +12 but it doesn't quite center automatically. 
    dashed_group.add(dashed_line)       #This adds the dashed line to the group
#omg this actually worked crying tears omg 


#The main game loop
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    
    #Get a list of all keys currently being held.
    keys=pygame.key.get_pressed()

    #Move the left paddle
    if (keys[pygame.K_w]) and paddle_1_rect.top>0:
        paddle_1_rect.y -=velocity
    if (keys[pygame.K_s]) and paddle_1_rect.bottom<height:
        paddle_1_rect.y +=velocity
    
    #Move the right paddle
    if (keys[pygame.K_UP]) and paddle_2_rect.top>0:
        paddle_2_rect.y -=velocity
    if (keys[pygame.K_DOWN]) and paddle_2_rect.bottom<height:
        paddle_2_rect.y +=velocity

    #move the ball hits the wall
    ball_rect.y+=y_velocity #the first term determines if the ball travels up or down. The second term determines the speed.
    ball_rect.x+=x_velocity #the first term determine if the ball will move left or right. 

    #determine if the
    if ball_rect.y>height or ball_rect.y<0:
        y_velocity=-1*y_velocity     #so the direction of travel changes
        pong.play()

    # Detect Collision with paddle and change the balls trajectory. 
    if ball_rect.colliderect(paddle_2_rect):   #the input is the rect you are aiming to detect a collision with. IF you change the order it should work just the same.
        current_streak+=1
        x_velocity=random.choice([-2,-4])
        pong.play()
    if ball_rect.colliderect(paddle_2_rect) and ball_rect.top>400:     #so if it is in the top half of the screen, the next direction should be downward
        y_velocity=random.choice([-6,-3])
    if ball_rect.colliderect(paddle_2_rect) and ball_rect.top<400:     #if it is the bottom half of the screen, the next direction should be upward
        y_velocity=random.choice([3,6])
    

    if ball_rect.colliderect(paddle_1_rect):   #the input is the rect you are aiming to detect a collision with. IF you change the order it should work just the same.
        current_streak+=1
        x_velocity=random.choice([2,4])
        pong.play()
    if ball_rect.colliderect(paddle_2_rect) and ball_rect.top>400:   #so if it is in the top half of the screen, the next direction should be downward
        y_velocity=random.choice([-6,-3])
    if ball_rect.colliderect(paddle_2_rect) and ball_rect.top<400:     #if it is the bottom half of the screen, the next direction should be upward
        y_velocity=random.choice([3,6])

    
    #Update the longest streak if it is surpassed
    if current_streak>=longest_streak:
        longest_streak=current_streak


    #Determining a miss
    if ball_rect.x>width:
        left_score+=1
        ball_rect.center=(width//2,height//2)
        x_velocity=random.choice([-1,1])*random.randrange(2,4)  #the first -1 or 1 value determines if we are going left or right
        y_velocity=random.choice([-1,1])*random.randrange(3,6)  #the first -1 or 1 value determines if we are going up or down
        current_streak=0 #reset the current streak

    if ball_rect.x<0:
        right_score+=1
        ball_rect.center=(width//2,height//2)
        x_velocity=random.choice([-1,1])*random.randrange(2,4)  #the first -1 or 1 value determines if we are going left or right
        y_velocity=random.choice([-1,1])*random.randrange(3,6)  #the first -1 or 1 value determines if we are going up or down
        current_streak=0 #reset the current streak

#Determining for right

    if right_score==5:
        right_wins=system_font_small.render("Right Wins", True, (251,251,251))
        right_wins_rect=right_wins.get_rect()
        right_wins_rect.center=(width*0.75,height//2)
        display_surface.blit(right_wins, right_wins_rect)   #blit the game over text
        display_surface.blit(replay_text,replay_text_rect)     #blit the click to play again text 
        pygame.display.update()
        rest=True

        while rest:
            for event in pygame.event.get():
                if  event.type==pygame.KEYDOWN:   #so look to detect if there is a key being pressed 
                    velocity=5      #this is the paddle speed 
                    x_velocity=2
                    y_velocity=4
                    left_score=0
                    right_score=0
                    current_streak=0
                    longest_streak=0
                    best_of=5 #ie first to what score
                    rest=False   #rest is over
                
                #Give the player to option to leave the game
                if event.type==pygame.QUIT:
                    running=False

# Determining game over for left
    if left_score==5:
        left_wins=system_font_small.render("Left Wins", True, (251,251,251))
        left_wins_rect=left_wins.get_rect()
        left_wins_rect.center=(width//4,height//2)
        display_surface.blit(left_wins, left_wins_rect)   #blit the game over text
        display_surface.blit(replay_text,replay_text_rect)     #blit the click to play again text 
        pygame.display.update()
        rest=True

        while rest:
            for event in pygame.event.get():
                if  event.type==pygame.KEYDOWN:   #so look to detect if there is a key being pressed 
                    velocity=5      #this is the paddle speed 
                    x_velocity=2
                    y_velocity=4
                    left_score=0
                    right_score=0
                    current_streak=0
                    longest_streak=0
                    best_of=5 #ie first to what score
                    rest=False   #rest is over
                
                #Give the player to option to leave the game
                if event.type==pygame.QUIT:
                    running=False 

    #Fill the display
    display_surface.fill((236,198,230))

    #Update and Draw the dashed lines (ie the center line)
    dashed_group.update()  
    dashed_group.draw(display_surface)

    #Need to re render score and streak as they have changed values
    left_points=system_font.render("{}".format(left_score), True, (255,255,255))
    right_points=system_font.render("{}".format(right_score), True, (255,255,255))
    streak=system_font_small.render("Current Streak: {}".format(current_streak), True, (255,255,255))
    long_streak=system_font_small.render("Longest Streak: {}".format(longest_streak), True, (255,255,255))


    #blit assets
    display_surface.blit(paddle_1,paddle_1_rect) #blitting paddle 1
    display_surface.blit(paddle_2,paddle_2_rect) #blitting paddle 2
    display_surface.blit(ball, ball_rect)

    #Blitting text to the display
    display_surface.blit(left_points,left_points_rect) #left score
    display_surface.blit(right_points, right_points_rect)  #right score
    display_surface.blit(streak, streak_rect)
    display_surface.blit(long_streak, long_streak_rect)
    #update display
    pygame.display.update() #This line is critical 

    #Tick the clock
    clock.tick(FPS)  #this ensures that the frames per second is not at the computers computational max.

#End the game
pygame.quit()
