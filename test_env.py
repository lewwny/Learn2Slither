import pygame
from environment import Board
from utils import *

def manual_test():
    # On initialise l'environnement en mode visuel
    env = Board(visual=True)
    running = True
    
    print("--- MODE TEST MANUEL ---")
    print("Utilise les flèches directionnelles pour bouger.")
    print("Appuie sur ESC pour quitter.")

    # On définit une action par défaut (ne rien faire n'est pas possible, le serpent avance toujours)
    # Pour le test manuel, on va attendre une touche.
    current_action = UP 

    while running:
        # 1. Gestion des entrées clavier (Humain remplace l'Agent)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    current_action = UP
                elif event.key == pygame.K_DOWN:
                    current_action = DOWN
                elif event.key == pygame.K_LEFT:
                    current_action = LEFT
                elif event.key == pygame.K_RIGHT:
                    current_action = RIGHT

        # 2. On fait avancer le jeu d'un pas avec l'action choisie
        # Note: Dans le vrai jeu, l'IA décide très vite. Ici, on ralentit pour que ce soit jouable.
        state, reward, done, score = env.step(current_action)

        # 3. Affichage des infos de débogage dans la console
        # On affiche ce que l'IA "verrait" (Reward et Vision)
        print(f"Action: {current_action} | Reward: {reward} | Score: {score} | Game Over: {done}")
        
        # 4. Rendu graphique
        env.render()
        pygame.time.wait(100) # On gère l'attente manuellement dans le test
        # 5. Gestion de la fin de partie
        if done:
            print(f"--- GAME OVER! Score final: {score} ---")
            print("Redémarrage...")
            env.reset()
            pygame.time.wait(1000) # Pause d'1 seconde avant de relancer

    pygame.quit()

if __name__ == "__main__":
    manual_test()