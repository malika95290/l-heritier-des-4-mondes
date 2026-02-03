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
VERT_survol = (46, 204, 113)
BLEU = (41, 128, 185)          
BLEU_survol = (52, 152, 219)   
GRIS = (44, 62, 80)            
GRIS_CLAIR = (52, 73, 94)      
ROUGE = (231, 76, 60)          
ROUGE_survol = (192, 57, 43)

#Création de la police pour les boutons
font_bouton = pygame.font.Font(None, 60)
#Police plus petite pour le texte dans la fenêtre Paramètres
font_param = pygame.font.Font(None, 36)
#Police encore plus petite pour les labels des touches
font_touches = pygame.font.Font(None, 30)

#Classe pour créer un bouton
class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte, couleur, couleur_hover):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.couleur = couleur
        self.couleur_hover = couleur_hover
        self.couleur_actuelle = couleur
    
    def dessiner(self, surface):
        pygame.draw.rect(surface, self.couleur_actuelle, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLANC, self.rect, 3, border_radius=10)
        texte_surface = font_bouton.render(self.texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)
    
    def verifier_survol(self, pos_souris):
        if self.rect.collidepoint(pos_souris):
            self.couleur_actuelle = self.couleur_hover
            return True
        else:
            self.couleur_actuelle = self.couleur
            return False
    
    def est_clique(self, pos_souris):
        return self.rect.collidepoint(pos_souris)

#class pour créér la barre de vollume pour pouvoir augmenter ou diminuer
class BarreVolume:
    def __init__(self, x, y, largeur, hauteur, valeur_initiale=0.5):
        self.rect = pygame.Rect(x, y, largeur, hauteur)  #Rectangle de la barre totale
        self.valeur = valeur_initiale  #Valeur actuelle du volume (entre 0 et 1)
        #Le cercle qu'on glisse : sa taille et sa position
        self.rayon_cercle = 12
        self.x_cercle = x + int(largeur * valeur_initiale)  #Position x du cercle selon la valeur
        self.en_cours_de_glissement = False  #True quand on maintient le clic sur le cercle

    def dessiner(self, surface):
        #dessine la barre grise en arrière-plan (la partie vide)
        pygame.draw.rect(surface, GRIS_CLAIR, self.rect, border_radius=5)
        #Dessine la partie colorée selon la valeur actuelle du volume
        rect_rempli = pygame.Rect(
            self.rect.x,
            self.rect.y,
            int(self.rect.width * self.valeur),  #La largeur dépend de la valeur
            self.rect.height
        )
        pygame.draw.rect(surface, BLEU, rect_rempli, border_radius=5)
        # dessine le cercle qu'on glisse (le "thumb" de la barre)
        pygame.draw.circle(surface, BLANC, (self.x_cercle, self.rect.centery), self.rayon_cercle)

    def gerer_evenement(self, event):
        #gère les clics et le glissement sur la barre
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Si on clique sur le cercle, on commence à glisser
            if pygame.math.Vector2(event.pos).distance_to((self.x_cercle, self.rect.centery)) < self.rayon_cercle + 5:
                self.en_cours_de_glissement = True

        if event.type == pygame.MOUSEBUTTONUP:
            #On arrête de glisser quand on lâche le bouton
            self.en_cours_de_glissement = False

        if event.type == pygame.MOUSEMOTION:
            #Si on est en train de glisser, on met à jour la position du cercle
            if self.en_cours_de_glissement:
                #On limite la position entre le début et la fin de la barre
                self.x_cercle = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                #On calcule la nouvelle valeur du volume (entre 0 et 1)
                self.valeur = (self.x_cercle - self.rect.x) / self.rect.width

    def obtenir_valeur(self):
        #Retourne la valeur actuelle de la barre (entre 0 et 1)
        return self.valeur

#classe pour créer une touche qu'on peut changer
class ToucheParametre:
    def __init__(self, x, y, largeur, hauteur, label, touche_par_defaut):
        """
        label : texte à gauche (ex: "Haut")
        touche_par_defaut : la touche assignée au départ (ex: "UP")
        """
        self.rect = pygame.Rect(x, y, largeur, hauteur)  #Rectangle du bouton de touche
        self.label = label
        self.touche_actuelle = touche_par_defaut  #La touche actuellement assignée
        self.en_attente = False  #True quand on attend une nouvelle touche

    def dessiner(self, surface):
        # couleur du bouton : orange si on attend une touche, sinon gris
        couleur = (230, 126, 34) if self.en_attente else GRIS_CLAIR
        pygame.draw.rect(surface, couleur, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLANC, self.rect, 2, border_radius=5)

        #texte du label à gauche du bouton
        label_surface = font_touches.render(self.label + " :", True, BLANC)
        surface.blit(label_surface, (self.rect.x - 120, self.rect.y + 8))

        # Texte de la touche au centre du bouton (ou "Appuyez..." si on attend)
        texte = "Appuyez..." if self.en_attente else self.touche_actuelle
        texte_surface = font_touches.render(texte, True, BLANC)
        texte_rect = texte_surface.get_rect(center=self.rect.center)
        surface.blit(texte_surface, texte_rect)

    def est_clique(self, pos_souris):
        """Vérifie si on a cliqué sur le bouton de touche"""
        return self.rect.collidepoint(pos_souris)

    def gerer_evenement(self, event):
        """Gère le changement de touche"""
        #Si on est en attente d'une touche et qu'une touche est appuyée
        if self.en_attente and event.type == pygame.KEYDOWN:
            #pygame.key.name() convertit le code de la touche en nom lisible (ex: "up", "space")
            self.touche_actuelle = pygame.key.name(event.key).upper()
            self.en_attente = False

#Création des éléments du menu principal
bouton_jouer = Bouton(450, 280, 300, 80, "JOUER", VERT, VERT_survol)
bouton_paramètres = Bouton(450, 390, 300, 80, "PARAMÈTRES", BLEU, BLEU_survol)

#Création des éléments de la fenêtre Paramètres
#Barre de volume centrée dans la fenêtre de paramètres
barre_volume = BarreVolume(500, 420, 200, 20, valeur_initiale=0.5)

#Bouton "Retour" en bas de la fenêtre Paramètres
bouton_retour = Bouton(470, 470, 260, 60, "RETOUR", ROUGE, ROUGE_survol)

#les 4 touche à modifier
touche_haut    = ToucheParametre(570, 200, 100, 35, "Haut",    "Z")
touche_gauche  = ToucheParametre(570, 290, 100, 35, "Gauche",  "Q")
touche_bas     = ToucheParametre(570, 245, 100, 35, "Bas",     "S")
touche_droite  = ToucheParametre(570, 335, 100, 35, "Droite",  "D")

#Liste pour boucler facilement sur les touches
touches = [touche_haut, touche_bas, touche_gauche, touche_droite]

# Variable pour savoir si la fenêtre Paramètres est ouverte ou non
paramètres_ouvert = False

#Pour définir l'image de fond du menu
fond = pygame.image.load("C://Users//amo95//OneDrive//Bureau//jungle.png")
fond = pygame.transform.scale(fond, (1200, 700))

#fonctions
def lancer_jeu():
    print("Le jeu se lance !")

def dessiner_fenetre_paramètres(surface):
    
    #Création d'une surface semi-transparente pour le fond flou
    # Le fond est déjà affiché derrière, l'overlay assombrit juste dessus
    overlay = pygame.Surface((1200, 700), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  #Noir avec transparence (150/255)
    surface.blit(overlay, (0, 0))

    #Rectangle de la fenêtre Paramètres (centré)
    fenetre_param = pygame.Rect(350, 100, 500, 450)
    pygame.draw.rect(surface, GRIS, fenetre_param, border_radius=15)
    pygame.draw.rect(surface, BLANC, fenetre_param, 3, border_radius=15)

    #titre "PARAMÈTRES" en haut de la fenêtre
    titre = font_bouton.render("PARAMÈTRES", True, BLANC)
    titre_rect = titre.get_rect(center=(600, 140))
    surface.blit(titre, titre_rect)

    #Ligne séparatrice sous le titre
    pygame.draw.line(surface, BLANC, (380, 165), (820, 165), 2)

    #Label "COMMANDES" pour la section des touches
    label_commandes = font_param.render("COMMANDES", True, BLANC)
    surface.blit(label_commandes, (535, 173))

    #Dessine chaque touche
    for touche in touches:
        touche.dessiner(surface)

    #Label "VOLUME" pour la barre de volume
    label_volume = font_param.render("VOLUME", True, BLANC)
    surface.blit(label_volume, (545, 385))

    #Dessine la barre de volume
    barre_volume.dessiner(surface)

    # affiche la valeur du volume en pourcentage à droite de la barre
    pourcentage = font_touches.render(f"{int(barre_volume.obtenir_valeur() * 100)}%", True, BLANC)
    surface.blit(pourcentage, (720, 415))

    #Dessine le bouton Retour
    bouton_retour.dessiner(surface)

#la boucle principale
while True:
    pos_souris = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Si la fenêtre Paramètres est OUVERTE
        if paramètres_ouvert:
            #Gère les événements de la barre de volume
            barre_volume.gerer_evenement(event)

            #Gère les événements des touches
            for touche in touches:
                touche.gerer_evenement(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #Si on clique sur "Retour", on ferme les Paramètres
                if bouton_retour.est_clique(pos_souris):
                    paramètres_ouvert = False

                #Si on clique sur une touche, on la met en mode "attente"
                for touche in touches:
                    if touche.est_clique(pos_souris):
                        #D'abord on désactive toutes les autres touches
                        for t in touches:
                            t.en_attente = False
                        #Puis on active celle qu'on a cliquée
                        touche.en_attente = True

        #Si la fenêtre Paramètres est FERMÉE (menu principal)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bouton_jouer.est_clique(pos_souris):
                    lancer_jeu()
                if bouton_paramètres.est_clique(pos_souris):
                    paramètres_ouvert = True  #Ouvre la fenêtre Paramètres

    #Affichage du fond (toujours dessiné en premier, même en paramètres)
    screen.blit(fond, (0, 0))  # (0, 0) = coin supérieur gauche de la fenêtre

    #Dessine toujours les boutons du menu en arrière-plan
    bouton_jouer.verifier_survol(pos_souris)
    bouton_jouer.dessiner(screen)
    bouton_paramètres.verifier_survol(pos_souris)
    bouton_paramètres.dessiner(screen)

    #Si les Paramètres sont ouverts, on dessine la fenêtre par-dessus
    if paramètres_ouvert:
        dessiner_fenetre_paramètres(screen)
        bouton_retour.verifier_survol(pos_souris)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()