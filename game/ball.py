# At top of file, ensure you import pygame
import pygame
import random
class Ball:
    def __init__(self, x, y, w=16, h=16, speed_x=6, speed_y=4):
        self.rect = pygame.Rect(x, y, w, h)
        self.velocity_x = speed_x
        self.velocity_y = speed_y
        # store previous position
        self.prev_pos = pygame.Vector2(self.rect.x, self.rect.y)

    def update(self, paddles, screen_rect):
        # Save old position
        old_x, old_y = self.rect.x, self.rect.y

        # Move ball
        self.rect.x += int(self.velocity_x)
        self.rect.y += int(self.velocity_y)

        # Build swept rect from old to new position (covers path)
        sweep_left = min(old_x, self.rect.x)
        sweep_top  = min(old_y, self.rect.y)
        sweep_width = abs(self.rect.x - old_x) + self.rect.width
        sweep_height = abs(self.rect.y - old_y) + self.rect.height
        swept = pygame.Rect(sweep_left, sweep_top, sweep_width, sweep_height)

        # Check collisions with paddles using swept rect to avoid tunneling
        for paddle in paddles:
            if swept.colliderect(paddle.rect):
                # Determine if collision is primarily horizontal (paddle hit) or vertical (rare)
                if old_x < paddle.rect.x and self.rect.x >= paddle.rect.x - self.rect.width:
                    # hit left side of paddle - moving right
                    self.rect.right = paddle.rect.left - 1
                    self.velocity_x = -abs(self.velocity_x)
                elif old_x > paddle.rect.x and self.rect.x <= paddle.rect.right:
                    # hit right side of paddle - moving left
                    self.rect.left = paddle.rect.right + 1
                    self.velocity_x = abs(self.velocity_x)
                else:
                    # Fallback: flip X velocity
                    self.velocity_x *= -1

                # small speed tweak to change angle by where ball hits paddle
                # compute offset from paddle center to ball center
                offset = (self.rect.centery - paddle.rect.centery) / (paddle.rect.height / 2)
                self.velocity_y += offset * 2  # tweak vertical speed slightly
                break

        # Wall collisions (top/bottom)
        if self.rect.top <= screen_rect.top:
            self.rect.top = screen_rect.top
            self.velocity_y = abs(self.velocity_y)
        elif self.rect.bottom >= screen_rect.bottom:
            self.rect.bottom = screen_rect.bottom
            self.velocity_y = -abs(self.velocity_y)
