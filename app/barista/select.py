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
    
class SelectRecherche(forms.Form):
    CHOIX3 = (        
        ('1','Liste produits en fonction du niveau'),
        ('2','Un Produit en fonction du niveau'),
        ('3','Un Produit spécifique'),
    )
    ma_select_box5 = forms.ChoiceField(choices=CHOIX3, label='Choissisez une action à réaliser :', required=True)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=3)
    
class SelectUtilisateurNeo(forms.Form):
    ma_select_box6 = forms.IntegerField(label='Niveau :')
    ma_select_box7 = forms.CharField(label='Nom utilisateur :', max_length=100)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=4)
    
class SelectProduitAndNiveauNeo(forms.Form):
    ma_select_box8 = forms.IntegerField(label='Niveau :')
    ma_select_box9 = forms.CharField(label='Nom utilisateur :', max_length=100)
    ma_select_box10 = forms.CharField(label='Nom du produit :', max_length=100)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=5)

class SelectProduitNeo(forms.Form):
    ma_select_box11 = forms.IntegerField(label='Niveau :')
    ma_select_box12 = forms.CharField(label='Nom du produit :', max_length=100)
    etape = forms.IntegerField(widget=forms.HiddenInput(), initial=6)