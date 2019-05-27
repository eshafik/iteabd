from django.contrib.auth.decorators import login_required, user_passes_test

from account.models import Profile


# Custom decorator for checking finance user
finance_login_required = user_passes_test(lambda user: user.profile.finance,
                                          login_url='/')

def finance_user_required(view_func):
    decorated_view_func = login_required(finance_login_required(view_func))

    return decorated_view_func



# Cutom decorator for checking executive user
executive_login_required = user_passes_test(lambda u: True if 
                                            u.profile.is_executive else False,
                                            login_url='/')

def executive_user_required(view_func):
    decorated_view_func = login_required(executive_login_required(view_func),
                                         login_url='/')
    return decorated_view_func


#personal decorator just for saving
# def is_recruiter(self):
#     if str(self.user_type) == 'Recruiter':
#         return True
#     else:
#         return False
# rec_login_required = user_passes_test(lambda u: True if u.is_recruiter else False, login_url='/')

# def recruiter_login_required(view_func):
#     decorated_view_func = login_required(rec_login_required(view_func), login_url='/')
#     return decorated_view_func

# @recruiter_login_required
# def index(request):
#     return render(request, 'index.html')