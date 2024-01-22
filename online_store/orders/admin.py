from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import csv
from .models import Order, OrderItem
import datetime
from django.http import HttpResponse
from django.urls import reverse


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # записать первую строку с информацией заголовка
    writer.writerow([field.verbose_name for field in fields])
    # записать строки данных
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Експорт у CSV'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_payment.short_description = 'Stripe платежі'


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">Переглянути</a>')


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Рахунок'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'email', 'city',
                    'department_np', 'order_notes', 'order_total', 'paid',
                    order_payment, 'created', order_detail, order_pdf]

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

    def order_total(self, obj):
        # Рассчитать общую сумму для каждого заказа
        total_cost = sum(item.get_cost() for item in obj.items.all())
        return total_cost

    order_total.short_description = 'Сума замовлення'  # Название для колонки в административной панели


