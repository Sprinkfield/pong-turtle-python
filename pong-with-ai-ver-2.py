"""
If you need to change ball's speed, go to line 44 and line 45 and modify turtle_object.dx.
If you want to change or disable increasing ball's speed after every score changing, go to line 81 and line 82.
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
            turtle_object.dx = 0.15  # Setting the distance (speed) of the ball movement along the X axis
            turtle_object.dy = 0.15  # Setting the distance (speed) of the ball movement along the Y axis

        return turtle_object


class TurtleObjectManipulation:
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

    def move_the_ball(self):
        self.object.setx(self.object.xcor() + self.object.dx)
        self.object.sety(self.object.ycor() + self.object.dy)


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
        score_info.write(f'Player: {self.score_a}  AI: {self.score_b}', align='center', font=('Courier', 24, 'normal'))


class BorderChecking:
    def __init__(self, ball, score_a, score_b):
        self.ball = ball
        self.score_a = score_a
        self.score_b = score_b

    def check_border(self):
        # Border checking
        if self.ball.ycor() > 290:
            self.ball.sety(290)
            self.ball.dy *= -1  # Reverse ball's direction

        if self.ball.ycor() < -290:
            self.ball.sety(-290)
            self.ball.dy *= -1  # Reverse ball's direction

        if self.ball.xcor() > 390:
            self.score_a += 1 
            NewRoundBeginning(self.score_a, self.score_b).output_score(self.ball)

        if self.ball.xcor() < -390:
            self.score_b += 1 
            NewRoundBeginning(self.score_a, self.score_b).output_score(self.ball)


class PaddleAndBallCollisions:
    def __init__(self, ball, paddle_a, paddle_b):
        self.ball = ball 
        self.paddle_a = paddle_a
        self.paddle_b = paddle_b

    def check_collision(self):
        if (340 < self.ball.xcor() < 350) and (self.paddle_b.ycor() - 50 < self.ball.ycor() < self.paddle_b.ycor() + 50): 
            self.ball.dx *= -1  # Reverse ball's direction because the ball collided with the paddle

        if (-350 < self.ball.xcor() < -340) and (self.paddle_a.ycor() - 50 < self.ball.ycor() < self.paddle_a.ycor() + 50): 
            self.ball.dx *= -1  # Reverse ball's direction because the ball collided with the paddle


class AiPlayer(PaddleAndBallCollisions):
    def ai_move(self):
        if self.paddle_b.ycor() < self.ball.ycor():
            TurtleObjectManipulation(self.paddle_b, ai_move=True).move_paddle_up()

        if self.paddle_b.ycor() > self.ball.ycor():
            TurtleObjectManipulation(self.paddle_b, ai_move=True).move_paddle_down()


def main():
    # Player Score
    score_1 = 0
    score_2 = 0

    # Paddles
    paddle_a = CreateGameObject(-350, is_paddle=True).create_object()
    paddle_b = CreateGameObject(350, is_paddle=True).create_object()

    # Balls
    ball1 = CreateGameObject(0, is_paddle=False).create_object()
    ball2 = CreateGameObject(0, is_paddle=False).create_object()
    ball2.dx *= -1

    # Processing user keyboard input
    game_window.listen()
    game_window.onkeypress(TurtleObjectManipulation(paddle_a).move_paddle_up, 'w')
    game_window.onkeypress(TurtleObjectManipulation(paddle_a).move_paddle_down, 's')

    # Disabled due it is a version of the game with an AI.
    #game_window.onkeypress(TurtleObjectManipulation(paddle_b).move_paddle_up, 'Up')
    #game_window.onkeypress(TurtleObjectManipulation(paddle_b).move_paddle_down, 'Down')

    while True:
        game_window.update()

        TurtleObjectManipulation(ball1).move_the_ball()
        TurtleObjectManipulation(ball2).move_the_ball()

        BorderChecking(ball1, score_1, score_2).check_border()
        BorderChecking(ball2, score_1, score_2).check_border()

        PaddleAndBallCollisions(ball1, paddle_a, paddle_b).check_collision()
        PaddleAndBallCollisions(ball2, paddle_a, paddle_b).check_collision()

        # Preventing the paddle from moving outside the game window
        if paddle_a.ycor() > 250:
            paddle_a.goto(-350, 250)
        
        if paddle_a.ycor() < -250:
            paddle_a.goto(-350, -250)

        if paddle_b.ycor() > 250:
            paddle_b.goto(350, 250)

        if paddle_b.ycor() < -250:
            paddle_b.goto(350, -250)

        AiPlayer(ball1, paddle_a, paddle_b).ai_move()
        AiPlayer(ball2, paddle_a, paddle_b).ai_move()
        

if __name__ == '__main__':
    main()
