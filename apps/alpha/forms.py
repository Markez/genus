from .models import Chama
from django import forms

CONTRIBUTION_INTERVALS = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('yearly', 'Yearly'),
    ]


class ChamaForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'c-input',
                                                         'placeholder': 'Genus Investment', 'required':''}))
    year_founded = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'c-input',
                                                                 'placeholder': '2018', 'required':''}))
    maximum_members = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'c-input',
                                                                    'placeholder': '10', 'required':''}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'c-input',
                                                               'placeholder': 'Briefly describe chama', 'required':'',
                                                               'rows': '3'}))
    contribution_intervals = forms.CharField(widget=forms.Select(choices=CONTRIBUTION_INTERVALS,
                                                                 attrs={'class': 'c-input', 'required':''}))
    total_contributions = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'c-input',
                                                                        'placeholder': '3000', 'required':''}))
    saved_amounts = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'c-input',
                                                                  'placeholder': '30000', 'required':''}))
    twitter_link = forms.CharField(initial='http://', widget=forms.TextInput(attrs={'class': 'c-input',
                                                                 'placeholder': 'n/a', 'required':''}))
    facebook_link = forms.CharField(initial='http://', widget=forms.TextInput(attrs={'class': 'c-input',
                                                                  'placeholder': 'n/a', 'required':''}))

# class UserForm(forms.Form):
#     first_name= forms.CharField(max_length=100)
#     last_name= forms.CharField(max_length=100)
#     email= forms.EmailField()
#     age= forms.IntegerField()
#     favorite_fruit= forms.CharField(label='What is your favorite fruit?', widget=forms.Select(choices=FRUIT_CHOICES))

#         widgets = {
#             'creator': forms.TextInput(attrs={'class': 'c-input', 'value':'{{user.id}}'}),
#             'name': forms.TextInput(attrs={'class': 'c-input', 'placeholder': 'Genus Investment'}),
#             'year_founded': forms.TextInput(attrs={'class': 'c-input', 'placeholder': '2018'}),
#             'maximum_members': forms.TextInput(attrs={'class': 'c-input', 'placeholder': '10'}),
#             'description': forms.TextInput(attrs={'class': 'c-input', 'placeholder': 'Briefly describe chama'}),
#             'contribution_intervals': forms.TextInput(attrs={'class': 'c-input', 'placeholder': 'Monthly'}),
#             'total_contributions': forms.TextInput(attrs={'class': 'c-input', 'placeholder': '3000'}),
#             'saved_amounts': forms.TextInput(attrs={'class': 'c-input', 'placeholder': '30000'}),
#             'twitter_link': forms.TextInput(attrs={'class': 'c-input', 'placeholder': 'n/a'}),
#             'facebook_link': forms.TextInput(attrs={'class': 'c-input', 'placeholder': 'n/a'}),
#         }


# class ChamaForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super(ChamaForm, self).__init__(*args, **kwargs)
#         self.fields['creator'].widget.attrs['name'] = 'creator'
#         self.fields['creator'].widget.attrs['value'] = '{{ user.get_id }}'
#         self.fields['name'].widget.attrs['name'] = 'name'
#         self.fields['name'].widget.attrs['placeholder'] = 'Genus Investment'
#         self.fields['year_founded'].widget.attrs['name'] = 'createdOn'
#         self.fields['year_founded'].widget.attrs['placeholder'] = '2018'
#         self.fields['maximum_members'].widget.attrs['name'] = 'totalMembers'
#         self.fields['maximum_members'].widget.attrs['placeholder'] = '10'
#         self.fields['description'].widget.attrs['name'] = 'description'
#         self.fields['description'].widget.attrs['placeholder'] = 'Briefly describe chama'
#         self.fields['contribution_intervals'].widget.attrs['name'] = 'contributionCircle'
#         self.fields['contribution_intervals'].widget.attrs['placeholder'] = 'Monthly'
#         self.fields['total_contributions'].widget.attrs['name'] = 'totalContributions'
#         self.fields['total_contributions'].widget.attrs['placeholder'] = '3000'
#         self.fields['saved_amounts'].widget.attrs['name'] = 'savedAmount'
#         self.fields['saved_amounts'].widget.attrs['placeholder'] = '30000'
#         self.fields['twitter_link'].widget.attrs['name'] = 'twitterLink'
#         self.fields['twitter_link'].widget.attrs['placeholder'] = 'n/a'
#         self.fields['facebook_link'].widget.attrs['name'] = 'facebookLink'
#         self.fields['facebook_link'].widget.attrs['placeholder'] = 'n/a'
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'c-input'
#             visible.field.widget.attrs['required'] = ''
#
#     class Meta:
#         model = chama
#         fields = ['creator', 'name', 'year_founded', 'maximum_members', 'description', 'contribution_intervals',
# 'total_contributions', 'saved_amounts', 'twitter_link', 'facebook_link']
