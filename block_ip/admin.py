from django.contrib import admin


from .models import BlockIP 


@admin.register(BlockIP)
class BlockIPAdmin(admin.ModelAdmin):
	pass
