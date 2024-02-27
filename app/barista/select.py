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
    
class SelectRecherche(forms.Form):
    CHOIX3 = (        
        ('1','Liste produits en fonction du niveau'),
        ('2','Un Produit en fonction du niveau'),
        ('3','Un Produit spécifique'),
    )
    ma_select_box4 = forms.ChoiceField(choices=CHOIX3, label='Choissisez une action à réaliser :', required=True)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=3)
    
class SelectNiveauNeo(forms.Form):
    ma_select_box5 = forms.IntegerField(label='Niveau :')
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=4)
    
class SelectProduitAndNiveauNeo(forms.Form):
    ma_select_box6 = forms.IntegerField(label='Niveau :')
    ma_select_box7 = forms.CharField(label='Nom du produit :', max_length=100)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=5)

class SelectProduitNeo(forms.Form):
    ma_select_box8 = forms.CharField(label='Nom du produit :', max_length=100)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=6)
    