from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Event

class EventForm(forms.ModelForm):
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('Submit', 'Create this event', css_class="btn btn-primary" ))

	class Meta:
		model = Event
		fields = '__all__'
		#widgets = {'creator': forms.HiddenInput()}
		
