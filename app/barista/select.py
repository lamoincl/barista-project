from django import forms

class SelectBddAndRequest(forms.Form):
    CHOIX1 = (
        ('1', 'PostgreSQL'),
        ('2', 'Neo4j'),
    )
    CHOIX2 = (
        ('1', 'Injection'),
        ('2', 'Recherche'),
    )
    ma_select_box1 = forms.ChoiceField(choices=CHOIX1, label='Choissisez une base de données :', required=True)
    ma_select_box2 = forms.ChoiceField(choices=CHOIX2, label='Choissisez une action à réaliser :', required=True)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

class SelectInjection(forms.Form):
    ma_select_box3 = forms.IntegerField(label='Nombre d utilisateurs :')
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=2)