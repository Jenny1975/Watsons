from django import forms
from .models import Promotion

class PromotionForm(forms.Form):
    start_time = forms.DateField(label='StartTime')
    end_time = forms.DateField(label='EndTime')
    amount = forms.IntegerField(label='Promotion_Amount')

    class Meta:    
        model = Promotion    
        fields = ('start_time', 'end_time', 'amount')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()