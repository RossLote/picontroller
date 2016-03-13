from RPi import GPIO as pi
from django.views.generic import FormView
from .forms import WheelSpeedForm
from django.http import JsonResponse

ALIVE = False

PINS = [4, 17, 27, 22]

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


class RightWheelSpeed(FormView):
    form_class = WheelSpeedForm

    def form_valid(self, form):
        if not ALIVE:
            return JsonResponse({'error': 'Not Alive'})

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

        return JsonResponse({})


class LeftWheelSpeed(FormView):
    form_class = WheelSpeedForm

    def form_valid(self, form):
        if not ALIVE:
            return JsonResponse({'error': 'Not Alive'})

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

        return JsonResponse({})
