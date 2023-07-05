from campy.gui.events.timer import pause
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random
import time

FRAME_RATE = 1000 / 120 # 120 frames per second.
NUM_LIVES = 3
# Color names to cycle through for brick rows.
COLORS = ['RED', 'ORANGE', 'YELLOW', 'GREEN', 'BLUE']

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 5.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 3.5      # Maximum initial horizontal speed for the ball.
bricks = []

class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout', frame_rate = FRAME_RATE):

        self.ball_radius = ball_radius
        self.paddle_height = paddle_height 
        self.paddle_width = paddle_width 
        self.paddle_offset = paddle_offset 
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_offset = brick_offset
        self.brick_spacing = brick_spacing
        self.title = title
        self.frame_rate = frame_rate
        self.remaining = NUM_LIVES
        
        # Create a graphical window, with some extra space.
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)
        
        # Create a paddle.
        new_paddle_width = ((self.window_width /2)- paddle_width/2)
        new_paddle_height = self.window_height - paddle_offset
        self.paddle = GRect(paddle_width,paddle_height, x = new_paddle_width ,  y = new_paddle_height )
        self.window.add(self.paddle)
        self.paddle.fill_color = 'black'
        # Center a filled ball in the graphical window.
        self.ball = GOval(ball_radius, ball_radius, x = (self.window_width /2), y = self.window_height/2)
        # self.ball = GOval(ball_radius, ball_radius, x = 350, y = 200)
        self.window.add(self.ball)
        self.ball.fill_color = 'black'
        # Default initial velocity for the ball.
        # Draw bricks.
        self.colors = COLORS
            
    
        def draw_bricks(self):
            new_space_x =  0 
            selected_color =  0 
            new_space_y = self.brick_spacing
            for i in range(self.brick_rows):
                for j in range(self.brick_cols):
                    self.brick = GRect(self.brick_width, self.brick_height, x = new_space_x, y = new_space_y)
                    self.window.add(self.brick)
                    bricks.append(self.brick)
                    # print(bricks)
                    new_space_x += self.brick_width + self.brick_spacing
                    self.brick.fill_color = self.colors[selected_color]

                new_space_y += self.brick_height + self.brick_spacing
                new_space_x = 0
                if i % 2 == 1:
                    selected_color += 1 
        draw_bricks(self)
    
    
    def paddle_move(self,event):

        while True:
            paddle_val = self.paddle.x + (self.paddle_width /2)
            
            if event.x > 231 and  (event.x + self.paddle_width/2) < self.window_width:
                x = (event.x - paddle_val)
                self.paddle.move(x,0)
                break
            elif event.x < 231 and event.x -self.paddle_width/2 > 0:
                x = (event.x - paddle_val)
                self.paddle.move(x,0)

                break
            else:
                break

    

    def check_collision(self,x,y):
        result = self.window.get_object_at(x,y)
        if result is not None:
            if result == self.paddle:
                return result
            else:
                bricks.remove(result)
                self.window.remove(result)
                return result
        else:
            result = self.window.get_object_at(x+(2*BALL_RADIUS),y)
            if result is not None:
                if result == self.paddle:
                    return result
                else:
                    bricks.remove(result)
                    self.window.remove(result)
                    return result
            else:
                result = self.window.get_object_at(x,y+(2*BALL_RADIUS))
                if result is not None:
                    if result == self.paddle:
                        return result
                    else:
                        bricks.remove(result)
                        self.window.remove(result)
                        return result
                else:
                    result = self.window.get_object_at(x+(2*BALL_RADIUS),y+(2*BALL_RADIUS))
                    if result is not None:
                        if result == self.paddle:
                            return result
                        else:
                            bricks.remove(result)
                            self.window.remove(result)
                            return result
                    else:
                        return False
                    


    def starter(self,event):
        if self.remaining > 0  :
            self.ball_move()
        else:
            self.rect = GRect(120, 40,x = 160, y = self.window_height/2 )
            self.window.add(self.rect)
            self.rect.fill_color = 'red'
            self.rect.color = 'white'
            self.text = GLabel('Game Over', x = 160 + 30, y = (self.window_height/2)+30)
            self.text.color = 'white'
            self.window.add(self.text)
            return False



    def ball_move(self):
        vy = INITIAL_Y_SPEED
        vx = MAX_X_SPEED
        while True:
            if len(bricks) > 0:
                if self.ball.y > 0 and self.ball.y < self.window_height-self.ball.width+2.5:
                    check = self.check_collision(self.ball.x,self.ball.y)
                    if check == self.paddle:
                        vx = random.uniform(-MAX_X_SPEED,MAX_X_SPEED)
                        vy = vy*(-1)
                    elif check != self.paddle and check != False:
                        vx = random.uniform(-MAX_X_SPEED,MAX_X_SPEED)
                        vy = vy*(-1)
                    if self.ball.x <= 0:
                        vx += 1
                    elif self.ball.x >= self.window_width-self.ball.width:
                        vx -= 1
                    self.ball.move(vx,vy)
                    pause(self.frame_rate)
                elif self.ball.y <= 0:
                    vy = vy*(-1)
                    self.ball.move(vx,vy)
                else:
                    self.remaining -= 1
                    self.rect = GRect(120, 40,x = 160, y = self.window_height/2 )
                    self.window.add(self.rect)
                    self.rect.fill_color = 'blue'
                    label  = GLabel("life lost")
                    self.rect.color = 'white'
                    label.color = 'white'
                    self.window.add(label,190,(self.window_height/2)+30)
                    time.sleep(1)
                    self.ball.x = self.window_width /2
                    self.ball.y = self.window_height/2
                    self.window.remove(label)
                    self.window.remove(self.rect)
                    break
            else:
                self.remaining == 0
                self.rect = GRect(120, 40,x = 160, y = self.window_height/2 )
                self.window.add(self.rect)
                self.rect.fill_color = 'green'
                label  = GLabel("You Won")
                self.rect.color = 'white'
                label.color = 'white'
                self.window.add(label,190,(self.window_height/2)+30)
                del self.ball
                time.sleep(1)
                self.window.remove(label)
                self.window.remove(self.rect)
                    
                break


if __name__ == '__main__':
    graphis = BreakoutGraphics()
    print("I am created agian")

    if graphis.starter is not False:
        onmouseclicked(graphis.starter)    
        onmousemoved(graphis.paddle_move)
    else:
        del graphis


