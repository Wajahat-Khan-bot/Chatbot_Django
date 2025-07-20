from django.contrib import admin
from .models import Business
from django.utils.html import format_html

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'services', 'chatbot_url']
    prepopulated_fields = {
        'identifier':['name']
    }
    readonly_fields = ('chatbot_url',)

    def chatbot_url(self,obj):
        base_url = "https://chatwise-xnb0.onrender.com/"
        full_url = f"{base_url}/api/chat/{obj.identifier}/?token={obj.access_token}"
        return format_html(f'<a href="{full_url}" target="_blank">{full_url}</a>')
    
    chatbot_url.short_description = "url"