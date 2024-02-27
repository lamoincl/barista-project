from django.shortcuts import render
from django.views import View
from barista.select import SelectBddAndRequest, SelectInjection

class HomeView(View):
    template_name = 'base.html'

    def get(self, request):
        form = SelectBddAndRequest()
        return render(request, self.template_name, {'form': form, 'etape': 1})

    def post(self, request):
        etape = int(request.POST.get('etape', '1'))
        form = None
        print(request.POST.get('form', ''))
        if etape == 1:
            form = SelectBddAndRequest(request.POST)
            if form.is_valid():
                etape += 1
                form = SelectInjection(initial={'etape': etape})  
        elif etape == 2:
            form = SelectInjection(request.POST)
            if form.is_valid():
                # Traiter les données valides de l'étape 2
                pass

        if not form:
            form = SelectBddAndRequest() if etape == 1 else SelectInjection()

        return render(request, self.template_name, {'form': form, 'etape': etape})
