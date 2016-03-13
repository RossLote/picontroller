from RPi import GPIO as pi
from django.views.generic import FormView
from .forms import WheelSpeedForm

ALIVE = False

PINS = [4, 17, 27, 22]

FORWARD_RIGHT_PIN = None
FORWARD_LEFT_PIN = None
BACKWARD_RIGHT_PIN = None
BACKWARD_LEFT_PIN = None


def turn_on(request):
    pi.setmode(pi.BCM)
    for pin in PINS:
        pi.setup(pin, pi.OUT)

    FORWARD_RIGHT_PIN = pi.PWM(PINS[0], 100)
    FORWARD_LEFT_PIN = pi.PWM(PINS[1], 100)
    BACKWARD_RIGHT_PIN = pi.PWM(PINS[2], 100)
    BACKWARD_LEFT_PIN = pi.PWM(PINS[3], 100)

    FORWARD_RIGHT_PIN.start(0)
    FORWARD_LEFT_PIN.start(0)
    BACKWARD_RIGHT_PIN.start(0)
    BACKWARD_LEFT_PIN.start(0)

    ALIVE = True


def turn_off(request):
    FORWARD_RIGHT_PIN.stop()
    FORWARD_LEFT_PIN.stop()
    BACKWARD_RIGHT_PIN.stop()
    BACKWARD_LEFT_PIN.stop()

    FORWARD_RIGHT_PIN = None
    FORWARD_LEFT_PIN = None
    BACKWARD_RIGHT_PIN = None
    BACKWARD_LEFT_PIN = None

    pi.cleanup()

    ALIVE = False


class RightWheelSpeed(FormView):
    form_class = WheelSpeedForm

    def form_valid(self, form):
        if not ALIVE:
            return

        speed = form.cleaned_data['speed']

        if speed > 0:
            FORWARD_RIGHT_PIN.ChangeDutyCycle(speed)
            BACKWARD_RIGHT_PIN.ChangeDutyCycle(0)

        elif speed < 0:
            FORWARD_RIGHT_PIN.ChangeDutyCycle(0)
            BACKWARD_RIGHT_PIN.ChangeDutyCycle(speed)

        else:
            FORWARD_RIGHT_PIN.ChangeDutyCycle(0)
            BACKWARD_RIGHT_PIN.ChangeDutyCycle(0)


class LeftWheelSpeed(FormView):
    form_class = WheelSpeedForm

    def form_valid(self, form):
        if not ALIVE:
            return

        speed = form.cleaned_data['speed']

        if speed > 0:
            FORWARD_LEFT_PIN.ChangeDutyCycle(speed)
            BACKWARD_LEFT_PIN.ChangeDutyCycle(0)

        elif speed < 0:
            FORWARD_LEFT_PIN.ChangeDutyCycle(0)
            BACKWARD_LEFT_PIN.ChangeDutyCycle(speed)

        else:
            FORWARD_LEFT_PIN.ChangeDutyCycle(0)
            BACKWARD_LEFT_PIN.ChangeDutyCycle(0)
