import pygame
#Pour lancer pygame
pygame.init()

#Création de la fenêtre
screen = pygame.display.set_mode((1200, 700))
pygame.display.set_caption("Menu du Jeu")  # Titre de la fenêtre
clock = pygame.time.Clock()

#Définition des couleurs (RGB)
NOIR = (25, 25, 30)
BLANC = (255, 255, 255)
VERT = (39, 174, 96)
VERT_HOVER = (46, 204, 113)  # Vert plus clair pour le survol

#Création de la police pour le bouton
font_bouton = pygame.font.Font(None, 60)  # None = police par défaut, 60 = taille

#Classe pour créer un bouton
class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur, couleur_hover):
        
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_hover = couleur_hover
        self.couleur_actuelle = couleur
    
    def dessiner(self, surface):
        #Dessine le rectangle du bouton
        pygame.draw.rect(surface, self.couleur_actuelle, self.rect, border_radius=10)
        #Dessine le contour du bouton
        pygame.draw.rect(surface, BLANC, self.rect, 3, border_radius=10)
        
        #Créé le texte du bouton
        texte_surface = font_bouton.render(self.texte, True, BLANC)
        #Pour centrer le texte du bouton
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        #affiche le texte
        surface.blit(texte_surface, texte_rect)
    
    def verifier_survol(self, pos_souris):
        #Vérifie si la souris survole le bouton et change la couleur
        if self.rect.collidepoint(pos_souris):
            self.couleur_actuelle = self.couleur_hover
            return True
        else:
            self.couleur_actuelle = self.couleur
            return False
    
    def est_clique(self, pos_souris):
        #Vérifie si le bouton a été cliqué
        return self.rect.collidepoint(pos_souris)

#Fonction appelée quand on clique sur "Jouer"
def lancer_jeu():
    print("Le jeu se lance !")
    # mettre le code du jeu quand on l'aura codé comme la fonction qui démarre le premier niveau ou l'histoire si on la met comme intro


bouton_jouer = Bouton(450, 310, 300, 80, "JOUER", VERT, VERT_HOVER)

#la boucle principale du jeu
running = True
while running:
    #récupere la position de la souris
    pos_souris = pygame.mouse.get_pos()
    
    #Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #Détection du clic de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                #Vérifie si on a cliqué sur le bouton "Jouer"
                if bouton_jouer.est_clique(pos_souris):
                    lancer_jeu()
    
    #Efface l'écran avec la couleur de fond
    screen.fill(NOIR)
    
    #Vérifie si la souris survole le bouton (pour l'effet de survol)
    bouton_jouer.verifier_survol(pos_souris)
    
    #Dessine le bouton sur l'écran
    bouton_jouer.dessiner(screen)
    
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()