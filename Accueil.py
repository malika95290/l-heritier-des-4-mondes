import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((25, 25, 30)) # Efface l'ecran
    pygame.display.flip() #Affiche la frame 
    clock.tick(60) #Limite la vitesse (FPS)

pygame.quit()