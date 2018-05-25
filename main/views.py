from django.shortcuts import render, redirect


def main(request):
    session_key = request.session.session_key
    user_id = request.session['user_id']
    print("Имя пользователя со стороны - ", user_id)

    return render(request, 'main/main.html', locals())