
# from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.gui.events.mouse import onmousemoved,onmouseclicked

FRAME_RATE = 1000 / 120 # 120 frames per second.
NUM_LIVES = 3


def main():
    
    # graphis.draw_bricks()
    graphis = BreakoutGraphics()
    print("I am created agian")

    if graphis.starter is not False:
        onmouseclicked(graphis.starter)    
        onmousemoved(graphis.paddle_move)
    else:
        del graphis

    

    # Add animation loop here!


if __name__ == '__main__':
    main()
