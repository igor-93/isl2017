from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


def set_field_html_name(cls, new_name):
    """
    This creates wrapper around the normal widget rendering, 
    allowing for a custom field name (new_name).
    """
    old_render = cls.widget.render
    def _widget_render_wrapper(name, value, attrs=None):
        return old_render(new_name, value, attrs)

    cls.widget.render = _widget_render_wrapper


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),label='Dandli Password (not Instagram)')


    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
        "username": "Dandli Username",
        "password": "Dandli Password",
    	}


    


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('instagram_username',)
