# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
define isgameover = False

define e = Character("C_person", color="#800000") 
define mc = Character("Player", color="#FF00FF")

#############################################################################################################
#
# Mini Game
#
init python:

    class PongDisplayable(renpy.Displayable):

        def __init__(self):

            renpy.Displayable.__init__(self)

            # The sizes of some of the images.
            self.PADDLE_WIDTH = 12
            self.PADDLE_HEIGHT = 95
            self.PADDLE_X = 240
            self.BALL_WIDTH = 15
            self.BALL_HEIGHT = 15
            self.COURT_TOP = 129
            self.COURT_BOTTOM = 650

            # Some displayables we use.
            self.paddle = Solid("#ffffff", xsize=self.PADDLE_WIDTH, ysize=self.PADDLE_HEIGHT)
            self.ball = Solid("#ffffff", xsize=self.BALL_WIDTH, ysize=self.BALL_HEIGHT)

            # If the ball is stuck to the paddle.
            self.stuck = True

            # The positions of the two paddles.
            self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
            self.computery = self.playery

            # The speed of the computer.
            self.computerspeed = 380.0

            # The position, delta-position, and the speed of the
            # ball.
            self.bx = self.PADDLE_X + self.PADDLE_WIDTH + 10
            self.by = self.playery
            self.bdx = .5
            self.bdy = .5
            self.bspeed = 350.0

            # The time of the past render-frame.
            self.oldst = None

            # The winner.
            self.winner = None

        def visit(self):
            return [ self.paddle, self.ball ]

        # Recomputes the position of the ball, handles bounces, and
        # draws the screen.
        def render(self, width, height, st, at):

            # The Render object we'll be drawing into.
            r = renpy.Render(width, height)

            # Figure out the time elapsed since the previous frame.
            if self.oldst is None:
                self.oldst = st

            dtime = st - self.oldst
            self.oldst = st

            # Figure out where we want to move the ball to.
            speed = dtime * self.bspeed
            oldbx = self.bx

            if self.stuck:
                self.by = self.playery
            else:
                self.bx += self.bdx * speed
                self.by += self.bdy * speed

            # Move the computer's paddle. It wants to go to self.by, but
            # may be limited by it's speed limit.
            cspeed = self.computerspeed * dtime
            if abs(self.by - self.computery) <= cspeed:
                self.computery = self.by
            else:
                self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)

            # Handle bounces.

            # Bounce off of top.
            ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
            if self.by < ball_top:
                self.by = ball_top + (ball_top - self.by)
                self.bdy = -self.bdy

            # Bounce off bottom.
            ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
            if self.by > ball_bot:
                self.by = ball_bot - (self.by - ball_bot)
                self.bdy = -self.bdy

            # This draws a paddle, and checks for bounces.
            def paddle(px, py, hotside):

                # Render the paddle image. We give it an 800x600 area
                # to render into, knowing that images will render smaller.
                # (This isn't the case with all displayables. Solid, Frame,
                # and Fixed will expand to fill the space allotted.)
                # We also pass in st and at.
                pi = renpy.render(self.paddle, width, height, st, at)

                # renpy.render returns a Render object, which we can
                # blit to the Render we're making.
                r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))

                if py - self.PADDLE_HEIGHT / 2 <= self.by <= py + self.PADDLE_HEIGHT / 2:

                    hit = False

                    if oldbx >= hotside >= self.bx:
                        self.bx = hotside + (hotside - self.bx)
                        self.bdx = -self.bdx
                        hit = True

                    elif oldbx <= hotside <= self.bx:
                        self.bx = hotside - (self.bx - hotside)
                        self.bdx = -self.bdx
                        hit = True

                    if hit:
                        #renpy.sound.play("pong_boop.opus", channel=1)
                        self.bspeed *= 1.10

            # Draw the two paddles.
            paddle(self.PADDLE_X, self.playery, self.PADDLE_X + self.PADDLE_WIDTH)
            paddle(width - self.PADDLE_X - self.PADDLE_WIDTH, self.computery, width - self.PADDLE_X - self.PADDLE_WIDTH)

            # Draw the ball.
            ball = renpy.render(self.ball, width, height, st, at)
            r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                          int(self.by - self.BALL_HEIGHT / 2)))

            # Check for a winner.
            if self.bx < -50:
                self.winner = "eileen"

                # Needed to ensure that event is called, noticing
                # the winner.
                renpy.timeout(0)

            elif self.bx > width + 50:
                self.winner = "player"
                renpy.timeout(0)

            # Ask that we be re-rendered ASAP, so we can show the next
            # frame.
            renpy.redraw(self, 0)

            # Return the Render object.
            return r

        # Handles events.
        def event(self, ev, x, y, st):

            import pygame

            # Mousebutton down == start the game by setting stuck to
            # false.
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                self.stuck = False

                # Ensure the pong screen updates.
                renpy.restart_interaction()

            # Set the position of the player's paddle.
            y = max(y, self.COURT_TOP)
            y = min(y, self.COURT_BOTTOM)
            self.playery = y

            # If we have a winner, return him or her. Otherwise, ignore
            # the current event.
            if self.winner:
                return self.winner
            else:
                raise renpy.IgnoreEvent()

screen pong():

    default pong = PongDisplayable()
    add "bg pong field"
    add pong

    text _("Player"):
        xpos 240
        xanchor 0.5
        ypos 25
        size 40

    text _("Eileen"):
        xpos (1280 - 240)
        xanchor 0.5
        ypos 25
        size 40

    if pong.stuck:
        text _("Click to Begin"):
            xalign 0.5
            ypos 50
            size 40




##########################################################################################################
#
# Labels for each day

label Monday:
    
    show eileen happy

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"
    
    call CC1
    call CC2
    call CC3
    return 
    
label Tuesday:

    e "j8q0jh3r9ha378a"

    "wa3q210391u203!"
    
    return 
    
label Wednesday:

    e "j8q0jh3r9ha378a"

    "wa3q210391u203!"
    
    return 
    
label Thursday:

    e "j8q0jh3r9ha378a"

    "wa3q210391u203!"
    
    return 
##########################################################################################################
#
# Labelsfor Choices for Main Girl_C

label CC1:
    $ choice = 0
    "This is choice number #1"
    
    menu:
        "1. Throw the stress ball on your desk AT HER WINDOW":
            $choice = 1
        "2. Call her cellphone":
            $choice = 2
        "3. Go downstairs and ring her door bell":
            $choice = 3

    if choice == 1:
        "You grab the used stress ball sitting on your desk and open your window." 
        "Take a couple of steps back, run up and throw the ball."
        "You’ve done this before, the window won’t break. The ball hits, and hits hard."
        mc"WAKE UP!!!"
        "You hear an audible thud and the blinds open slowly." 
        "You see your childhood friend in her pyjamas and freak out about oversleeping." 
        "Again..."
        "You take your leave and wait outside for her."
    elif choice == 2:
        "You grab your cell phone and ring her phone."
        "ㄴ phone ring sound ㄱ"
        "It rings for a while and finally she picks up."
        
        e"H-hello?"
        mc"Good morning, idiot." 
        mc"It's currently 30 minutes before class starts and from the looks of it you just woke up." 
        mc"Get it together, I won’t be here to wake you up forever."
        
        "You start to hear her freak out and panic about being late for school." 
        "She hangs up and you let out a big sigh. Hopefully she won’t do this ever again."
        "You take your leave and wait outside for her."
    elif choice == 3:
        "You decide that the polite thing would be to just ring her doorbell."
        "You step outside and ring her doorbell."
        "The distinct noise of someone running down the stairs and she opens the door."
        "You decide to feign ignorance and be passive aggressive."
        mc"Oh you’re not ready yet?"
        e"Shut up! I overslept and my alarm didn’t go off!"
        "You simply just smile and the door slams shut."
        "You decide to wait for her outside her door."
    return 
    
label CC2:
    $ choice_2 = 0
    "This is choice number #2"
    
    menu:
        "1. Say nothing and stay silent":
            $choice_2 = 1
        "2. “Yea, you need to start waking up on time.”":
            $choice_2 = 1
        "3. Kick her shins and make a run for it.":
            $choice_2 = 3
    
    if choice_2 == 1:
        "This doesn’t feel right."
        "You’re overcome with a sense of mischief and kick her shins lightly and make a run for it. "
    elif choice_2 == 3:
        "An evil grin starts to dawn on your face."
        "You turn to her and kick her shins and make a run for it."
    
    return 
    
label CC3:
    $ choice_3 = 0
    "This is choice number #3"
    
    menu:
        "1. Give her half of your lunch.":
            $choice_3 = 1
        "2. Do nothing and tell her to go away.":
            $choice_3 = 2
    
    if choice_3 == 1:
        "You can’t help but empathize with her, you’ve been in the same situation before and maybe it’s time to show some kindness to her.
        She’s been having a rough morning after all."
        "You walk over to your desk and quickly eat your lunch until half of it remains." 
        "You walk back over and hand it to her."
        mc"Here. It’s only half but it’s all I got"
        e"Are you sure?."
        mc"Yes, now take it before I change my mind and kick your shins again."
        e"Thank you so much!"
        "She gives you a hug and her face lights up as she takes your food and rounds the corner of the hallway." 
        "You turn back to your friends and they are all giving you a smug look. One of them even asked if she was your girlfriend."
    elif choice_3 == 2:
        "Oh no... GAME OVER"
        jump end
    return 
    
label CC4:

    e "j8q0jh3r9ha378a"

    "wa3q210391u203!"
    
    return 
    
label CC5:

    e "j8q0jh3r9ha378a"

    "wa3q210391u203!"
    
    return 
    
##########################################################################################################
#
# The game starts here.

label start:
    scene bg room
    "My friend tito toto"
    pause
    
    call Monday
    $ quick_menu = False
#     call screen pong
    $ quick_menu = True
    
    pause
### End of Game
label end:
    return