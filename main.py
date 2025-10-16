import pygame
import time

WINNING_SCORE = 5  # default

def show_game_over(screen, winner_text, screen_rect):
    # Render dim overlay then text
    overlay = pygame.Surface((screen_rect.width, screen_rect.height))
    overlay.set_alpha(180)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))

    font = pygame.font.Font(None, 64)
    text_surf = font.render(winner_text, True, (255,255,255))
    text_rect = text_surf.get_rect(center=screen_rect.center)
    screen.blit(text_surf, text_rect)

    small = pygame.font.Font(None, 32)
    prompt = small.render("Press R to replay, or ESC to quit", True, (200,200,200))
    p_rect = prompt.get_rect(center=(screen_rect.centerx, screen_rect.centery + 60))
    screen.blit(prompt, p_rect)

    pygame.display.flip()

    # Wait inside a loop to keep window responsive
    waiting = True
    while waiting:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    return 'replay'
                if ev.key == pygame.K_ESCAPE:
                    return 'quit'
        # small sleep to avoid busy loop
        pygame.time.delay(50)

    main()
