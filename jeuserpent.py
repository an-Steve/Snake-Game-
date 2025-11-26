import pygame
import random

# ------------------ Initialisation ------------------
pygame.init()

# ------------------ Couleurs ------------------
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (213, 50, 80)
VERT = (0, 255, 0)
BLEU = (50, 153, 213)
VERT_FONCE = (0, 100, 0)
VERT_CLAIR = (0, 150, 0)
GRIS_FONCE = (40, 40, 40)

# Thèmes de couleurs pour le décor
THEMES_DECOR = [
    {"nom": "Herbe", "fonce": (0, 100, 0), "clair": (0, 150, 0)},
    {"nom": "Sable", "fonce": (194, 178, 128), "clair": (238, 214, 175)},
    {"nom": "Océan", "fonce": (0, 105, 148), "clair": (0, 150, 200)},
    {"nom": "Lave", "fonce": (139, 0, 0), "clair": (255, 69, 0)},
    {"nom": "Neige", "fonce": (200, 200, 210), "clair": (240, 240, 255)},
    {"nom": "Nuit", "fonce": (25, 25, 50), "clair": (50, 50, 80)},
]

# ------------------ Dimensions ------------------
LARGEUR = 600
HAUTEUR = 400
TAILLE_BLOC = 20

# ------------------ Fenêtre ------------------
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Snake Game - Python")
horloge = pygame.time.Clock()

# ------------------ Charger images ------------------
snake_img = pygame.image.load(r"C:\Users\anton\OneDrive\Bureau\JeuPython\serpent.png")
snake_img = pygame.transform.scale(snake_img, (TAILLE_BLOC, TAILLE_BLOC))

pomme_img = pygame.image.load(r"C:\Users\anton\OneDrive\Bureau\JeuPython\pomme.png")
pomme_img = pygame.transform.scale(pomme_img, (TAILLE_BLOC, TAILLE_BLOC))

ennemi_img = pygame.image.load(r"C:\Users\anton\OneDrive\Bureau\JeuPython\ennemi.png")
ennemi_img = pygame.transform.scale(ennemi_img, (TAILLE_BLOC, TAILLE_BLOC))

# ------------------ Fonctions Menu ------------------
def afficher_menu():
    menu_actif = True
    option_selectionnee = 0
    options = ["JOUER", "RÈGLES", "QUITTER"]
    
    while menu_actif:
        fenetre.fill(NOIR)
        
        # Titre
        font_titre = pygame.font.SysFont("consolas", 50, bold=True)
        titre = font_titre.render("SNAKE GAME", True, VERT)
        fenetre.blit(titre, [LARGEUR/2 - titre.get_width()/2, 50])
        
        # Options du menu
        font_options = pygame.font.SysFont("consolas", 30)
        for i, option in enumerate(options):
            if i == option_selectionnee:
                couleur = VERT
                texte = font_options.render(f"> {option} <", True, couleur)
            else:
                couleur = BLANC
                texte = font_options.render(option, True, couleur)
            fenetre.blit(texte, [LARGEUR/2 - texte.get_width()/2, 150 + i * 60])
        
        # Instructions
        font_instructions = pygame.font.SysFont("consolas", 18)
        instruction = font_instructions.render("Utilisez les flèches HAUT/BAS et ENTRÉE", True, BLEU)
        fenetre.blit(instruction, [LARGEUR/2 - instruction.get_width()/2, 350])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option_selectionnee = (option_selectionnee - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    option_selectionnee = (option_selectionnee + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if option_selectionnee == 0:  # JOUER
                        gameLoop()
                    elif option_selectionnee == 1:  # RÈGLES
                        afficher_regles()
                    elif option_selectionnee == 2:  # QUITTER
                        pygame.quit()
                        quit()
        
        horloge.tick(15)

def afficher_regles():
    affichage_regles = True
    
    while affichage_regles:
        fenetre.fill(NOIR)
        
        # Titre
        font_titre = pygame.font.SysFont("consolas", 40, bold=True)
        titre = font_titre.render("RÈGLES DU JEU", True, VERT)
        fenetre.blit(titre, [LARGEUR/2 - titre.get_width()/2, 30])
        
        # Règles
        font_regles = pygame.font.SysFont("consolas", 18)
        regles = [
            "• Utilisez les flèches pour diriger le serpent",
            "• Mangez les pommes pour grandir",
            "• Évitez les murs et votre propre corps",
            "• À 50 points, un ennemi apparaît",
            "• À 10 points, l'ennemi se déplace",
            "• Plus vous mangez, plus vous allez vite !",
        ]
        
        y_position = 100
        for regle in regles:
            texte = font_regles.render(regle, True, BLANC)
            fenetre.blit(texte, [50, y_position])
            y_position += 35
        
        # Retour
        font_retour = pygame.font.SysFont("consolas", 20)
        retour = font_retour.render("Appuyez sur ÉCHAP pour revenir au menu", True, BLEU)
        fenetre.blit(retour, [LARGEUR/2 - retour.get_width()/2, 350])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    affichage_regles = False
        
        horloge.tick(15)

# ------------------ Fonctions Jeu ------------------
def dessiner_decor(theme_index):
    """Dessine un fond quadrillé style damier avec le thème de couleur"""
    theme = THEMES_DECOR[theme_index]
    for y in range(0, HAUTEUR, TAILLE_BLOC):
        for x in range(0, LARGEUR, TAILLE_BLOC):
            if (x // TAILLE_BLOC + y // TAILLE_BLOC) % 2 == 0:
                pygame.draw.rect(fenetre, theme["fonce"], (x, y, TAILLE_BLOC, TAILLE_BLOC))
            else:
                pygame.draw.rect(fenetre, theme["clair"], (x, y, TAILLE_BLOC, TAILLE_BLOC))
    
    # Bordure décorative
    pygame.draw.rect(fenetre, GRIS_FONCE, (0, 0, LARGEUR, HAUTEUR), 3)
    
    # Afficher le nom du thème
    font_theme = pygame.font.SysFont("consolas", 18)
    texte_theme = font_theme.render(f"Theme: {theme['nom']}", True, BLANC)
    fond = pygame.Surface((texte_theme.get_width() + 10, texte_theme.get_height() + 5))
    fond.fill(NOIR)
    fond.set_alpha(180)
    fenetre.blit(fond, [LARGEUR - texte_theme.get_width() - 15, 5])
    fenetre.blit(texte_theme, [LARGEUR - texte_theme.get_width() - 10, 10])

def afficher_score(score, longueur):
    font = pygame.font.SysFont("consolas", 25)
    texte = font.render(f"Score : {score}  |  Taille : {longueur}", True, BLANC)
    # Fond pour le texte
    fond = pygame.Surface((texte.get_width() + 10, texte.get_height() + 5))
    fond.fill(NOIR)
    fond.set_alpha(180)
    fenetre.blit(fond, [5, 5])
    fenetre.blit(texte, [10, 10])

def dessiner_snake(liste_snake):
    for x, y in liste_snake:
        fenetre.blit(snake_img, (x, y))

def game_over_screen(score):
    option_selectionnee = 0
    options = ["REJOUER", "MENU", "QUITTER"]
    waiting = True
    
    while waiting:
        fenetre.fill(NOIR)
        
        # Titre Game Over
        font_titre = pygame.font.SysFont("consolas", 60, bold=True)
        titre = font_titre.render("GAME OVER !", True, ROUGE)
        fenetre.blit(titre, [LARGEUR/2 - titre.get_width()/2, 60])
        
        # Score final
        font_score = pygame.font.SysFont("consolas", 35)
        texte_score = font_score.render(f"Score final : {score}", True, BLANC)
        fenetre.blit(texte_score, [LARGEUR/2 - texte_score.get_width()/2, 140])
        
        # Options du menu
        font_options = pygame.font.SysFont("consolas", 28)
        for i, option in enumerate(options):
            if i == option_selectionnee:
                couleur = VERT
                texte = font_options.render(f"> {option} <", True, couleur)
            else:
                couleur = BLANC
                texte = font_options.render(option, True, couleur)
            fenetre.blit(texte, [LARGEUR/2 - texte.get_width()/2, 220 + i * 50])
        
        # Instructions
        font_instructions = pygame.font.SysFont("consolas", 18)
        instruction = font_instructions.render("Utilisez les flèches HAUT/BAS et ENTRÉE", True, BLEU)
        fenetre.blit(instruction, [LARGEUR/2 - instruction.get_width()/2, 360])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    option_selectionnee = (option_selectionnee - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    option_selectionnee = (option_selectionnee + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if option_selectionnee == 0:  # REJOUER
                        gameLoop()
                        waiting = False
                    elif option_selectionnee == 1:  # MENU
                        waiting = False
                    elif option_selectionnee == 2:  # QUITTER
                        pygame.quit()
                        quit()
        
        horloge.tick(15)

# ------------------ Boucle principale ------------------
def gameLoop():
    game_over = False
    x = LARGEUR / 2
    y = HAUTEUR / 2
    dx = 0
    dy = 0
    snake_list = []
    longueur_snake = 1
    score = 0
    vitesse = 10

    # Gestion du changement de thème
    theme_actuel = 0
    temps_dernier_changement = pygame.time.get_ticks()
    INTERVALLE_CHANGEMENT = 10000  # 10 secondes en millisecondes

    # Position nourriture
    nourriturex = round(random.randrange(0, LARGEUR - TAILLE_BLOC) / TAILLE_BLOC) * TAILLE_BLOC
    nourriturey = round(random.randrange(0, HAUTEUR - TAILLE_BLOC) / TAILLE_BLOC) * TAILLE_BLOC

    # Position ennemi
    ennemi_visible = False
    ennemi_x = 0
    ennemi_y = 0
    ennemi_dx = TAILLE_BLOC
    ennemi_dy = 0

    while not game_over:
        # Vérifier si 10 secondes se sont écoulées
        temps_actuel = pygame.time.get_ticks()
        if temps_actuel - temps_dernier_changement >= INTERVALLE_CHANGEMENT:
            theme_actuel = (theme_actuel + 1) % len(THEMES_DECOR)
            temps_dernier_changement = temps_actuel
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -TAILLE_BLOC
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = TAILLE_BLOC
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -TAILLE_BLOC
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = TAILLE_BLOC
                    dx = 0
                elif event.key == pygame.K_ESCAPE:
                    return

        x += dx
        y += dy

        # Collision murs
        if x < 0 or x >= LARGEUR or y < 0 or y >= HAUTEUR:
            game_over_screen(score)
            return

        # Dessiner le décor avec le thème actuel
        dessiner_decor(theme_actuel)
        fenetre.blit(pomme_img, (nourriturex, nourriturey))

        # Dessiner ennemi si score >=50
        if score >= 50:
            if not ennemi_visible:
                ennemi_x = round(random.randrange(0, LARGEUR - TAILLE_BLOC) / TAILLE_BLOC) * TAILLE_BLOC
                ennemi_y = round(random.randrange(0, HAUTEUR - TAILLE_BLOC) / TAILLE_BLOC) * TAILLE_BLOC
                ennemi_visible = True
            fenetre.blit(ennemi_img, (ennemi_x, ennemi_y))

            # Déplacer ennemi si score >=10
            if score >= 10:
                ennemi_x += ennemi_dx
                ennemi_y += ennemi_dy

                # Rebondir sur les murs
                if ennemi_x < 0 or ennemi_x >= LARGEUR:
                    ennemi_dx *= -1
                if ennemi_y < 0 or ennemi_y >= HAUTEUR:
                    ennemi_dy *= -1

        # Update Snake
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > longueur_snake:
            del snake_list[0]

        # Collision avec soi-même
        for bloc in snake_list[:-1]:
            if bloc == snake_head:
                game_over_screen(score)
                return

        # Collision avec ennemi
        if ennemi_visible:
            if x == ennemi_x and y == ennemi_y:
                game_over_screen(score)
                return

        dessiner_snake(snake_list)
        afficher_score(score, longueur_snake)
        pygame.display.update()

        # Quand le snake mange la nourriture
        if x == nourriturex and y == nourriturey:
            nourriturex = round(random.randrange(0, LARGEUR - TAILLE_BLOC) / TAILLE_BLOC) * TAILLE_BLOC
            nourriturey = round(random.randrange(0, HAUTEUR - TAILLE_BLOC) / TAILLE_BLOC) * TAILLE_BLOC
            longueur_snake += 1
            score += 10
            vitesse += 0.5

        horloge.tick(vitesse)

# ------------------ Lancer le jeu ------------------
afficher_menu()