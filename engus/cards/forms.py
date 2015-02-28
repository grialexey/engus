from django import forms
from .models import CardLearner


class CardLearnerConfidenceForm(forms.ModelForm):
    confidence = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = CardLearner
        fields = []

    def update_level(self):
        confidence = self.cleaned_data.get('confidence')
        self.instance.update_level(confidence)