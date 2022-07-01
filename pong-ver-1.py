"""
If you need to change ball's speed, go to line 44 and line 45 and modify turtle_object.dx.
If you want to change or disable increasing ball's speed after every score changiing, go to line 74 and line 75.
"""
import turtle 


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
score_info.write('Player 1: 0  Player 2: 0', align='center', font=('Courier', 24, 'normal'))


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
            turtle_object.dx = 0.15  # Setting the distance (speed) of the ball movement along the X axis
            turtle_object.dy = 0.15  # Setting the distance (speed) of the ball movement along the Y axis

        return turtle_object


class PaddleManipulation:
    def __init__(self, object):
        self.object = object

    def move_paddle_up(self):
        y = self.object.ycor()
        y += 20
        self.object.sety(y)

    def move_paddle_down(self):
        y = self.object.ycor()
        y -= 20
        self.object.sety(y)


class NewRoundBeginning:
    def __init__(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b
    
    def output_score(self, ball):
        ball.goto(0, 0)
        ball.dx *= -1  # Reverse ball's direction
        # Increasing ball speed
        ball.dx *= 1.05
        ball.dy *= 1.05
        # Output of the score
        score_info.clear()
        score_info.write(f'Player 1: {self.score_a}  Player 2: {self.score_b}', align='center', font=('Courier', 24, 'normal'))


def main():
    # Player Score
    score_a = 0
    score_b = 0

    # Paddles
    paddle_a = CreateGameObject(-350, is_paddle=True).create_object()
    paddle_b = CreateGameObject(350, is_paddle=True).create_object()

    # Ball
    ball = CreateGameObject(0, is_paddle=False).create_object()

    # Processing user keyboard input
    game_window.listen()
    # Left paddle (paddle_a)
    game_window.onkeypress(PaddleManipulation(paddle_a).move_paddle_up, 'w')
    game_window.onkeypress(PaddleManipulation(paddle_a).move_paddle_down, 's')
    # Right paddle (paddle_b)
    game_window.onkeypress(PaddleManipulation(paddle_b).move_paddle_up, 'Up')
    game_window.onkeypress(PaddleManipulation(paddle_b).move_paddle_down, 'Down')

    while True:
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
            NewRoundBeginning(score_a, score_b).output_score(ball)

        if ball.xcor() < -390:
            score_b += 1 
            NewRoundBeginning(score_a, score_b).output_score(ball)

        # Paddle and ball collisions
        if (340 < ball.xcor() < 350) and (paddle_b.ycor() - 50 < ball.ycor() < paddle_b.ycor() + 50): 
            ball.dx *= -1  # Reverse ball's direction because the ball collided with the paddle

        if (-350 < ball.xcor() < -340) and (paddle_a.ycor() - 50 < ball.ycor() < paddle_a.ycor() + 50): 
            ball.dx *= -1  # Reverse ball's direction because the ball collided with the paddle


if __name__ == '__main__':
    main()
