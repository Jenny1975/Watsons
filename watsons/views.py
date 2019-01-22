from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404,\
     redirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from django.db import models
from decimal import Decimal
from .models import Transaction, Product, Customer, Pocket_other, Servive, Promotion, Staff
from .forms import PromotionForm, UploadFileForm
from django.db.models import Avg, Sum, Count
import matplotlib.pyplot as plt
from django.http import JsonResponse
import json
from django.views import generic
from django.conf import settings

import csv
import random
import datetime
import time
import os


NOW =  datetime.datetime.now()

@login_required
def index(request):
    staff = get_object_or_404(Staff, user=request.user)
    
    return render(request, 'watsons/Base.html', {'isManager':staff.isManager})
             
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
@login_required
def showTransaction(request):
    staff = get_object_or_404(Staff, user=request.user)
    allList = Transaction.objects.all()
    yList = Transaction.objects.filter(time__year=2018).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m1 = Transaction.objects.filter(time__year=2018, time__month=1).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m2 = Transaction.objects.filter(time__year=2018, time__month=2).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m3 = Transaction.objects.filter(time__year=2018, time__month=3).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m4 = Transaction.objects.filter(time__year=2018, time__month=4).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m5 = Transaction.objects.filter(time__year=2018, time__month=5).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m6 = Transaction.objects.filter(time__year=2018, time__month=6).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m7 = Transaction.objects.filter(time__year=2018, time__month=7).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m8 = Transaction.objects.filter(time__year=2018, time__month=8).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m9 = Transaction.objects.filter(time__year=2018, time__month=9).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m10 = Transaction.objects.filter(time__year=2018, time__month=10).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m11 = Transaction.objects.filter(time__year=2018, time__month=11).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    m12 = Transaction.objects.filter(time__year=2018, time__month=12).values("product_id").annotate(sales=Sum("amount")).values("product", "sales")
    context = {'allList': allList, 'yList':yList, 'mList': {1: m1, 2: m2, 3: m3, 4: m4, 5: m5, 6: m6, 7: m7, 8: m8, 9: m9, 10: m10, 11: m11, 12: m12}, 'isManager': staff.isManager}
    return render(request, 'watsons/ShowTransaction.html', context)

#Show Transaction End

    
@login_required
def uploadTransaction(request):
    staff = get_object_or_404(Staff, user=request.user)
    f = UploadFileForm()
    return render(request, 'watsons/UploadFile.html', {'f': f, 'isManager':staff.isManager})


def upload_csv(request):
    staff = get_object_or_404(Staff, user=request.user)
    data = {}
    if request.method == 'GET':
        return render(request, "watsons/UploadFile.html", data)
    else:
        csv_file = request.FILES["csv_file"]
        file_data = csv_file.read().decode("utf-8")		

        lines = file_data.split("\n")

        for line in lines[1:]:
            each = line.split(',')
            try:
                if csv_file.name.startswith('P'):
                    c, created = Product.objects.get_or_create(product_name=each[0], 
                                                                category=each[1],
                                                                price=int(each[2]),
                                                                quantity=int(each[3]))
                elif csv_file.name.startswith('C'):
                    c, created = Customer.objects.get_or_create(customer_name=each[0],
                                                                gender=each[1])
                elif each == ['']:
                    break
                else:
                    y = request.POST.get('year')
                    m = request.POST.get('month')
                    d = request.POST.get('day')
                    thisTime = datetime.date(int(y), int(m), int(d))
                    amount = each[2][:-1]
                    c, created = Transaction.objects.get_or_create(customer_id=int(each[0]),
                                                            product_id=int(each[1]),
                                                            time=thisTime,
                                                            amount=int(amount))

                if not created:
                    c.add()
                    c.save()
            except:
                pass


    return render(request, 'watsons/ShowTransaction.html', {'isManager':staff.isManager})


# @login_required
# def readFile(request):

#     save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', request.FILES['file'])
#     path = default_storage.save(save_path, request.FILES['file'])
#     return default_storage.path(path)
# def handle_uploaded_file(f):
#     with open('data/name.csv', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

# def readFile(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         handle_uploaded_file(request.FILES['file'])
#         return redirect('/')
#     else:
#         form = UploadFileForm()
#     return HttpResponse('ijij')





#RFM Model start
def RFM_model(request):
    staff = get_object_or_404(Staff, user=request.user)
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
                                                'dataset_amount' : dataset_amount, 'isManager':staff.isManager})


def customer_avg(customer_query):
    total = 0
    count = 0
    for c in customer_query:
        total += c.transaction_total
        count += 1

    if count == 0:
        average = 0
    else:
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
    staff = get_object_or_404(Staff, user=request.user)
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
    
    return render(request, 'watsons/ShowRFM.html', {"customer_transaction_list": new_list, 'isManager':staff.isManager})


def RFM_model_group(request):
    staff = get_object_or_404(Staff, user=request.user)
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
    
    return render(request, 'watsons/ShowRFMGroup.html', {"new_group_list": new_group_list, 'isManager':staff.isManager})


def get_promotion(request):
    staff = get_object_or_404(Staff, user=request.user)
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            p, created = Promotion.objects.get_or_create(**form.cleaned_data)
            p.save()
            return redirect('watsons:edit_BreakEven')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PromotionForm()


    customer_list = Customer.objects.all()
    promotion = Promotion.objects.order_by('-id')[0]

    customer_transaction_list = []

    promotion_delta = promotion.end_time - promotion.start_time

    for cm in customer_list:
        transaction_queryset = cm.transaction_set.order_by('delta_date')
        transaction_promotion = []
        for t in transaction_queryset:
            if t.time - promotion.start_time < promotion_delta:
                transaction_promotion.append(t)
            else:
                continue

        customer_transaction_list.append({"Customer": cm, "Transaction_Query": transaction_queryset, \
                                        "Transaction_promotion": transaction_promotion})
    
    
    for customer_t in customer_transaction_list:
        customer_t["recent_num"] = create_recent_number(customer_t["Transaction_Query"])
        customer_t["frequency_num"] = create_frequency_number(customer_t["Transaction_Query"])
        customer_t["amount_num"] = create_amount_number(customer_t["Transaction_Query"])
        customer_t["promotion_average_spending"] = customer_avg(customer_t["Transaction_promotion"])
        customer_t["RFM_num"] = customer_t["recent_num"]*100+customer_t["frequency_num"]*10+customer_t["amount_num"]

    RFM_list = []
    customer_group_list = []
    for t in customer_transaction_list:
        rfm_num = t["RFM_num"]
        temp = {}
        if rfm_num not in RFM_list:
            RFM_list.append(rfm_num)
            temp["RFM_num"] = rfm_num
            temp["TOTAL"] = t["promotion_average_spending"]
            temp["count"] = 1
            customer_group_list.append(temp)
        else:
            for i in customer_group_list:
                if i["RFM_num"] == rfm_num:
                    i["count"] += 1
                    i["TOTAL"] += t["promotion_average_spending"]
                else:
                    continue

    avg_cost = promotion.amount/len(customer_list)
    
    for item in customer_group_list:
        item["AVG"] = item["TOTAL"] / i["count"] 
        item["BreakEven_Index"] = (item["AVG"] - avg_cost)*100 / avg_cost



    new_group_list = sorted(customer_group_list, key = lambda e:(e.__getitem__('RFM_num')))

    return render(request, 'watsons/EditBreakEven.html', {'form': form, "new_group_list": new_group_list, 'isManager':staff.isManager})

def BreakEven(request):
    staff = get_object_or_404(Staff, user=request.user)
    customer_list = Customer.objects.all()
    promotion = Promotion.objects.order_by('-id')[0]

    customer_transaction_list = []

    promotion_delta = promotion.end_time - promotion.start_time

    for cm in customer_list:
        transaction_queryset = cm.transaction_set.order_by('delta_date')
        transaction_promotion = []
        for t in transaction_queryset:
            if t.time - promotion.start_time < promotion_delta:
                transaction_promotion.append(t)
            else:
                continue

        customer_transaction_list.append({"Customer": cm, "Transaction_Query": transaction_queryset, \
                                        "Transaction_promotion": transaction_promotion, 'isManager':staff.isManager})
    
    
    for customer_t in customer_transaction_list:
        customer_t["recent_num"] = create_recent_number(customer_t["Transaction_Query"])
        customer_t["frequency_num"] = create_frequency_number(customer_t["Transaction_Query"])
        customer_t["amount_num"] = create_amount_number(customer_t["Transaction_Query"])
        customer_t["promotion_average_spending"] = customer_avg(customer_t["Transaction_promotion"])
        customer_t["RFM_num"] = customer_t["recent_num"]*100+customer_t["frequency_num"]*10+customer_t["amount_num"]

    RFM_list = []
    customer_group_list = []
    for t in customer_transaction_list:
        rfm_num = t["RFM_num"]
        temp = {}
        if rfm_num not in RFM_list:
            RFM_list.append(rfm_num)
            temp["RFM_num"] = rfm_num
            temp["TOTAL"] = t["promotion_average_spending"]
            temp["count"] = 1
            customer_group_list.append(temp)
        else:
            for i in customer_group_list:
                if i["RFM_num"] == rfm_num:
                    i["count"] += 1
                    i["TOTAL"] += t["promotion_average_spending"]
                else:
                    continue

    avg_cost = promotion.amount/len(customer_list)
    
    for item in customer_group_list:
        item["AVG"] = item["TOTAL"] / i["count"] 
        item["BreakEven_Index"] = (item["AVG"] - avg_cost)*100 / avg_cost



    new_group_list = sorted(customer_group_list, key = lambda e:(e.__getitem__('RFM_num')))
    
    return render(request, 'watsons/BreakEvenList.html', {"new_group_list": new_group_list, 'isManager':staff.isManager})


def Association_Rule(request):
    staff = get_object_or_404(Staff, user=request.user)
    customer_list = Customer.objects.all()

    customer_transaction_list = []
    Association_list = []
    
    for cm in customer_list:
        double_time = cm.transaction_set.values('time').annotate(time_count = Count('time'))
        for d in double_time:
            if d['time_count'] > 1:
                product = cm.transaction_set.filter('time' == d['time'])
                if product not in Association_list:
                    Association_list.append({'Product': product, 'Count' : 1})
                else:
                    for p in Association_list:
                        if p['Product'] == product:
                            p['Count'] += 1
                        else:
                            continue
            else:
                continue

        customer_transaction_list.append({'Customer': cm, 'time': double_time})

    
    return render(request, 'watsons/Association.html', {"Association_list": Association_list, 'isManager':staff.isManager})




#RFM Model End 

#Product Index Start

def product_index(request):
    staff = get_object_or_404(Staff, user=request.user)
 
    return render(request,'watsons/product_index.html',locals())


#Product Index End

#Product list Start

def listall(request):
    staff = get_object_or_404(Staff, user=request.user)
 
    products = Product.objects.all().order_by('-id') #依據id欄位遞減排序顯示所有資料
    return render(request,'watsons/listall.html',locals())


#Product list End

#Product listone Start

def listone(request):
    staff = get_object_or_404(Staff, user=request.user)
    try:
        unit = Product.objects.get(product_id="100010001") #讀取第一筆資料
    except:
        errormessage = "(讀取錯誤!)"
    return render(request,'watsons/listone.html',locals())

#Product listone End

#Product listless Start

def listless(request):
    staff = get_object_or_404(Staff, user=request.user)
    try:

        unit1 = Product.objects.get(id = 5) #讀取前兩筆資料
        unit2 = Product.objects.get(id = 5)
        unit3 = Product.objects.get(id = 5)
        unit4 = Product.objects.get(id = 5)
        unit5 = Product.objects.get(id = 5)

        product_dict = [unit1, unit2, unit3, unit4, unit5]
          #讀取前兩筆資料
        
    except:
        errormessage = "(讀取錯誤!)"
    return render(request,'watsons/listless.html',{'product_list':product_dict, 'isManager':staff.isManager})

#Product listless End

#Marketing part Start

def servive(request): #存活率
    staff = get_object_or_404(Staff, user=request.user)
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
    staff = get_object_or_404(Staff, user=request.user)
    poc = Pocket_other.objects.order_by('customer').all()
    dict1 = cal_poc(poc)
    poc2 = poc
    cal_rate(poc2)
    context = {'poc2': poc2}
    return render(request, 'watsons/total_rate.html', context)


def rate(request):  #錢包大小
    staff = get_object_or_404(Staff, user=request.user)
    poc = Pocket_other.objects.order_by('customer').all()
    dict1 = cal_poc(poc)
    context = {'poc': poc}
    context.update(dict1)
    return render(request, 'watsons/rate.html', {'context': context, 'isManager':staff.isManager})


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
    dict1 = {'cosmetic': cosmetic, 'snacks': snacks, 'care': care, 'isManager':staff.isManager}
    return dict1



 # call function  from  total_rate
def cal_rate(poc2):
    for p in poc2:
        try:
            p.total_Cosmetic = round(80 / p.total_Cosmetic,2)
        except ZeroDivisionError:
            p.total_Cosmetic = 0
        try:
            p.total_Snacks = round(440 / p.total_Snacks,2)
        except ZeroDivisionError:
            p.total_Snacks = 0
        try:
            p.total_Care = round(80 / p.total_Care,2)
        except ZeroDivisionError:
            p.total_Care = 0

    return poc2
#Marketing Part End






