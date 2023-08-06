from time import sleep
from enum import Enum

import RPi.GPIO as GPIO


class Stepper:
    class Direction(Enum):
        CLOCKWISE = 0
        CW = 0
        COUNTERCLOCKWISE = 1
        CCW = 1

    def __init__(self, pul_pin: int, dir_pin: int, ena_pin: int, spr: int = 200) -> None:
        """
        Create a new instance.
        :param pul_pin: Pulse pin.
        :param dir_pin: Direction pin.
        :param ena_pin: Enable pin.
        :param spr: Steps per revolution. default = 200, change when microstepping.
        """
        self.pul = pul_pin
        self.dir = dir_pin
        self.ena = ena_pin

        self.spr = spr

        GPIO.setup(self.pul, GPIO.OUT)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)

    def __del__(self) -> None:
        self.disable()

    def run(self, speed: float, rotations: float, direction: Direction = Direction.CLOCKWISE) -> None:
        """
        Start stepper motor signal.
        :param speed: Motor speed in RPM.
        :param rotations: Amount of rotations motor turns.
        :param direction: Set the direction of the motor ('CW' or 'CCW'), default='CW'.
        :return: None
        """

        steps = int(self.spr * rotations)
        delay = 60/(self.spr*speed)

        if delay <= 0:
            raise ValueError('Speed cannot be zero or lower.')
        elif delay < 0.0001:
            raise ValueError(f'Maximum speed in this setup is: {60/(self.spr * 0.0001)} RPM.')

        if not isinstance(direction, Stepper.Direction):
            raise TypeError('direction must be an instance of Direction')

        GPIO.output(self.dir, direction.value)

        for _ in range(steps):
            GPIO.output(self.pul, GPIO.HIGH)
            sleep(delay / 2)
            GPIO.output(self.pul, GPIO.LOW)
            sleep(delay / 2)

    def enable(self) -> None:
        """
        Enable stepper motor. Used to start rotating or hold position.
        :return: None
        """
        GPIO.output(self.ena, GPIO.HIGH)

    def disable(self) -> None:
        """
        Disable stepper motor. Used to stop rotating or unhold position.
        :return: None
        """
        GPIO.output(self.ena, GPIO.LOW)
