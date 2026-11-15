import asyncio
import random
import pygame


pygame.init()
WIDTH, HEIGHT = 600, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Web-Ready Snake Game")
clock = pygame.time.Clock()

# Colors (RGB)
BG_COLOR = (67, 217, 22)       # Classic vibrant green
BORDER_COLOR = (79, 91, 147)   # Deep blue-grey
TEXT_COLOR = (255, 255, 255)
FOOD_COLOR = (240, 5, 5)
HEAD_COLOR = (178, 182, 179)
PAUSE_COLOR = (255, 215, 64)

# Fonts
font_large = pygame.font.SysFont("Arial", 20, bold=True)
font_message = pygame.font.SysFont("Arial", 16)
font_pause = pygame.font.SysFont("Arial", 32, bold=True)

# Game State Variables
score = 0
highscore = 0
paused = False
delay = 0.1

head_pos = [0, 0]
head_direction = "stop"
segments = []
food_pos = [0, 0]

def random_position():
    while True:
        x = random.randint(-14, 14) * 20
        y = random.randint(-9, 9) * 20
        free = True

        if head_pos[0] == x and head_pos[1] == y:
            free = False
        if food_pos[0] == x and food_pos[1] == y:
            free = False
        for seg in segments:
            if seg[0] == x and seg[1] == y:
                free = False

        if free:
            return [x, y]

def reset_game():
    global score, delay, head_pos, head_direction, segments, food_pos
    head_pos = [0, 0]
    head_direction = "stop"
    segments.clear()
    food_pos = random_position()
    score = 0
    delay = 0.1

def to_pixel(x, y):
    # Convert center-origin coords (Turtle style) to Pygame screen coords
    return int(WIDTH // 2 + x), int(HEIGHT // 2 - y)

async def main():
    global score, highscore, paused, delay, head_pos, head_direction, food_pos
    
    running = True
    food_pos = random_position()

    while running:
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and head_direction != "down":
                    head_direction = "up"
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and head_direction != "up":
                    head_direction = "down"
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and head_direction != "right":
                    head_direction = "left"
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and head_direction != "left":
                    head_direction = "right"
                elif event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused and head_direction != "stop":
            
            if len(segments) > 0:
                for i in range(len(segments) - 1, 0, -1):
                    segments[i] = list(segments[i - 1])
                segments[0] = list(head_pos)

        
            if head_direction == "up":
                head_pos[1] += 20
            elif head_direction == "down":
                head_pos[1] -= 20
            elif head_direction == "right":
                head_pos[0] += 20
            elif head_direction == "left":
                head_pos[0] -= 20

            # Wall Collision (Bounds: x: -290 to 290, y: -190 to 190)
            if head_pos[0] > 290 or head_pos[0] < -290 or head_pos[1] > 190 or head_pos[1] < -190:
                reset_game()

            
            for seg in segments:
                if head_pos[0] == seg[0] and head_pos[1] == seg[1]:
                    reset_game()
                    break

           
            if abs(head_pos[0] - food_pos[0]) < 10 and abs(head_pos[1] - food_pos[1]) < 10:
                food_pos = random_position()
                segments.append(list(head_pos))
                score += 1
                delay = max(0.04, delay - 0.003)

                if score > highscore:
                    highscore = score

        # Drawing Graphics
        screen.fill(BG_COLOR)

        # Draw Border
        border_rect = pygame.Rect(to_pixel(-290, 190)[0], to_pixel(-290, 190)[1], 580, 380)
        pygame.draw.rect(screen, BORDER_COLOR, border_rect, 4)

        # Draw Food
        fx, fy = to_pixel(food_pos[0], food_pos[1])
        pygame.draw.circle(screen, FOOD_COLOR, (fx, fy), 9)

        # Draw Snake Body with gradient shading
        for index, seg in enumerate(segments):
            sx, sy = to_pixel(seg[0], seg[1])
            shade = index / max(len(segments), 1)
            green = int(230 - 110 * shade)
            blue = int(120 - 40 * shade)
            seg_color = (16, max(0, min(255, green)), max(0, min(255, blue)))
            pygame.draw.rect(screen, seg_color, pygame.Rect(sx - 9, sy - 9, 18, 18))

        # Draw Snake Head
        hx, hy = to_pixel(head_pos[0], head_pos[1])
        pygame.draw.rect(screen, HEAD_COLOR, pygame.Rect(hx - 9, hy - 9, 18, 18), border_radius=4)

        # Scoreboard UI
        level = score // 5 + 1
        score_surface = font_large.render(f"Score: {score}   High Score: {highscore}   Level: {level}", True, TEXT_COLOR)
        screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 20))

        # Initial prompt & pause overlays
        if head_direction == "stop":
            msg_surface = font_message.render("Press an arrow key or WASD to start", True, TEXT_COLOR)
            screen.blit(msg_surface, (WIDTH // 2 - msg_surface.get_width() // 2, HEIGHT // 2 - 40))

        if paused:
            pause_surface = font_pause.render("PAUSED", True, PAUSE_COLOR)
            screen.blit(pause_surface, (WIDTH // 2 - pause_surface.get_width() // 2, HEIGHT // 2 - 20))

        pygame.display.flip()
        await asyncio.sleep(delay)

if __name__ == "__main__":
    asyncio.run(main())