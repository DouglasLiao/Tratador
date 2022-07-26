from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django_tables2 import SingleTableView

from django.contrib.auth.models import User, Group

from .models import Servico, Funcionario, Recursos, Animais, Read
from .forms import ContatoForm
from .tables import AnimaisTable, ReaderTable

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .serializers import AnimaisSerializer

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
    
class AnimaisListApiView(APIView):
    def get(self, request, *args, **kwargs):
        animal = Animais.objects.filter(ativo = request.user.id)
        serializer = AnimaisSerializer(animal, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'comeu': request.data.get('comeu'), 
            'bebeu': request.data.get('bebeu'), 
            'saiu': request.data.get('saiu'), 
            'peso': request.data.get('peso'), 
            'saude': request.data.get('saude'), 
            'id': request.user.id
        }
        serializer = AnimaisSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, animais_id, *args, **kwargs):
        animal_instance = self.get_object(animais_id, request.id)
        if not animal_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        animal_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

class ReadListView(SingleTableView):
    model = Read
    table_class = ReaderTable
    template_name = 'read.html'
