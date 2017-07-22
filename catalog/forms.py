from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewBookForm(forms.Form):
    renewal_date=forms.DateField(help_text="Enter a date within 4 weeks from now")
    def clean_renewal_date(self):
        data=self.cleaned_data['renewal_date']

        if data<datetime.date.today():
            raise ValidationError(_('Past date invalid unless you have a time machine'))

        if data>datetime.date.today()+datetime.timedelta(weeks=4):
            raise ValidationError(_('I think you should just buy the book'))

        return data
