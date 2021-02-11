from django.forms import ModelForm
from .models import EmailRecipient, InfoRequester


class EmailSignUp(ModelForm):
    class Meta:
        model = EmailRecipient
        fields = "__all__"

class InfoRequest(ModelForm):
    class Meta:
        model = InfoRequester
        fields = "__all__"