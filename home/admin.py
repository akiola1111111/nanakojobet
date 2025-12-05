from django.contrib import admin
from .models import FreeTip, VIP, AdminPayment, DailyBookingCode

@admin.register(FreeTip)
class FreeTipAdmin(admin.ModelAdmin):
    list_display = ('teams', 'league', 'date_posted', 'results')
    list_filter = ('date_posted', 'league', 'results')
    search_fields = ('teams', 'league', 'description')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)
    
    # Remove 'date_posted' from fieldsets since it's auto_now_add=True
    fieldsets = (
        ('Match Information', {
            'fields': ('title', 'teams', 'league')
        }),
        ('Prediction Details', {
            'fields': ('description', 'results')
        }),
        # Removed 'Timing' section since date_posted is auto-generated
    )
    
    # Optional: If you want to show date_posted in readonly format
    readonly_fields = ('date_posted',)

@admin.register(VIP)
class VIPAdmin(admin.ModelAdmin):
    list_display = ('teams', 'league', 'date_posted', 'results')
    list_filter = ('date_posted', 'league', 'results')
    search_fields = ('teams', 'league', 'description')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)
    
    # Remove 'date_posted' from fieldsets since it's auto_now_add=True
    fieldsets = (
        ('Match Information', {
            'fields': ('title', 'teams', 'league')
        }),
        ('Prediction Details', {
            'fields': ('description', 'results')
        }),
        # Removed 'Timing' section since date_posted is auto-generated
    )
    
    # Optional: If you want to show date_posted in readonly format
    readonly_fields = ('date_posted',)

@admin.register(AdminPayment)
class AdminPaymentAdmin(admin.ModelAdmin):
    list_display = ('email', 'amount', 'reference', 'is_verified', 'timestamp')
    list_filter = ('is_verified', 'timestamp')
    search_fields = ('email', 'reference')
    readonly_fields = ('timestamp',)

@admin.register(DailyBookingCode)
class DailyBookingCodeAdmin(admin.ModelAdmin):
    list_display = ('date', 'free_tips_code', 'vip_code')
    list_filter = ('date',)
    search_fields = ('free_tips_code', 'vip_code')
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Date Information', {
            'fields': ('date',)
        }),
        ('Booking Codes', {
            'fields': ('free_tips_code', 'vip_code'),
            'description': 'Enter the booking codes for free tips and VIP tips for this date'
        }),
    )
admin.site.site_header = "Nanakojoodds Betting Tips Admin"
admin.site.site_title = "Nanakojoodds Admin Portal"
admin.site.index_title = "Welcome to Nanakojoodds Administration"
