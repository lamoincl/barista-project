from django.shortcuts import render, redirect
from django.views import View
from barista.select import SelectBddAndRequest, SelectProduitAndNiveauNeo, SelectProduitNeo, SelectRecherche, SelectUtilisateurNeo
import os 
import csv
from barista.utils import generate_csv
from barista.neo4j import init_neo4j, request1, request2, request3

class HomeView(View):
    template_name = 'base.html'
    
    def get(self, request):
        users_file_path = './shared/users.csv'
        products_file_path = './shared/products.csv'
        follow_file_path = 'shared/follow.csv'
        buy_file_path = 'shared/buy.csv'

        if not os.path.exists(users_file_path) or not os.path.exists(products_file_path) or not os.path.exists(follow_file_path) or not os.path.exists(buy_file_path):
            generate_csv(1_000_000, 10_000)
        
        with open(users_file_path, 'r') as users_file:
            no_lines_users = len(list(csv.reader(users_file)))
        
        with open(products_file_path, 'r') as products_file:
            no_lines_products = len(list(csv.reader(products_file)))

        form = SelectBddAndRequest()

        return render(request, self.template_name, {
            'form': form, 
            'etape': 1, 
            'no_lines_users': no_lines_users, 
            'no_lines_products': no_lines_products
        })
    
    def post(self, request):
        if 'generate' in request.POST:
            time = generate_csv(1_000_000, 10_000)
            reader = csv.reader(open("./shared/users.csv"))
            no_lines_users= len(list(reader))
            reader = csv.reader(open("./shared/products.csv"))
            no_lines_products = len(list(reader))
            form = SelectBddAndRequest()

            return render(request, self.template_name, {'form': form, 'etape': 1, 'no_lines_users': no_lines_users, 'no_lines_products': no_lines_products, 'time': time})
        form = SelectBddAndRequest(request.POST)
        if form.is_valid():
            db = form.cleaned_data['ma_select_box1']
            option = form.cleaned_data['ma_select_box2']
            if option == '1':
                if db == '1':
                    db_name = 'Postgresql'   
                elif db == '2':
                    db_name = 'Neo4j'
                return redirect('injection_url', db_name)
            elif option == '2':
                if db == '1':
                    db_name = 'Postgresql'   
                elif db == '2':
                    db_name = 'Neo4j'
                return redirect('recherche_url', db_name)
        
        
class InjectionView(View):
    template_name = 'injection.html'

    def get(self, request, db_name):
        print("Début de l'injection")
        time = init_neo4j()
        return render(request, self.template_name, {'db_name': db_name, 'time': time})

class ResearchView(View):
    template_name = 'research.html'

    def get(self, request, db_name):
        form = SelectRecherche()
        return render(request, self.template_name, {'db_name': db_name, 'form': form, 'etape': 3})
    def post(self, request, db_name):
        form = SelectRecherche(request.POST)
        if form.is_valid():
            option = form.cleaned_data['ma_select_box5']
            if option == '1':
                return redirect('recherche1_url', db_name)
            elif option == '2':
                return redirect('recherche2_url', db_name)
            elif option == '3':
                return redirect('recherche3_url', db_name)
    
class Request1View(View):
    template_name = "request1.html"
        
    def get(self, request, db_name):
        
        if db_name == 'Neo4j':
            form = SelectUtilisateurNeo()
            return render(request, self.template_name, {'db_name': db_name, 'form': form, 'etape': 4})
        
    def post(self, request, db_name):
        form = SelectUtilisateurNeo(request.POST)
        if form.is_valid():
            level = form.cleaned_data['ma_select_box6']
            user_id = form.cleaned_data['ma_select_box7']
            time, result, col_names = request1(user_id, level)

            request.session['result'] = result
            request.session['col_names'] = col_names
            request.session['time'] = time

            return redirect('result_url')
    
class Request2View(View):
    template_name = "request2.html"
        
    def get(self, request, db_name):
            if db_name == 'Neo4j':
                form = SelectProduitAndNiveauNeo()
            
                return render(request, self.template_name, {'db_name': db_name, 'form': form, 'etape': 5})
            
class Request3View(View):
    template_name = "request3.html"
        
    def get(self, request, db_name):
            if db_name == 'Neo4j':
                form = SelectProduitNeo()
            
                return render(request, self.template_name, {'db_name': db_name, 'form': form, 'etape': 6})
            
class ResultView(View):
        template_name = 'result.html'

        def get(self, request):
            print("Affichage du résultat", request.session.get('result', []))
            result = request.session.get('result', [])
            col_names = request.session.get('col_names', [])
            time = request.session.get('time', 0)

            context = {
                'result': result,
                'col_names': col_names,
                'time': time,
            }
            return render(request, self.template_name, context)
    