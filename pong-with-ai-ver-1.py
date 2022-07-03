"""
If you need to change ball's speed, go to line 45 and modify turtle_object.dx.
If you want to change or disable increasing ball's speed after every score changing, go to line 81 and line 82.
"""
import turtle
import random


# Game window setup
game_window = turtle.Screen()
game_window.title('Pong Game')
game_window.bgcolor('black')
game_window.setup(width=800, height=600)
game_window.tracer(0)

# Score information on the top of the game window setup
score_info = turtle.Turtle()
score_info.speed(0)
score_info.color('white')
score_info.penup()
score_info.hideturtle()
score_info.goto(0, 260)
score_info.write('Player: 0  AI: 0', align='center', font=('Courier', 24, 'normal'))


class CreateGameObject:
    def __init__(self, x_coord: int, is_paddle: bool):
        self.x_coord = x_coord
        self.is_paddle = is_paddle
    
    def create_object(self):
        """This function creates a paddle or a ball depending on the value of is_paddle."""
        turtle_object = turtle.Turtle()
        turtle_object.speed(0)
        turtle_object.color('white')
        turtle_object.penup()
        turtle_object.goto(self.x_coord, 0)

        if self.is_paddle:
            turtle_object.shape('square')
            turtle_object.shapesize(stretch_wid=5, stretch_len=1)
        else:
            turtle_object.shape('circle')
            turtle_object.shapesize(stretch_wid=1, stretch_len=1)
            turtle_object.dx = random.uniform(0.08, 0.2)  # Setting the distance (speed) of the ball movement along the X axis (range of random.uniform(): [0; 1]. If you need speed > 1, use random.randrange(). Also don't forget to change turtle_object.dy (line 46))
            turtle_object.dy = 0.3 - turtle_object.dx  # Setting the distance (speed) of the ball movement along the Y axis

        return turtle_object


class PaddleManipulation:
    def __init__(self, object, ai_move=False):
        self.object = object
        self.ai_move = ai_move

    def move_paddle_up(self):
        y = self.object.ycor()
        if self.ai_move:
            y += 5
        else:
            y += 20
        self.object.sety(y)

    def move_paddle_down(self):
        y = self.object.ycor()
        if self.ai_move:
            y -= 5
        else:
            y -= 20
        self.object.sety(y)


class NewRoundBeginning:
    def __init__(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b
    
    def output_score(self, ball):
        ball.goto(-1000, -1000)
        ball.dx *= -1  # Reverse ball's direction
        # Increasing ball speed
        ball.dx *= 1.01
        ball.dy *= 1.01
        # Output of the score
        score_info.clear()
        score_info.write(f'Player: {self.score_a}  AI: {self.score_b}', align='center', font=('Courier', 24, 'normal'))


def main():
    new_round_flag = True

    # Player Score
    score_a = 0
    score_b = 0

    # Paddles
    paddle_a = CreateGameObject(-350, is_paddle=True).create_object()
    paddle_b = CreateGameObject(350, is_paddle=True).create_object()

    # Processing user keyboard input
    game_window.listen()
    game_window.onkeypress(PaddleManipulation(paddle_a).move_paddle_up, 'w')
    game_window.onkeypress(PaddleManipulation(paddle_a).move_paddle_down, 's')
    game_window.onkeypress(PaddleManipulation(paddle_a).move_paddle_up, 'Up')
    game_window.onkeypress(PaddleManipulation(paddle_a).move_paddle_down, 'Down')

    # Disabled due it is a version of the game with an AI.
    #game_window.onkeypress(PaddleManipulation(paddle_b).move_paddle_up, 'Up')
    #game_window.onkeypress(PaddleManipulation(paddle_b).move_paddle_down, 'Down')

    while True:
        if new_round_flag:
            # Ball
            ball = CreateGameObject(0, is_paddle=False).create_object()
            new_round_flag = False

        game_window.update()

        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border checking
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1  # Reverse ball's direction

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1  # Reverse ball's direction

        if ball.xcor() > 390:
            score_a += 1 
            new_round_flag = True
            NewRoundBeginning(score_a, score_b).output_score(ball)

        if ball.xcor() < -390:
            score_b += 1 
            new_round_flag = True
            NewRoundBeginning(score_a, score_b).output_score(ball)

        # Paddle and ball collisions
        if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50): 
            ball.dx *= -1  # Reverse ball's direction because the ball collided with the paddle
            ball.dx *= 1.01
            ball.dy *= 1.01

        if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50): 
            ball.dx *= -1  # Reverse ball's direction because the ball collided with the paddle
            ball.dx *= 1.01
            ball.dy *= 1.01

        # Preventing the paddle from moving outside the game window
        if paddle_a.ycor() > 250:
            paddle_a.goto(-350, 250)
        
        if paddle_a.ycor() < -250:
            paddle_a.goto(-350, -250)

        if paddle_b.ycor() > 250:
            paddle_b.goto(350, 250)

        if paddle_b.ycor() < -250:
            paddle_b.goto(350, -250)

        # AI Player
        if paddle_b.ycor() < ball.ycor():
            PaddleManipulation(paddle_b, ai_move=True).move_paddle_up()

        if paddle_b.ycor() > ball.ycor():
            PaddleManipulation(paddle_b, ai_move=True).move_paddle_down()


if __name__ == '__main__':
    main()
