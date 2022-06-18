from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django_tables2 import SingleTableView

from django.contrib.auth.models import User, Group

from .models import Servico, Funcionario, Recursos, Animais
from .forms import ContatoForm
from .tables import AnimaisTable

class IndexView(FormView):
    template_name = 'index.html'
    form_class = ContatoForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['servicos'] = Servico.objects.order_by('?').all()
        context['funcionarios'] = Funcionario.objects.order_by('?').all()
        
        var = int((Recursos.objects.count())/2)
        context['recursos1'] = Recursos.objects.all()[:var]
        
        context['recursos2'] = Recursos.objects.all()[var:]
        return context
    
    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(IndexView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail')
        return super(IndexView, self).form_invalid(form, *args, **kwargs)

class AnimaisView(SingleTableView):
    model = Animais
    table_class = AnimaisTable
    template_name = 'animais.html'