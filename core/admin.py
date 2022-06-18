from django.contrib import admin

from .models import Animais, Cargo, Recursos, Servico, Funcionario


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('cargo', 'ativo', 'modificado')


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('servico', 'icone', 'ativo', 'modificado')


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'ativo', 'modificado')

@admin.register(Recursos)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('recurso', 'descricao', 'ativo', 'modificado')
    
@admin.register(Animais)
class Animais(admin.ModelAdmin):
    list_display = ('id', 'comeu', 'bebeu', 'saiu','peso', 'saude', 'modificado')