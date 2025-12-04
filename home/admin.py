from django.contrib import admin
from .models import FreeTip,VIP, AdminPayment

@admin.register(FreeTip)
class FreeTipAdmin(admin.ModelAdmin):
    # This controls the columns displayed in the admin list view
    list_display = ('title', 'league', 'teams', 'date_posted', 'results')
    search_fields = ('title', 'teams', 'league')
    list_filter = ('date_posted', 'league')
    
   
    fieldsets = (
        ('Tip Details', {
            'fields': ('title', 'league', 'teams', 'description')
        }),
        ('Results', {
            'fields': ('results',),
            'classes': ('collapse',) # Optional: makes this section collapsible
        }),
    )

@admin.register(VIP)
class VIPAdmin(admin.ModelAdmin):
    # This controls the columns displayed in the admin list view
    list_display = ('title', 'league', 'teams', 'date_posted', 'results')
    search_fields = ('title', 'teams', 'league')
    list_filter = ('date_posted', 'league')
    
   
    fieldsets = (
        ('Tip Details', {
            'fields': ('title', 'league', 'teams', 'description')
        }),
        ('Results', {
            'fields': ('results',),
            'classes': ('collapse',) # Optional: makes this section collapsible
        }),
    )

admin.site.register(AdminPayment)
