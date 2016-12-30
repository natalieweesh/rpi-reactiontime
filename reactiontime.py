import pygame.mixer
from pygame.mixer import Sound
from gpiozero import Button, LED, RGBLED
from signal import pause
from functools import partial, update_wrapper
import time, datetime, random

def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

button_left = Button(3)
button_right = Button(2)
sound_left = Sound("sounds/drum_cymbal_open.wav")
sound_right = Sound("sounds/drum_tom_mid_hard.wav")
sound_beep = Sound("sounds/elec_blip.wav")
sound_boom = Sound("sounds/elec_blup.wav")
led_left = LED(7, initial_value=False)
led_right = LED(8, initial_value=False)
rgb_led = RGBLED(5, 6, 13)
rgb_led.color = (0,0,0)

game_over = False
message_printed = False
left_time = -1
right_time = -1
start_time = -1

def end_game():
    global message_printed
    if message_printed:
        return
    left_diff = left_time - start_time
    right_diff = right_time - start_time
    print("LEFT" if left_diff < right_diff else "RIGHT", " WINS!")
    print("left reaction time", left_diff)
    print("right reaction time", right_diff)
    message_printed = True

def press(which):
    global game_over
    global left_time
    global right_time

    time = datetime.datetime.now()
    if which == "left":
        sound_left.play()
        if left_time == -1:
            left_time = time
    elif which == "right":
        sound_right.play()
        if right_time == -1:
            right_time = time

    if game_over:
        end_game()
        return
    else:
        game_over = True

    if which == "left":
        led_left.on()
    else:
        led_right.on()

def main():
    global start_time
    print("game will start in 5 seconds")
    time.sleep(5)
    sound_boom.play()
    print("OK! press the button when you see the light...")
    rand = random.random() * 5
    time.sleep(rand)
    sound_beep.play()
    rgb_led.color = (0, 1, 0)
    start_time = datetime.datetime.now()


    button_left.when_pressed = wrapped_partial(press, which="left")
    button_right.when_pressed = wrapped_partial(press, which="right")

    pause()

if __name__ == "__main__":
    main()
