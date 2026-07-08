from django import forms

from .models import *


class SubmissionForm(forms.ModelForm):

    class Meta:

        model = Submission

        fields = [

            'activity',

            'activity_date',

            'description'

        ]

        widgets = {

            'activity_date': forms.DateInput(

                attrs={

                    'type': 'date'

                }

            ),

            'description': forms.Textarea(

                attrs={

                    'rows':6

                }

            )

        }