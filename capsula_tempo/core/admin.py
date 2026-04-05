from django.contrib import admin

from .models import Capsula, Usuario, ItemTexto, ItemImagem, ItemLink

admin.site.register(Usuario)
admin.site.register(Capsula)
admin.site.register(ItemTexto)
admin.site.register(ItemImagem)
admin.site.register(ItemLink)