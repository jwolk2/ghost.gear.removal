import board, busio
import pygame
import config.core as cfg
from adafruit_seesaw.seesaw import Seesaw

I2C_BUTTON_RELEASE_EVENT = pygame.USEREVENT + 10

i2c = busio.I2C(board.SCL, board.SDA)
seesaw = Seesaw(i2c, addr=0x3A)

BUTTON_PINS = [cfg.RED_BUTTON_ID, cfg.BLUE_BUTTON_ID, cfg.GREEN_BUTTON_ID]
LED_PINS = [cfg.RED_BUTTON_LED_ID, cfg.BLUE_BUTTON_LED_ID, cfg.GREEN_BUTTON_LED_ID]

for pin in BUTTON_PINS:
    seesaw.pin_mode(pin, seesaw.INPUT_PULLUP)

for pin in LED_PINS:
    seesaw.pin_mode(pin, seesaw.OUTPUT)
    seesaw.digital_write(pin, False) # turn off all LEDs initially

# Track previous button states
_prev_button_states = {pin: False for pin in BUTTON_PINS}

def poll_buttons():
    """Call this once per frame to check for button releases and post events."""
    global _prev_button_states
    for pin in BUTTON_PINS:
        pressed = not seesaw.digital_read(pin)  # active low
        if _prev_button_states[pin] and not pressed:
            # Button was just released
            pygame.event.post(pygame.event.Event(I2C_BUTTON_RELEASE_EVENT, {"button_id": pin}))
        _prev_button_states[pin] = pressed

def set_led(pin: int, state: bool) -> None:
    seesaw.digital_write(pin, state)

def i2c_reset() -> None:
    for pin in LED_PINS:
        set_led(pin, False)