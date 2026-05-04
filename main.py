import pygame, sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
font_ranking = pygame.font.Font(None, 28)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Próximo", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Tetris")

name = input("Nome do jogador: ")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)

game.player_name = name
score_saved = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                score_saved = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
                game.update_score(0, 1)
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
    
    screen.fill((20, 20, 40))

    # Mostrar sprites
    if game.game_over == False:
        game.draw(screen) 

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 15)
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 15)

        score_val = title_font.render(str(game.score), True, Colors.white)
        screen.blit(score_val, score_val.get_rect(center=score_rect.center))

        score_value_surface = title_font.render(str(game.score), True, Colors.white)

        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (365, 20, 50, 50))
        screen.blit(next_surface, (350, 180, 50, 50))

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)

        game.draw(screen)
    else:
        if not score_saved:
            game.save_score()
            score_saved = True

        overlay = pygame.Surface((500, 620), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200)) 
        screen.blit(overlay, (0,0))

        msg_rect = game_over_surface.get_rect(center=(250, 80))
        screen.blit(game_over_surface, msg_rect)

        ranking = game.get_high_scores()
        y_pos = 180
        
        ranking_rect = pygame.Rect(100, 150, 300, 300)
        pygame.draw.rect(screen, Colors.dark_blue, ranking_rect, 0, 15)
        
        for i, (name, pts) in enumerate(ranking):
            color = Colors.yellow if i == 0 else Colors.white
            txt = font_ranking.render(f"{i+1}º {name} - {pts} pts", True, color)
            screen.blit(txt, (130, y_pos))
            y_pos += 45

        restart_txt = font_ranking.render("Pressione para tentar novamente", True, Colors.cyan)
        screen.blit(restart_txt, restart_txt.get_rect(center=(250, 550)))

    pygame.display.update()
    clock.tick(60)