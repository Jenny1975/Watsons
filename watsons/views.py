from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404,\
     redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.db import models
from decimal import Decimal
from .models import Transaction, Product, Customer, Pocket_other, Servive
from django.db.models import Avg, Sum
import matplotlib.pyplot as plt
from django.http import JsonResponse
import json
from django.views import generic

import csv
import random
import datetime


NOW =  datetime.datetime.now()

def index(request):
    latest_transaction_list = Transaction.objects.order_by('-time')[:5]
    context = {'latest_transaction_list': latest_transaction_list}
    return render(request, 'watsons/Base.html', context)

def create(request):
    with open('Pfile.csv') as pf:
        first = True
        data = csv.reader(pf, delimiter=',')
        for each in data:
            if first:
                first =False
                pass
            else:
                c, created = Product.objects.get_or_create(product_name=each[0], 
                                                        category=each[1],
                                                        price=int(each[2]),
                                                        quantity=int(each[3]))
                if not created:
                    c.save()

    with open('Cfile.csv') as cf:
        first = True
        data = csv.reader(cf, delimiter=',')
        for each in data:
            if first:
                first =False
                pass
            else:
                c, created = Customer.objects.get_or_create(customer_name=each[0],
                                                            gender=each[1])
                if not created:
                    c.save()

    with open('Tfile.csv') as tf:
        first = True
        data = csv.reader(tf, delimiter=',')
        for each in data:
            if first:
                first =False
                pass
            else:
                d = random.randint(1,364)
                thisTime = NOW + datetime.timedelta(days=d)
                c, created = Transaction.objects.get_or_create(customer_id=each[0],
                                                            product_id=each[1],
                                                            time=thisTime,
                                                            amount=each[2])
        if not created:
            c.save()
    return HttpResponse('You can')

#Show Transaction Start

def showTransaction(request):
    allList = Transaction.objects.all()
    yList = Transaction.objects.filter(time__year=2018)
    m1 = Transaction.objects.filter(time__year=2018, time__month=1)
    m2 = Transaction.objects.filter(time__year=2018, time__month=2)
    m3 = Transaction.objects.filter(time__year=2018, time__month=3)
    m4 = Transaction.objects.filter(time__year=2018, time__month=4)
    m5 = Transaction.objects.filter(time__year=2018, time__month=5)
    m6 = Transaction.objects.filter(time__year=2018, time__month=6)
    m7 = Transaction.objects.filter(time__year=2018, time__month=7)
    m8 = Transaction.objects.filter(time__year=2018, time__month=8)
    m9 = Transaction.objects.filter(time__year=2018, time__month=9)
    m10 = Transaction.objects.filter(time__year=2018, time__month=10)
    m11 = Transaction.objects.filter(time__year=2018, time__month=11)
    m12 = Transaction.objects.filter(time__year=2018, time__month=12)

    return render(request, 'watsons/ShowTransaction.html', {'allList': allList})

#Show Transaction End




#RFM Model start
def RFM_model(request):
    customer_list = Customer.objects.all()

    customer_transaction_list = []

    for cm in customer_list:
        transaction_queryset = cm.transaction_set.order_by('delta_date')
        customer_transaction_list.append({"Customer": cm, "Transaction_Query": transaction_queryset})
    
    for customer_t in customer_transaction_list:
        customer_t["recent_num"] = create_recent_number(customer_t["Transaction_Query"])
        customer_t["frequency_num"] = create_frequency_number(customer_t["Transaction_Query"])
        customer_t["amount_num"] = create_amount_number(customer_t["Transaction_Query"])
        customer_t["average_spending"] = customer_avg(customer_t["Transaction_Query"])

    recent_avg_list = calculate_avg(customer_transaction_list, 1)
    frequency_avg_list = calculate_avg(customer_transaction_list, 2)
    amount_avg_list = calculate_avg(customer_transaction_list, 3)



    
    dataset_recent = [{'recent': 5, 'recent_average_amount': recent_avg_list[4]},
                {'recent': 4, 'recent_average_amount': recent_avg_list[3]},
                {'recent': 3, 'recent_average_amount': recent_avg_list[2]},
                {'recent': 2, 'recent_average_amount': recent_avg_list[1]},
                {'recent': 1, 'recent_average_amount': recent_avg_list[0]}]

    dataset_frequency = [{'frequency': 5, 'frequency_average_amount': frequency_avg_list[4]},
                {'frequency': 4, 'frequency_average_amount': frequency_avg_list[3]},
                {'frequency': 3, 'frequency_average_amount': frequency_avg_list[2]},
                {'frequency': 2, 'frequency_average_amount': frequency_avg_list[1]},
                {'frequency': 1, 'frequency_average_amount': frequency_avg_list[0]}]
                
    dataset_amount = [{'amount': 5, 'amount_average_amount': amount_avg_list[4]},
                {'amount': 4, 'amount_average_amount': amount_avg_list[3]},
                {'amount': 3, 'amount_average_amount': amount_avg_list[2]},
                {'amount': 2, 'amount_average_amount': amount_avg_list[1]},
                {'amount': 1, 'amount_average_amount': amount_avg_list[0]},]


    return render(request, 'watsons/detail.html', {'dataset_recent': dataset_recent,
                                                'dataset_frequency': dataset_frequency, 
                                                'dataset_amount' : dataset_amount})


def customer_avg(customer_query):
    total = 0
    count = 0
    for c in customer_query:
        total += c.transaction_total
        count += 1
    average = total / count

    return average


def calculate_avg(list, attribute):
    count_5 = 0
    count_4 = 0
    count_3 = 0
    count_2 = 0
    count_1 = 0
    total_5 = 0
    total_4 = 0
    total_3 = 0
    total_2 = 0
    total_1 = 0
    customer_transaction_list = list
        
    
    for customer in customer_transaction_list:
        if attribute == 1:
            at = customer["recent_num"]
        elif attribute == 2:
            at = customer["frequency_num"]
        else:
            at = customer["amount_num"]

        customer_total = customer["average_spending"]
        if at == 5:
            count_5 += 1
            total_5 += customer_total
        elif at == 4:
            count_4 += 1
            total_4 += customer_total
        elif at == 3:
            count_3 += 1
            total_3 += customer_total
        elif at == 2:
            count_2 += 1
            total_2 += customer_total
        else:
            count_1 += 1
            total_1 += customer_total
    
    average_5 = total_5 / count_5
    average_4 = total_4 / count_4
    average_3 = total_3 / count_3
    average_2 = total_2 / count_2
    average_1 = total_1 / count_1

    return [average_1, average_2, average_3, average_4, average_5]

def create_recent_number(list):
    customer_recent_transaction = list[0]
    recent_day = customer_recent_transaction.delta_date
    if recent_day < 7:
        recent_num = 5
    elif recent_day < 15:
        recent_num = 4
    elif recent_day < 22:
        recent_num = 3
    elif recent_day < 29:
        recent_num = 2
    else:
        recent_num = 1
    return recent_num

def create_frequency_number(list):
    customer_first_transaction = list.reverse()[0]
    first_day = customer_first_transaction.delta_date
    count = 0
    for i in list:
        count += 1
    frquency_day = first_day / count
    if frquency_day < 4:
        frquency_num = 5
    elif frquency_day < 7:
        frquency_num = 4
    elif frquency_day < 10:
        frquency_num = 3
    elif frquency_day < 14:
        frquency_num = 2
    else:
        frquency_num = 1
    return frquency_num


def create_amount_number(list):
    recent_transaction = list [0]
    recent_amount = recent_transaction.transaction_total
    if recent_amount > 1000:
        amount_num = 5
    elif recent_amount > 500:
        amount_num = 4
    elif recent_amount > 300:
        amount_num = 3
    elif recent_amount > 100:
        amount_num = 2
    else:
        amount_num = 1
    return amount_num



def RFM_model_list(request):
    customer_list = Customer.objects.all()

    customer_transaction_list = []

    for cm in customer_list:
        transaction_queryset = cm.transaction_set.order_by('delta_date')
        customer_transaction_list.append({"Customer": cm, "Transaction_Query": transaction_queryset})
    
    
    for customer_t in customer_transaction_list:
        customer_t["recent_num"] = create_recent_number(customer_t["Transaction_Query"])
        customer_t["frequency_num"] = create_frequency_number(customer_t["Transaction_Query"])
        customer_t["amount_num"] = create_amount_number(customer_t["Transaction_Query"])
        customer_t["average_spending"] = customer_avg(customer_t["Transaction_Query"])

    new_list = sorted(customer_transaction_list, key = lambda e:(e.__getitem__('recent_num'), e.__getitem__('frequency_num'), \
                                                                    e.__getitem__('amount_num')))
    
    return render(request, 'watsons/ShowRFM.html', {"customer_transaction_list": new_list})


def RFM_model_group(request):
    customer_list = Customer.objects.all()

    customer_transaction_list = []

    for cm in customer_list:
        transaction_queryset = cm.transaction_set.order_by('delta_date')
        customer_transaction_list.append({"Customer": cm, "Transaction_Query": transaction_queryset})
    
    
    for customer_t in customer_transaction_list:
        customer_t["recent_num"] = create_recent_number(customer_t["Transaction_Query"])
        customer_t["frequency_num"] = create_frequency_number(customer_t["Transaction_Query"])
        customer_t["amount_num"] = create_amount_number(customer_t["Transaction_Query"])
        customer_t["average_spending"] = customer_avg(customer_t["Transaction_Query"])
        customer_t["RFM_num"] = customer_t["recent_num"]*100+customer_t["frequency_num"]*10+customer_t["amount_num"]

    RFM_list = []
    customer_group_list = []
    for t in customer_transaction_list:
        rfm_num = t["RFM_num"]
        temp = {}
        if rfm_num not in RFM_list:
            RFM_list.append(rfm_num)
            temp["RFM_num"] = rfm_num
            temp["TOTAL"] = t["average_spending"]
            temp["count"] = 1
            customer_group_list.append(temp)
        else:
            for i in customer_group_list:
                if i["RFM_num"] == rfm_num:
                    i["count"] += 1
                    i["TOTAL"] += t["average_spending"]
                else:
                    continue

    for item in customer_group_list:
        item["AVG"] = item["TOTAL"] / i["count"] 



    new_group_list = sorted(customer_group_list, key = lambda e:(e.__getitem__('RFM_num')))
    
    return render(request, 'watsons/ShowRFMGroup.html', {"new_group_list": new_group_list})


#RFM Model End 

#Product Index Start

def product_index(request):
 
    return render(request,'watsons/product_index.html',locals())


#Product Index End

#Product list Start

def listall(request):
 
    products = Product.objects.all().order_by('-id') #依據id欄位遞減排序顯示所有資料
    return render(request,'watsons/listall.html',locals())


#Product list End


#Marketing part Start

def servive(request): #存活率
    ser = Servive.objects.order_by('Date')
    r = 1
    n = 100
    period = 0
    day=[]
    se=[]
    for s in ser:
        s.count((s.Num/n), r)
        r = s.servive_rate
        n = s.Num
        period = period+s.respected_customer_num
        day.append(s.Date)
        se.append(r)
    plt.plot(day, se)
    plt.title('Survival rate Graph')
    plt.ylabel('Date')
    plt.xlabel('servive rate')
    plt.show()
    period = period/100
    context = {'ser': ser, 'period': period, }
    return render(request, 'watsons/servive.html', context)


def total_rate(request): #個別錢包佔有率
    poc = Pocket_other.objects.order_by('customer').all()
    poc2 = Pocket_other.objects.order_by('customer')
    cal_rate(poc, poc2)
    context = {'poc2': poc2}
    return render(request, 'watsons/total_rate.html', context)


def rate(request):  #錢包大小
    poc = Pocket_other.objects.order_by('customer').all()
    dict1 = cal_poc(poc)
    context = {'poc': poc}
    context.update(dict1)
    return render(request, 'watsons/rate.html', context)


def cal_poc(poc):  #call function  from  rate,total_rate
    cosmetic = 0
    snacks = 0
    care = 0
    for p in poc:
        p.total_Cosmetic = p.total_Cosmetic*40
        p.total_Snacks = p.total_Snacks*200
        p.total_Care = p.total_Care*120
        cosmetic = cosmetic + p.total_Cosmetic
        snacks = snacks + p.total_Snacks
        care = care + p.total_Care
    dict1 = {'cosmetic': cosmetic, 'snacks': snacks, 'care': care}
    return dict1



 # call function  from  total_rate
def cal_rate(poc1,poc2):
    cost = Customer.objects.all()
    for c in cost:
        tran = Transaction.objects.filter(customer_id=c.id)   # 找到顧客交易資料
        p = poc2.get(customer_id=c.id)
        p1 = poc1.get(customer_id=c.id)                                         # poc1 為此顧客的錢包大小
        p.total_Cosmetic = 0
        p.total_Snacks = 0
        p.total_Care = 0
        for t in tran:                                                             # 找到的交易資訊 依據品類統計
            pro = Product.objects.get(product_name=t.product)
            if pro.category == 'Cosmetic':
                p.total_Cosmetic = p.total_Cosmetic+t.total
            elif pro.category == 'Snacks':
                p.total_Snacks = p.total_Snacks + t.total
            elif pro.category == 'Care Product':
                p.total_Care = p.total_Care + t.total
        p.total_Cosmetic = p.total_Cosmetic/p1.total_Cosmetic                     # 算出顧客在各品類的錢包佔有率
        p.total_Snacks = p.total_Snacks/p1.total_Snacks
        p.total_Care = p.total_Care/p1.total_Care

def home(request): #首頁

    return render(request, 'watsons/home.html', locals())
#Marketing Part End









