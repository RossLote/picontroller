from django import forms


class WheelSpeedForm(forms.Form):
    speed = forms.IntegerField(max_value=100, min_value=-100)
