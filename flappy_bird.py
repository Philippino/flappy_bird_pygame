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
font = pygame.font.Font(None, 24)

#classes

#class Bird
class Bird(object):

	def __init__(self):
		self.posY = size[1] / 2
		self.velY = 0
        self.index = 0
        self.assets = [load_image('img/bird.png'), load_image('img/bird_flap_1.png'), load_image('img/bird_flap_2.png'), load_image('img/bird_flap_1.png'),load_image('img/bird.png')]
        for i in range(len(self.assets)):
            self.assets[i] = pygame.transform.scale(self.assets[i], (34, 24))
        self.image = self.assets[self.index]

	def move(self):
		self.posY += self.velY
		self.velY += 0.1
		#self.rotate(0.1)

	def rotate(self, angle):
		self.image = pygame.transform.rotate(self.image, angle)

    def flap(self):
        self.index = 4

	def draw(self):
        self.image = self.assets[self.index]
		screen.blit(self.image, [100,self.posY])

#clas Pipe
class Pipe(object):
	def __init__(self, posX):
		self.posX = posX
		self.gate_posY = random.randint(50,350)

	def move(self):
		self.posX -= 4
		if self.posX <= - 120:
			self.posX = 960
			self.gate_posY = random.randint(50,350)

	def draw(self):
		pygame.draw.rect(screen, green, [self.posX, 0, 60, self.gate_posY], 0)
		pygame.draw.rect(screen, green, [self.posX, self.gate_posY + 124, 60, size[1] - self.gate_posY], 0)

#init classes
bird = Bird()
pipes = (Pipe(640), Pipe(960), Pipe(1280))

#framerate control
clock = pygame.time.Clock()

#show score on end
def final():
    global pause, done, score
    pause = True
    while pause == True:
        text = font.render("Bird has crashed. Your final score: " + str(score), True, white)
        screen.blit(text, [ size[0] / 2, size[1] / 2])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN or event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                pause = False

#pause loop
def paused():
    global pause, done
    for event in pygame.event.get():
        if event.type is pygame.KEYDOWN:
            _ = pygame.key.name(event.key);
            if _ == 'space':
                pause = False
            if event.type == pygame.QUIT: # close event
                pause = False
                done = True

    text = font.render("PAUSE", True, white)
    screen.blit(text, [ size[0] / 2, size[1] / 2])
    pygame.display.flip()

#main game loop
def main_loop():
    global done, pause, score
    while not done:
        for event in pygame.event.get():
            if event.type is pygame.KEYDOWN:
                _ = pygame.key.name(event.key);
                if _ == 'space':
                    pause = True
            if event.type == pygame.QUIT: # close event
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN: #mouseclick
                bird.velY -= 5
                bird.flap()

        while pause == True:
            paused()

        #moving characters
        bird.move()

        #bird is off the screen
        if bird.posY > 480 or bird.posY < -16:
    	   done = True
           final()

        # collision
        for pipe in pipes:
    	    pipe.move()
    	    if pipe.posX in range (68, 132) and bird.posY <= pipe.gate_posY:
    	        done = True
                final()
    	    elif pipe.posX in range(68, 132) and bird.posY >= pipe.gate_posY + 108:
                done = True
                final()
            if pipe.posX == 68:
                score += 1


        # draw
        screen.fill(black) 

        #background
        pygame.draw.rect(screen, sky_blue, [0, 0, 640, 480], 0)
        pygame.draw.rect(screen, sandy, [0, 360, 640, 120], 0)

        #bird
        if bird.index != 0:
            bird.index -= 1
        bird.draw()

        #pipes
        for pipe in pipes:
    	   pipe.draw()

        #score    
        text = font.render("Your score: " + str(score), True, white)
        screen.blit(text, [ 500, 50]) 
        #screen update
        pygame.display.flip()

        #framerate
        clock.tick(60)

main_loop()
#on close
pygame.quit()