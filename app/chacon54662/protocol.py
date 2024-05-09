import odroid_wiringpi as wiringpi

TIME_HIGH_LOCK = 290
TIME_LOW_LOCK = 2400

TIME_HIGH_0 = 1070
TIME_LOW_0 = 470

TIME_HIGH_1 = 290
TIME_LOW_1 = 1250


def sendBit(pin: int, b: bool):
    if b:
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        wiringpi.delayMicroseconds(TIME_HIGH_1)
        wiringpi.digitalWrite(pin, wiringpi.LOW)
        wiringpi.delayMicroseconds(TIME_LOW_1)
    else:
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        wiringpi.delayMicroseconds(TIME_HIGH_0)
        wiringpi.digitalWrite(pin, wiringpi.LOW)
        wiringpi.delayMicroseconds(TIME_LOW_0)


def sendWord(pin: int, word: int, bits: int):
    for bit in reversed(range(bits)):
        if word & (1 << bit):
            sendBit(pin, True)
        else:
            sendBit(pin, False)


def transmit(pin: int, word: int):
    for _ in range(4):
        # Code word (24 bits)
        sendWord(pin, word, 24)

        # End lock
        wiringpi.digitalWrite(pin, wiringpi.HIGH)
        wiringpi.delayMicroseconds(TIME_HIGH_LOCK)
        wiringpi.digitalWrite(pin, wiringpi.LOW)
        wiringpi.delayMicroseconds(TIME_LOW_LOCK)

    # Delay before next transmission
    wiringpi.delay(10)
