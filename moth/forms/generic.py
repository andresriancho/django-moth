from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class GenericForm(forms.Form):
    text = forms.CharField()
    INPUT = 'text'
    
    def __init__(self, * args, **kwargs):
        # pylint: disable=E1002
        super(GenericForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        submit = Submit('Submit', 'Submit', css_class="btn-success")

        # generate layout
        self.helper.layout = Layout(
                                    Field(self.INPUT,),
                                    submit
        )