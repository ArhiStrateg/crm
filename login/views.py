from django.shortcuts import render, redirect
from login.forms import Login_Form
from login.models import User_Login


def login(request):
    no_show_navbar = True
    session_key = request.session.session_key

    form = Login_Form(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form = form.cleaned_data

            name_login = form["name_login"]
            password_login = form["password_login"]

            all_users = User_Login.objects.filter()
            for user in all_users:
                if user.name_login == name_login and user.password_login == password_login:

                    User_Login.objects.filter(id=user.id, name_login=name_login, password_login=password_login).update(session_key_login=session_key)

                    print("Осуществляем вход")
                    login_site = True;
                    request.session['user_id'] = user.id

                    return redirect('main')



    return render(request, 'login/general.html', locals())
