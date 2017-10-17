from django import forms


class LobbyListForm(forms.Form):

    search = forms.CharField(required=False)
    sort_field = forms.ChoiceField(choices=(('id', 'id'),
                                            ('lobbyName', 'Name'),
                                            ('totalSlots', 'Total slots')),
                                   required=False)

    # def clean(self):
    #     # raise forms.ValidationError(u'SUM TING WONG')
    #     pass

    # def clean_search(self):
    #     search = self.cleaned_data.get('search')
    #     raise forms.ValidationError(u'qwerty')
    #     return search


class LobbyCreateForm(forms.Form):

    lobbyName = forms.CharField(max_length=255)
    password = forms.CharField(max_length=32, required=False)
    isPublic = forms.BooleanField(required=False)
    totalSlots = forms.IntegerField(min_value=1, max_value=8)


class PasswordInputForm(forms.Form):

    password = forms.CharField(max_length=32)


class EmptyForm(forms.Form):
    pass