from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,\
                                urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.db.models import Sum

from .forms import UserRegistrationForm,\
                    UserEditForm,\
                    ProfileEditForm
from blog.forms import SearchForm
from . tokens import account_activation_token
from .models import Profile
from balance.models import IndividualBalance,\
                            OrganizationBalance


@login_required
def dashboard(request):

    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password2'])
            new_user.is_active = False #For email verificaiton
            new_user.save()
            #Create user profile
            Profile.objects.create(user=new_user)
            IndividualBalance.objects.create(user=new_user)
            #for email verification
            current_stie = get_current_site(request)
            mail_subject = 'Activate your ITEA account.'
            message = render_to_string('account/acc_active_email.html', {
                'user': new_user,
                'domain': current_stie.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.id)).decode(),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return HttpResponse('Please confirm your email address to complete the registration.')
    else:
        user_form = UserRegistrationForm()

    return render(request,'account/register.html', {'user_form': user_form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 
    if user is not None and account_activation_token.check_token(user, token):
        user.is_activate = True
        user.save()
        # login(request,user, backend='account.authentication.EmailAuthBackend',)

        return redirect('blog:post_list')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
        



@login_required
def profile_details(request, username):
    user = get_object_or_404(User, username=username)

    # Query monthly balance and addtional and due month
    current_obj = IndividualBalance.objects.filter(user=request.user)
    monthly_balance = current_obj.aggregate(Sum('balance'))
    monthly_balance = monthly_balance['balance__sum']
    additional_balance = current_obj.aggregate(Sum('additional'))
    additional_balance = additional_balance['additional__sum']
    due_month = getattr(current_obj.last(), 'due_month' )
    updated = getattr(current_obj.last(), 'updated' )

    contex_data = {
        'user': user,
        'monthly_balance': monthly_balance,
        'additional_balance': additional_balance,
        'due_month': due_month,
        'updated': updated,

    }
    return render(request, 'account/profile_details.html', contex_data)

@login_required
def edit(request):
    if request.method=='POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')

            return redirect('profile_details', username=request.user)
        else:
            messages.error(request,'Error updating your profile.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def all_members(request):
    members = Profile.objects.all()

    return render(request, 'account/all_members.html',{'members': members})
