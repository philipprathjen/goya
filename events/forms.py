from django import forms 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Event, EventRequest, EventGroup

class EventForm(forms.ModelForm):
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('Submit', 'Create this event', css_class="btn btn-primary" ))

	class Meta:
		model = Event
		fields = '__all__'
		#widgets = {'creator': forms.HiddenInput()}
		
class RequestForm(forms.ModelForm):
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('Submit', 'Request Attendance', css_class="btn btn-primary" ))

	class Meta:
		model = EventRequest
		fields = '__all__'
		#widgets = {'creator': forms.HiddenInput()}
		
class AttendForm(forms.ModelForm):
	helper = FormHelper()
	helper.form_method = 'POST'
	helper.add_input(Submit('Submit', 'Confirm Attendance', css_class="btn btn-primary" ))

	class Meta:
		model = EventGroup
		fields = '__all__'
		#widgets = {'creator': forms.HiddenInput()}
		