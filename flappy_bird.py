#import
import pygame, random

#init game engine
pygame.init()

#colors
black = (0, 0, 0)
green = (0, 255, 0)
sandy = (212, 181, 129)
yellow = (250, 200, 0)
sky_blue = (135, 206, 235)
white = (255, 255, 255)

#define a screen
size = [640, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy Bird")

#helpers
def load_image(name):
    image = pygame.image.load(name)
    return image
#game standby
pause = False
done = False
score = 0

#set fonts
font = pygame.font.Font(None, 18)

#classes
class Bird(object):

	def __init__(self):
		self.posY = size[1] / 2
		self.velY = 0
		self.image = load_image('img/bird.png')
		self.image = pygame.transform.scale(self.image, (34, 24))

	def move(self):
		self.posY += self.velY
		self.velY += 0.1

	def draw(self):
		screen.blit(self.image, [100,self.posY])
		#pygame.draw.rect(screen, yellow, [100, self.posY, 32,16], 0) 

class Pipe(object):
	def __init__(self, posX):
		self.posX = posX
		self.gate_posY = random.randint(100,300)

	def move(self):
		self.posX -= 2
		if self.posX <= - 120:
			self.posX = 720
			self.gate_posY = random.randint(100,300)

	def draw(self):
		pygame.draw.rect(screen, green, [self.posX, 0, 62, self.gate_posY], 0)
		pygame.draw.rect(screen, green, [self.posX, self.gate_posY + 124, 62, size[1] - self.gate_posY], 0)

#init classes
bird = Bird()
pipes = ( Pipe(720),Pipe(1040),Pipe(1360))

#framerate control
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
while not done and pause == False:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type is pygame.KEYDOWN:
            _ = pygame.key.name(event.key);
            if _ == 'p':
                  pause = True
        if event.type == pygame.QUIT: # close event
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN: #mouseclick
            bird.velY -= 5;
    while pause == True:
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                _ = pygame.key.name(event.key);
                if _ == 'p':
                    pause = False
            if event.type == pygame.QUIT: # close event
                done = True

    #moving characters
    bird.move()

    #bird is off the screen
    if bird.posY > 480 or bird.posY < -16:
    	done = True

    # collision
    for pipe in pipes:
    	pipe.move()
    	if pipe.posX in range (68, 132) and bird.posY < pipe.gate_posY:
    		done = True
    	elif pipe.posX in range(68, 132) and bird.posY > pipe.gate_posY + 108:
    		done = True
        if pipe.posX == 68:
            score += 1


    # draw
    screen.fill(black) 

    #background
    pygame.draw.rect(screen, sky_blue, [0, 0, 640, 480], 0)
    pygame.draw.rect(screen, sandy, [0, 360, 640, 120], 0)

    #bird
    bird.draw()

    #pipes
    for pipe in pipes:
    	pipe.draw()

    #GUI
    if pause == True:
        text = font.render("PAUSE", True, white)
        screen.blit(text, [ size[0] / 2, size[1] / 2])

    #score    
    text = font.render("Your score: " + str(score), True, white)
    screen.blit(text, [ 500, 50]) 
    #screen update
    pygame.display.flip()

    #framerate
    clock.tick(60)

#show score
def final():
    pause = True
    while pause == True:
        text = font.render("Bird has crashed. Your final score: " + str(score), True, white)
        screen.blit(text, [ size[0] / 2, size[1] / 2])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN or event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                pause = False

#on close
pygame.quit()