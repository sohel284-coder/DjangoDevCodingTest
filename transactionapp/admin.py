from django.contrib import admin


from transactionapp.models import Balance, Transaction


admin.site.register(Transaction)
admin.site.register(Balance)
