import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from django.utils import dateformat
from django.db.models import Sum, Max
from django.core.cache import cache

from .custom_decorator import finance_user_required, executive_user_required
from .models import IndividualBalance, OrganizationBalance, InvestorBalance
from .forms import IndividualBalanceForm, OrganizationBalanceForm,\
                    DateForm, InvestorBalanceForm
from account.models import Profile
from .utils import render_to_pdf
from .tasks import balance_added


def get_due_month(d1, d2):
    return d1.month - d2.month + 12*(d1.year - d2.year)

@finance_user_required
def add_balance(request, username):
    user = get_object_or_404(User, username=username)
    try:
        total_balance = user.balances.aggregate(Sum('balance'))
        total_balance = total_balance['balance__sum']
        due = getattr(user.balances.latest('id'), 'due_month')
    except:
        due = 0
        total_balance = 0

    if request.method=='POST':
        balance_form = IndividualBalanceForm(data=request.POST)
        if balance_form.is_valid():
            amount = balance_form.cleaned_data['add_balance']
            additional = balance_form.cleaned_data['additonal']
            due_month = balance_form.cleaned_data['due_month']
            details = balance_form.cleaned_data['details']
            # date_now = datetime.datetime.now()
            # try:
            #     obj = IndividualBalance.objects.filter(user=user).latest('id')
            #     date_previous = getattr(obj, 'updated')
            # except:
            #     date_previous = date_now
            # due = get_due_month(date_now, date_previous)
            IndividualBalance.objects.create(user=user, balance=amount,
                                             additional=additional,
                                             due_month= due_month,
                                             payment_details= details)
            balance_added.delay(user.id)
            messages.success(request,'Balance updated successfully.')
            return redirect('balance:active_members')
        else:
            messages.error(request,'Error updating your Balance.')
    else:
        balance_form = IndividualBalanceForm()

    return render(request, 'balance/individual_balance.html',
                  {'balance_form': balance_form, 'user':user, 'total_balance': total_balance, 'due': due})
    

@finance_user_required
def active_members(request):
    members = User.objects.annotate(total_balance=Sum('balances__balance'), additional_balance=Sum('balances__additional'), updated=Max('balances__updated'))
    return render(request,'balance/active_members.html', {'members':members})

def org_calculation(start=None, end=None):
    try:
        if start and end:
            if start==end:
                org_all = OrganizationBalance.objects.filter(updated__date=start)
            else:
                org_all = OrganizationBalance.objects.filter(updated__date__range=[start, end])
        else:
            org_all = OrganizationBalance.objects.all()
        

        invest_expense = org_all.aggregate(Sum('invest_expense'))
        invest_income = org_all.aggregate(Sum('invest_income'))
        extra_expense = org_all.aggregate(Sum('extra_expense'))
        extra_income = org_all.aggregate(Sum('extra_income'))
        equity_all = IndividualBalance.objects.all()
        member_equity_monthly = equity_all.aggregate(Sum('balance'))
        member_equity_additional = equity_all.aggregate(Sum('additional'))
        latest_org_obj = org_all.latest('id')
        latest_updated = getattr(latest_org_obj, 'updated')
        investor_invest = InvestorBalance.objects.all().aggregate(Sum('balance'))

        context_data = {
            'invest_income': invest_income,
            'invest_expense': invest_expense,
            'extra_expense': extra_expense,
            'extra_income': extra_income,
            'equity_monthly': member_equity_monthly,
            'equity_additional': member_equity_additional,
            'updated': latest_updated,
            'org_trans': org_all,
            'invest': investor_invest
        }
        return context_data
    except:
        pass

@login_required
def org_detail(request):
    context_data = org_calculation()
    
    return render(request,'balance/org_detail.html', context_data)

@executive_user_required
def org_transaction(request):
    if request.method == "POST":

        dateForm = DateForm(request.POST)
        if dateForm.is_valid():
            #clean date range from the form
            start = dateForm.cleaned_data['start']
            end = dateForm.cleaned_data['end']

            context_data = org_calculation(start, end)
                
            return render(request,'balance/org_transaction_data.html', context_data)
    else:
        dateForm = DateForm()
    return render(request, 'balance/date_pic.html', {'form': dateForm})

   

@finance_user_required
def org_edit(request):
    
    if request.method == 'POST':
        org_form = OrganizationBalanceForm(data=request.POST)
        if org_form.is_valid():
            invest_expense = org_form.cleaned_data['invest_expense']
            invest_income = org_form.cleaned_data['invest_income']
            extra_expense = org_form.cleaned_data['extra_expense']
            extra_income = org_form.cleaned_data['extra_income']
            investment_details = org_form.cleaned_data['details']

            OrganizationBalance.objects.create(invest_expense=invest_expense,
                                               invest_income=invest_income,
                                               extra_expense=extra_expense,
                                               extra_income=extra_income,
                                               investment_details=investment_details)
            messages.success(request, 'Organization Status edited successfully.')
            return redirect('balance:org_detail')
        else:
             messages.error(request, 'Error editing your Organization Status.')
    else:
        org_form = OrganizationBalanceForm()

    return render(request,'balance/org_edit.html', {'org_form':org_form})
        
@executive_user_required       
def transaction(request):
    if request.method == "POST":
        result_list = []
        amount_list = []
        dateForm = DateForm(request.POST)
        if dateForm.is_valid():
            #clean date range from the form
            start = dateForm.cleaned_data['start']
            end = dateForm.cleaned_data['end']
            if start==end:
                qs = IndividualBalance.objects.filter(updated__date=start)
                users = User.objects.all()
                # for loop for every member transaction serially designed
                for user in users:
                    result_list.append(qs.filter(user=user))

                # for loop for every member total amount serially
                for result in result_list:
                    temp_amount = result.aggregate(Sum('balance'))
                    amount_list.append(temp_amount['balance__sum'])

                results = result_list
                g_amount = amount_list
                cache.set('results', results)
                cache.set('g_amount', g_amount)
                # result = zip(result_list, amount_list)
            else:
                qs = IndividualBalance.objects.filter(updated__date__range=[start, end])
                users = User.objects.all()
                for user in users:
                    result_list.append(qs.filter(user=user))
                
                # for loop for every member total amount serially
                for result in result_list:
                    temp_amount = result.aggregate(Sum('balance'))
                    amount_list.append(temp_amount['balance__sum'])

                results = result_list
                g_amount = amount_list
                # result = zip(result_list, amount_list)
                cache.set('results', results)
                cache.set('g_amount', g_amount)
            return render(request,'balance/transaction_data.html',{'users':results, 'amounts': g_amount})
    else:
        dateForm = DateForm()
    return render(request, 'balance/date_pic.html', {'form': dateForm})



class GeneratePdf(View):

    def get(self, request, *args, **kwargs):
        template = get_template('balance/pdf.html')
        context = {
            'users': cache.get('results'),
            'amounts': cache.get('g_amount'),
        }
        html = template.render(context)
        pdf = render_to_pdf('balance/pdf.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "transaction_%s.pdf" %(dateformat.format(datetime.datetime.now(), 'F_j_Y_P'))
            # filename = "Transaction"
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


@login_required
def personal_transaction(request):
    my_trans = IndividualBalance.objects.filter(user=request.user)

    return render(request, 'balance/personal_transaction.html', {'my_trans': my_trans})


@login_required
def investor_add_balance(request):
    if request.method=='POST':
        investor_form = InvestorBalanceForm(data=request.POST)
        if investor_form.is_valid():
            name = investor_form.cleaned_data['name']
            balance = investor_form.cleaned_data['amount']

            InvestorBalance.objects.create(name=name, balance=balance)

            messages.success(request, 'Amount of investor is added successfully.')
            return redirect('balance:investor_trans')

        else:
            messages.error(request, 'Error adding investor amount.')
    else:
        investor_form = InvestorBalanceForm()
    
    return render(request, 'balance/investor_form.html', {'investor_form': investor_form})


@login_required
def investor_transaction(requesst):
    try:
        all_invest = InvestorBalance.objects.all()
        return render(requesst, 'balance/investor_trans.html', {'all_invest': all_invest})
        
    except:
        pass