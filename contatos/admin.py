from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoria', 'nome', 'sobrenome', 'telefone', 'email', 'Mostrar']
    list_display_links = ['id', 'categoria', 'nome']
    #list_filter = ['categoria']
    list_per_page = 10
    search_fields = ['id', 'nome', 'sobrenome']
    list_editable = ['telefone', 'Mostrar']


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)



