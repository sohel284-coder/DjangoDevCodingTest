from calendar import month
from threading import Timer
from datetime import datetime

from itertools import chain

from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from django.db.models import Q



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


from transactionapp.serializers import TransactionHistorySerializer, TransactionSerializer
from transactionapp.models import Balance, Transaction




class TransactionAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        if request.data['schedule'] == False:
            try:
                amount = request.data['amount']
                sender = request.user.id
                schedule = request.data['schedule']
                receipent = request.data['receipent']
                schedule_date = None
            except:
                return Response('something wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            check_balance = get_balance(amount, sender)
            if not check_balance:
                return Response('Insufficient balanace', status=status.HTTP_405_METHOD_NOT_ALLOWED)

            debit_transaction = update_balance(sender, receipent, amount, schedule, schedule_date)
            if not debit_transaction:
                return Response('error')

            serializer = TransactionSerializer(debit_transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            try:
                amount = request.data['amount']
                sender = request.user.id
                schedule = request.data['schedule']
                receipent = request.data['receipent']
                schedule_date = request.data['schedule_date']
            except:
                return Response('something wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)    
            serializer = TransactionSerializer()
            debit_transaction = update_balance(sender, receipent, amount, schedule, schedule_date)
            if not debit_transaction:
                return Response('error')

            serializer = TransactionSerializer(debit_transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

           
            

def get_balance(amount, sender):
    try:
        
        get_current_balance = Balance.objects.filter(user=sender).last()
        
        get_current_balance = get_current_balance.current_balance
        print(get_current_balance)
        can_transfer = get_current_balance - amount
        if can_transfer < 0 :
            return False
        return True
    except Exception as e:
        print(e)
        return False  

def update_balance(sender, receipent, amount, schedule, schedule_date):
    get_last_transaction = Balance.objects.filter(user=sender).last()
    get_previous_balance = get_last_transaction.current_balance
    get_current_balance = get_last_transaction.current_balance - amount 

    
    try:
        if schedule:
            status = 'pending'
        else:
            status = 'done' 

        debit_transaction = Transaction.objects.create(
            sender=User.objects.get(id=sender),
            receipent=User.objects.get(id=receipent),
            type='dr',
            amount=amount, 
            schedule=schedule,
            schedule_date=schedule_date,
            status=status
        )
        print(debit_transaction)
        credit_transaction = Transaction.objects.create(
            sender=User.objects.get(id=sender),
            receipent=User.objects.get(id=receipent),
            type='cr',
            amount=amount, 
            schedule=schedule, 
            schedule_date=schedule_date,
            status=status
        )
        
        if schedule:
            return credit_transaction
        
        sender_balance = Balance.objects.create(user=User.objects.get(id=sender), current_balance=get_current_balance, previous_balance=get_previous_balance)

        get_receipent_last_transaction = Balance.objects.filter(user=receipent).last()
        get_receipent_previous_balance = get_receipent_last_transaction.current_balance
        get_receipent_current_balance = get_receipent_last_transaction.current_balance + amount 

        receive_balance = Balance.objects.create(user=User.objects.get(id=receipent), current_balance=get_receipent_current_balance, previous_balance=get_receipent_previous_balance)

    except Exception as e:
        print(e)
        return False

    return debit_transaction



def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()




class TransactionHistoryAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, ):
        transactions = Transaction.objects.filter(Q(sender=request.user, type='dr') | Q(receipent=request.user, type='cr'))
        serializer = TransactionHistorySerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class TransactionScheduler(APIView):
    def post(self, request):
        def clock():
            
            today = datetime.today().strftime('%Y-%m-%d')
            today_transactions = Transaction.objects.filter(status='pending', schedule_date=today, type='cr')
            print(today_transactions)
            for td in today_transactions:
                
                get_last_transaction = Balance.objects.filter(user=td.sender).last()
                get_previous_balance = get_last_transaction.current_balance
                get_current_balance = get_last_transaction.current_balance - td.amount 
                Balance.objects.create(user=td.sender, previous_balance=get_previous_balance, current_balance=get_current_balance)

                get_last_transaction = Balance.objects.filter(user=td.receipent).last()
                get_previous_balance = get_last_transaction.current_balance
                get_current_balance = get_last_transaction.current_balance + td.amount 
                Balance.objects.create(user=td.receipent, previous_balance=get_previous_balance, current_balance=get_current_balance)
                Transaction.objects.filter(id=td.id).update(status='done')
                         
            return False 

        setInterval(86400, clock)
        return Response('success')    

def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()     

    

