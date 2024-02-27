from django.shortcuts import render
from django.views import View
from barista.select import SelectBddAndRequest, SelectInjection, SelectRecherche, SelectProduitAndNiveauNeo, SelectUtilisateurNeo, SelectProduitNeo

class HomeView(View):
    template_name = 'base.html'

    def get(self, request):
        form = SelectBddAndRequest()
        return render(request, self.template_name, {'form': form, 'etape': 1})

    def post(self, request):
        etape = int(request.POST.get('etape', '1'))
        form = None
        db = None
        if etape == 1:
            form = SelectBddAndRequest(request.POST)
            if form.is_valid():
                request.session['db'] = form.cleaned_data['ma_select_box1'] # save db selected
                if form.cleaned_data['ma_select_box2'] == '1':
                    etape = 2
                    form = SelectInjection(initial={'etape': etape})
                elif form.cleaned_data['ma_select_box2'] == '2' :
                    etape = 3
                    form = SelectRecherche(initial={'etape': etape})                
        elif etape == 2 :
            form = SelectInjection(request.POST)
            if form.is_valid():
                pass
        elif etape == 3 :
            form = SelectRecherche(request.POST)
            if form.is_valid():
                db = request.session.get('db', None)
                print("DATABASE ->", db)
                if form.cleaned_data['ma_select_box5'] == '1':
                    if db == '2': #Neo4j
                        etape = 4
                        form = SelectUtilisateurNeo(initial={'etape': etape})
                elif form.cleaned_data['ma_select_box5'] == '2' :
                    if db == '2': #Neo4j
                        etape = 5
                        form = SelectProduitAndNiveauNeo(initial={'etape': etape})
                elif form.cleaned_data['ma_select_box5'] == '3' :
                    if db == '2': #Neo4j
                        etape = 6
                        form = SelectProduitNeo(initial={'etape': etape})
                pass
        if not form:
            form = SelectBddAndRequest() if etape == 1 else SelectInjection()

        return render(request, self.template_name, {'form': form, 'etape': etape})
