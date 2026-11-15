import os
import random
import sys
import time
from pathlib import Path

import turtle


if getattr(sys, "frozen", False):
    resource_folder = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    save_folder = Path(sys.executable).resolve().parent
else:
    resource_folder = Path(__file__).resolve().parent
    save_folder = resource_folder

try:
    import pygame

    pygame.mixer.init()
    audio_path = resource_folder / "snake_music.wav"
    if audio_path.exists():
        pygame.mixer.music.load(str(audio_path))
        pygame.mixer.music.play(-1)
except Exception:
    pygame = None


delay = 0.1

score = 0
highscore = 0

highscore_path = save_folder / "snake_highscore.txt"
try:
    highscore = int(highscore_path.read_text().strip())
except Exception:
    highscore = 0


paused = False
bonus_timer = 0

# Screen
window = turtle.Screen()
window.title("Snake Project")
window.bgcolor("#43d916")
window.setup(width=600, height=480)
window.tracer(0)  # turns off screen updates


image_folder = resource_folder
head_shape = "square"
body_shape = "square"
food_shape = "circle"

try:
    window.register_shape(str(image_folder / "head.gif"))
    head_shape = str(image_folder / "head.gif")
except Exception:
    pass

try:
    window.register_shape(str(image_folder / "body.gif"))
    body_shape = str(image_folder / "body.gif")
except Exception:
    pass

try:
    window.register_shape(str(image_folder / "food.gif"))
    food_shape = str(image_folder / "food.gif")
except Exception:
    pass


border = turtle.Turtle()
border.speed(0)
border.color("#4f5b93")
border.pensize(4)
border.penup()
border.hideturtle()
border.goto(-290, -190)
border.pendown()
for side in range(2):
    border.forward(580)
    border.left(90)
    border.forward(380)
    border.left(90)


head = turtle.Turtle()
head.speed(0)
head.shape(head_shape)
head.shapesize(0.95, 0.95)
head.color("#b2b6b3")
head.penup()
head.goto(0, 0)
head.direction = "stop"


food = turtle.Turtle()
food.speed(0)
food.shape(food_shape)
food.shapesize(0.9, 0.9)
food.color("#f00505")
food.penup()
food.goto(0, 100)

bonus = turtle.Turtle()
bonus.speed(0)
bonus.shape("circle")
bonus.shapesize(1.1, 1.1)
bonus.color("#ffd740")
bonus.penup()
bonus.goto(1000, 1000)

segments = []

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 200)
pen.write(f"Score: 0  High Score: {highscore}  Level: 1", align="center",
          font=("Arial", 20, "bold"))

message = turtle.Turtle()
message.speed(0)
message.penup()
message.hideturtle()
message.goto(0, -40)
message.color("white")
message.write("Press an arrow key or WASD to start", align="center",
              font=("Arial", 16, "normal"))


pause_pen = turtle.Turtle()
pause_pen.speed(0)
pause_pen.penup()
pause_pen.hideturtle()
pause_pen.goto(0, 40)
pause_pen.color("#ffd740")


def update_scoreboard():
    level = score // 5 + 1
    pen.clear()
    pen.write(f"Score: {score}  High Score: {highscore}  Level: {level}",
              align="center", font=("Arial", 20, "bold"))

def update_colors():
   
    for index, segment in enumerate(segments):
        shade = index / max(len(segments), 1)
        green = int(230 - 110 * shade)
        blue = int(120 - 40 * shade)
        segment.color(f"#10{green:02x}{blue:02x}")
        
        
        

def random_position():
   
    while True:
        x = random.randint(-14, 14) * 20
        y = random.randint(-9, 9) * 20
        free = True

        if head.distance(x, y) < 20:
            free = False
        if food.distance(x, y) < 20 or bonus.distance(x, y) < 20:
            free = False
        for segment in segments:
            if segment.distance(x, y) < 20:
                free = False

        if free:
            return x, y
        
        

def add_segment():
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape(body_shape)
    new_segment.shapesize(0.9, 0.9)
    new_segment.penup()
    new_segment.goto(1000, 1000)
    segments.append(new_segment)
    update_colors()
    
    

def game_over():
    global score, delay, bonus_timer


    message.clear()
    message.color("#fdbcbc")
    message.write("GAME OVER", align="center", font=("Arial", 32, "bold"))
    window.update()
    time.sleep(1)
    
    message.clear()
    message.color("white")
    message.write("Press an arrow key to play again", align="center",
                  font=("Arial", 16, "normal"))

    head.goto(0, 0)
    head.direction = "stop"

    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    bonus.goto(1000, 1000)
    bonus_timer = 0

    score = 0
    delay = 0.1

    update_scoreboard()


def go_up():
    if head.direction != "down":
        head.direction = "up"
        message.clear()

def go_down():
    if head.direction != "up":
        head.direction = "down"
        message.clear()

def go_right():
    if head.direction != "left":
        head.direction = "right"
        message.clear()

def go_left():
    if head.direction != "right":
        head.direction = "left"
        message.clear()

def toggle_pause():
    global paused
    paused = not paused
    pause_pen.clear()
    if paused:
        pause_pen.write("PAUSED", align="center", font=("Arial", 32, "bold"))

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

def close_game():
    os._exit(0)

window.getcanvas().winfo_toplevel().protocol("DELETE_WINDOW", close_game)

# interface
window.listen()
window.onkeypress(go_up, "Up")

window.onkeypress(go_down, "Down")

window.onkeypress(go_left, "Left")

window.onkeypress(go_right, "Right")

window.onkeypress(go_up, "w")

window.onkeypress(go_down, "s")

window.onkeypress(go_left, "a")

window.onkeypress(go_right, "d")

window.onkeypress(toggle_pause, "space")


#  loop
while True:
    window.update()

    # Pause
    if paused:
        time.sleep(0.05)
        continue

    
    
    if (head.xcor() > 290 or head.xcor() < -290 or
        head.ycor() > 190 or head.ycor() < -190):

        game_over()

    
    if head.distance(food) < 20:
        x, y = random_position()
        food.goto(x, y)

        add_segment()

        delay = max(0.04, delay - 0.003)
        score += 1

        if score > highscore:
            highscore = score
            try:
                highscore_path.write_text(str(highscore))
            except Exception:
                pass

      
        
        if score % 5 == 0 and bonus_timer == 0:
            x, y = random_position()
            bonus.goto(x, y)
            bonus_timer = 70

        update_scoreboard()

    
    if bonus_timer > 0:
        bonus_timer -= 1

        if head.distance(bonus) < 20:
            bonus.goto(10000, 10000)
            bonus_timer = 0

            add_segment()
            score += 3

            if score > highscore:
                highscore = score
                try:
                    highscore_path.write_text(str(highscore))
                except Exception:
                    pass

            update_scoreboard()

        elif bonus_timer == 0:
            bonus.goto(10000, 10000)

    # Move body segments
    for index in range(len(segments)-1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    
    for segment in segments:
        if segment.distance(head) < 20:
            game_over()
            break

    time.sleep(delay)

window.mainloop()
#tq 
