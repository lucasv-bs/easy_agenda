from django.forms import ModelForm

from .models import Consultation

class ConsultationCreateForm(ModelForm):
    class Meta:
        model = Consultation
        fields = ['medical_chart', 'status']