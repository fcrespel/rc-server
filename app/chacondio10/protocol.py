import odroid_wiringpi as wiringpi

__all__ = ["transmit"]

TIME_HIGH_LOCK = 275
TIME_LOW_LOCK1 = 9900
TIME_LOW_LOCK2 = 2675

TIME_HIGH_DATA = 275        # 310 or 275 or 220
TIME_LOW_DATA_LONG = 1225   # 1340 or 1225 or 1400
TIME_LOW_DATA_SHORT = 275   # 310 or 275 or 350


def send_bit(pin: int, b: bool):
    if b:
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        wiringpi.delayMicroseconds(TIME_HIGH_DATA)
        wiringpi.digitalWrite(pin, wiringpi.LOW)
        wiringpi.delayMicroseconds(TIME_LOW_DATA_LONG)
    else:
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        wiringpi.delayMicroseconds(TIME_HIGH_DATA)
        wiringpi.digitalWrite(pin, wiringpi.LOW)
        wiringpi.delayMicroseconds(TIME_LOW_DATA_SHORT)


def send_pair(pin: int, b: bool):
    send_bit(pin, b)
    send_bit(pin, not b)


def send_word(pin: int, word: int, bits: int):
    for bit in reversed(range(bits)):
        if word & (1 << bit):
            send_pair(pin, True)
        else:
            send_pair(pin, False)


def transmit(pin: int, sender: int, group: bool, button: int, onoff: bool):
    # Start lock
    wiringpi.digitalWrite(pin, wiringpi.HIGH)
    wiringpi.delayMicroseconds(TIME_HIGH_LOCK)
    wiringpi.digitalWrite(pin, wiringpi.LOW)
    wiringpi.delayMicroseconds(TIME_LOW_LOCK1)
    wiringpi.digitalWrite(pin, wiringpi.HIGH)
    wiringpi.delayMicroseconds(TIME_HIGH_LOCK)
    wiringpi.digitalWrite(pin, wiringpi.LOW)
    wiringpi.delayMicroseconds(TIME_LOW_LOCK2)
    wiringpi.digitalWrite(pin, wiringpi.HIGH)

    # Sender code (26 bits)
    send_word(pin, sender, 26)

    # Group bit
    send_pair(pin, group)

    # On/off bit
    send_pair(pin, onoff)

    # Button number (4 bits)
    send_word(pin, button, 4)

    # End lock
    wiringpi.digitalWrite(pin, wiringpi.HIGH)
    wiringpi.delayMicroseconds(TIME_HIGH_LOCK)
    wiringpi.digitalWrite(pin, wiringpi.LOW)

    # Delay before next transmission
    wiringpi.delay(10)
