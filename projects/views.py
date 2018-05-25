from django.shortcuts import render, redirect
from projects.forms import Form_Create_New_Project, Form_Create_New_SUBProject
from projects.models import Prime_Project, Data_Prime_Project, Sub_Project, Sub_Project_Prime_Data, Sub_Project_Sub_Data, \
    Incom, Outcom, Incom_Data, Outcom_Data, Comment_For_Project, File_For_Comment, File_For_Project, Contacts, Data_Contacts, \
    File_Incom_Data, File_Outcom_Data
from login.models import User_Login

import datetime as dt
from datetime import datetime, date


def projects(request):
    list_all_active_project = list()
    all_prime_projects_active = Data_Prime_Project.objects.filter(archiv_project=False)
    for all_prime_project_active in all_prime_projects_active:
        date = all_prime_project_active.date_create_project
        date_strt = all_prime_project_active.date_start_project
        date_dld = all_prime_project_active.date_deadline_project

        strt_prj = datetime.toordinal(date_strt)
        dld_prj = datetime.toordinal(date_dld)
        now_prg = datetime.toordinal(datetime.now())
        days_proj = dld_prj - strt_prj
        days_now = now_prg - strt_prj

        proc_ras = (days_now * 100) / days_proj

        project_activ = dict(project=all_prime_project_active,  proc_ras=round(proc_ras),
                             year_cr=date.strftime("%Y"), mouth_cr=date.strftime("%B"), data_cr=date.strftime("%d"),
                             year_strt=date_strt.strftime("%Y"), mouth_strt=date_strt.strftime("%B"), data_strt=date_strt.strftime("%d"),
                             year_dld=date_dld.strftime("%Y"), mouth_dld=date_dld.strftime("%B"), data_dld=date_dld.strftime("%d"),
                             status_1=all_prime_project_active.prime_project.status_1,
                             status_2=all_prime_project_active.prime_project.status_2,
                             status_3=all_prime_project_active.prime_project.status_3,
                             status_4=all_prime_project_active.prime_project.status_4,
                             status_5=all_prime_project_active.prime_project.status_5,
                             status_6=all_prime_project_active.prime_project.status_6,)
        list_all_active_project.append(project_activ)

    all_prime_projects_archive = Data_Prime_Project.objects.filter(archiv_project=True)



    return render(request, 'projects/projects.html', locals())


def create_new_project(request):
    session_key = request.session.session_key
    who_create = request.session['user_id']
    who_create_project = User_Login.objects.get(id=int(who_create))

    form_new_project = Form_Create_New_Project(request.POST or None)
    if request.method == "POST":
        if form_new_project.is_valid():
            form_new_project = form_new_project.cleaned_data

            name_create_project = form_new_project["name"]
            description_create_project = form_new_project["description_project"]
            who_boss_project = form_new_project["who_boss_project"]
            date_start_project= form_new_project["date_start_project"]
            date_deadline_project = form_new_project["date_deadline_project"]

            create_prime = Prime_Project.objects.create(name_project=form_new_project["name"], description_project=form_new_project["description_project"],
                                         who_create_project=who_create_project, status_1=True)

            Data_Prime_Project.objects.create(prime_project=create_prime, key_yacor_project="#pp"+str(create_prime.id),
                                              who_boss_project=form_new_project["who_boss_project"], date_start_project=form_new_project["date_start_project"],
                                              date_deadline_project=form_new_project["date_deadline_project"])

            return redirect('projects')

    return render(request, 'projects/create_new_project.html', locals())


def finaciar(request, project_id):
    session_key = request.session.session_key
    prime = Data_Prime_Project.objects.get(prime_project__id=project_id)

    # Data for incom - HTML (Begin)
    all_outcom_in_prime_project_status_1 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_1=True)
    outcom_summ_status_1 = 0
    list_for_outcom_status_1 = list()
    for outcom_simple in all_outcom_in_prime_project_status_1:
        outcom_summ_status_1 = outcom_summ_status_1 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        all_files = File_Outcom_Data.objects.filter(local_key__local_key__id=outcom_simple.local_key.id, local_key__local_key__status_1=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_outcom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=outcom_simple.local_key.id, outcom_sim=outcom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_outcom_status_1.append(dict_for_save)

    all_outcom_in_prime_project_status_2 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_2=True)
    outcom_summ_status_2 = 0
    list_for_outcom_status_2 = list()
    for outcom_simple in all_outcom_in_prime_project_status_2:
        outcom_summ_status_2 = outcom_summ_status_2 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        all_files = File_Outcom_Data.objects.filter(local_key__local_key__id=outcom_simple.local_key.id, local_key__local_key__status_2=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_outcom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=outcom_simple.local_key.id, outcom_sim=outcom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_outcom_status_2.append(dict_for_save)

    all_outcom_in_prime_project_status_3 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_3=True)
    outcom_summ_status_3 = 0
    list_for_outcom_status_3 = list()
    for outcom_simple in all_outcom_in_prime_project_status_3:
        outcom_summ_status_3 = outcom_summ_status_3 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        all_files = File_Outcom_Data.objects.filter(local_key__local_key__id=outcom_simple.local_key.id, local_key__local_key__status_3=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_outcom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=outcom_simple.local_key.id, outcom_sim=outcom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_outcom_status_3.append(dict_for_save)

    all_outcom_in_prime_project_status_4 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_4=True)
    outcom_summ_status_4 = 0
    list_for_outcom_status_4 = list()
    for outcom_simple in all_outcom_in_prime_project_status_4:
        outcom_summ_status_4 = outcom_summ_status_4 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        all_files = File_Outcom_Data.objects.filter(local_key__local_key__id=outcom_simple.local_key.id, local_key__local_key__status_4=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_outcom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=outcom_simple.local_key.id, outcom_sim=outcom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_outcom_status_4.append(dict_for_save)

    all_outcom_in_prime_project_status_5 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_5=True)
    outcom_summ_status_5 = 0
    list_for_outcom_status_5 = list()
    for outcom_simple in all_outcom_in_prime_project_status_5:
        outcom_summ_status_5 = outcom_summ_status_5 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        all_files = File_Outcom_Data.objects.filter(local_key__local_key__id=outcom_simple.local_key.id, local_key__local_key__status_5=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_outcom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=outcom_simple.local_key.id, outcom_sim=outcom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_outcom_status_5.append(dict_for_save)

    all_outcom_in_prime_project_status_6 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_6=True)
    outcom_summ_status_6 = 0
    list_for_outcom_status_6 = list()
    for outcom_simple in all_outcom_in_prime_project_status_6:
        outcom_summ_status_6 = outcom_summ_status_6 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        all_files = File_Outcom_Data.objects.filter(local_key__local_key__id=outcom_simple.local_key.id, local_key__local_key__status_6=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_outcom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=outcom_simple.local_key.id, outcom_sim=outcom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_outcom_status_6.append(dict_for_save)

    # Data for price (no_in) - HTML (Begin)
    project_for_main = Prime_Project.objects.get(id=project_id)
    if project_for_main.status_1 == True:
        view_for = "1"
        sum_outcom = outcom_summ_status_1
    if project_for_main.status_2 == True:
        view_for = "2"
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2
    if project_for_main.status_3 == True:
        view_for = "3"
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3
    if project_for_main.status_4 == True:
        view_for = "4"
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4
    if project_for_main.status_5 == True:
        view_for = "5"
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4 + outcom_summ_status_5
    if project_for_main.status_6 == True:
        view_for = "6"
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4 + outcom_summ_status_5 + outcom_summ_status_6

    form_button = request.POST
    form_file = request.FILES
    print(request.POST)
    print(request.FILES)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if elem_str != "csrfmiddlewaretoken":
                if "del_file_for_stat_1_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_1_", "")
                    id = int(recult_rep)
                    File_Outcom_Data.objects.filter(id=id).delete()
                    return redirect('finaciar', project_id)

                if "del_file_for_stat_2_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_2_", "")
                    id = int(recult_rep)
                    File_Outcom_Data.objects.filter(id=id).delete()
                    return redirect('finaciar', project_id)

                if "del_file_for_stat_3_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_3_", "")
                    id = int(recult_rep)
                    File_Outcom_Data.objects.filter(id=id).delete()
                    return redirect('finaciar', project_id)

                if "del_file_for_stat_4_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_4_", "")
                    id = int(recult_rep)
                    File_Outcom_Data.objects.filter(id=id).delete()
                    return redirect('finaciar', project_id)

                if "del_file_for_stat_5_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_5_", "")
                    id = int(recult_rep)
                    File_Outcom_Data.objects.filter(id=id).delete()
                    return redirect('finaciar', project_id)

                if "del_file_for_stat_6_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_6_", "")
                    id = int(recult_rep)
                    File_Outcom_Data.objects.filter(id=id).delete()
                    return redirect('finaciar', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_1_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_1_", "")
                id_reload_file_stat_1 = elem_str.replace("reload_description_for_file_stat_1_", "")
                if id_reload_file_stat_1 == id_in_file:
                    new_data_reload = File_Outcom_Data.objects.get(id=id_reload_file_stat_1)
                    name_form_button = "reload_description_for_file_stat_1_" + str(id_reload_file_stat_1)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_1_" + str(id_reload_file_stat_1)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_1).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Outcom_Data.objects.get(id=id_reload_file_stat_1)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_1).delete()
                        File_Outcom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finaciar', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_2_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_2_", "")
                id_reload_file_stat_2 = elem_str.replace("reload_description_for_file_stat_2_", "")
                if id_reload_file_stat_2 == id_in_file:
                    new_data_reload = File_Outcom_Data.objects.get(id=id_reload_file_stat_2)
                    name_form_button = "reload_description_for_file_stat_2_" + str(id_reload_file_stat_2)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_2_" + str(id_reload_file_stat_2)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_2).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Outcom_Data.objects.get(id=id_reload_file_stat_2)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_2).delete()
                        File_Outcom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finaciar', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_3_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_3_", "")
                id_reload_file_stat_3 = elem_str.replace("reload_description_for_file_stat_3_", "")
                if id_reload_file_stat_3 == id_in_file:
                    new_data_reload = File_Outcom_Data.objects.get(id=id_reload_file_stat_3)
                    name_form_button = "reload_description_for_file_stat_3_" + str(id_reload_file_stat_3)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_3_" + str(id_reload_file_stat_3)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_3).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Outcom_Data.objects.get(id=id_reload_file_stat_3)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_3).delete()
                        File_Outcom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finaciar', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_4_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_4_", "")
                id_reload_file_stat_4 = elem_str.replace("reload_description_for_file_stat_4_", "")
                if id_reload_file_stat_4 == id_in_file:
                    new_data_reload = File_Outcom_Data.objects.get(id=id_reload_file_stat_4)
                    name_form_button = "reload_description_for_file_stat_4_" + str(id_reload_file_stat_4)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_4_" + str(id_reload_file_stat_4)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_4).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Outcom_Data.objects.get(id=id_reload_file_stat_4)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_4).delete()
                        File_Outcom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finaciar', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_5_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_5_", "")
                id_reload_file_stat_5 = elem_str.replace("reload_description_for_file_stat_5_", "")
                if id_reload_file_stat_5 == id_in_file:
                    new_data_reload = File_Outcom_Data.objects.get(id=id_reload_file_stat_5)
                    name_form_button = "reload_description_for_file_stat_5_" + str(id_reload_file_stat_5)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_5_" + str(id_reload_file_stat_5)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_5).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Outcom_Data.objects.get(id=id_reload_file_stat_5)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_5).delete()
                        File_Outcom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finaciar', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_6_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_6_", "")
                id_reload_file_stat_6 = elem_str.replace("reload_description_for_file_stat_6_", "")
                if id_reload_file_stat_6 == id_in_file:
                    new_data_reload = File_Outcom_Data.objects.get(id=id_reload_file_stat_6)
                    name_form_button = "reload_description_for_file_stat_6_" + str(id_reload_file_stat_6)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_6_" + str(id_reload_file_stat_6)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_6).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Outcom_Data.objects.get(id=id_reload_file_stat_6)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Outcom_Data.objects.filter(id=id_reload_file_stat_6).delete()
                        File_Outcom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finaciar', project_id)

    if "description_for_file_stat_1_add" in form_button and form_button["description_for_file_stat_1_add"] != []:
        for elem in form_file:
            if "files_for_stat_1_add_id_" in elem:
                id_outcom_for_stat_1 = int(elem.replace("files_for_stat_1_add_id_", ""))
                outcom_for_save_files = Outcom_Data.objects.filter(local_key__id=id_outcom_for_stat_1)
                for outcom_for_save_file in outcom_for_save_files:
                    break
                name = "files_for_stat_1_add_id_" + str(id_outcom_for_stat_1)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_1_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Outcom_Data.objects.create(local_key=outcom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finaciar', project_id)

    if "description_for_file_stat_2_add" in form_button and form_button["description_for_file_stat_2_add"] != []:
        for elem in form_file:
            if "files_for_stat_2_add_id_" in elem:
                id_outcom_for_stat_2 = int(elem.replace("files_for_stat_2_add_id_", ""))
                outcom_for_save_files = Outcom_Data.objects.filter(local_key__id=id_outcom_for_stat_2)
                for outcom_for_save_file in outcom_for_save_files:
                    break
                name = "files_for_stat_2_add_id_" + str(id_outcom_for_stat_2)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_2_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Outcom_Data.objects.create(local_key=outcom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finaciar', project_id)

    if "description_for_file_stat_3_add" in form_button and form_button["description_for_file_stat_3_add"] != []:
        for elem in form_file:
            if "files_for_stat_3_add_id_" in elem:
                id_outcom_for_stat_3 = int(elem.replace("files_for_stat_3_add_id_", ""))
                outcom_for_save_files = Outcom_Data.objects.filter(local_key__id=id_outcom_for_stat_3)
                for outcom_for_save_file in outcom_for_save_files:
                    break
                name = "files_for_stat_3_add_id_" + str(id_outcom_for_stat_3)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_3_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Outcom_Data.objects.create(local_key=outcom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finaciar', project_id)

    if "description_for_file_stat_4_add" in form_button and form_button["description_for_file_stat_4_add"] != []:
        for elem in form_file:
            if "files_for_stat_4_add_id_" in elem:
                id_outcom_for_stat_4 = int(elem.replace("files_for_stat_4_add_id_", ""))
                outcom_for_save_files = Outcom_Data.objects.filter(local_key__id=id_outcom_for_stat_4)
                for outcom_for_save_file in outcom_for_save_files:
                    break
                name = "files_for_stat_4_add_id_" + str(id_outcom_for_stat_4)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_4_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Outcom_Data.objects.create(local_key=outcom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finaciar', project_id)

    if "description_for_file_stat_5_add" in form_button and form_button["description_for_file_stat_5_add"] != []:
        for elem in form_file:
            if "files_for_stat_5_add_id_" in elem:
                id_outcom_for_stat_5 = int(elem.replace("files_for_stat_5_add_id_", ""))
                outcom_for_save_files = Outcom_Data.objects.filter(local_key__id=id_outcom_for_stat_5)
                for outcom_for_save_file in outcom_for_save_files:
                    break
                name = "files_for_stat_5_add_id_" + str(id_outcom_for_stat_5)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_5_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Outcom_Data.objects.create(local_key=outcom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finaciar', project_id)

    if "description_for_file_stat_6_add" in form_button and form_button["description_for_file_stat_6_add"] != []:
        for elem in form_file:
            if "files_for_stat_6_add_id_" in elem:
                id_outcom_for_stat_6 = int(elem.replace("files_for_stat_6_add_id_", ""))
                outcom_for_save_files = Outcom_Data.objects.filter(local_key__id=id_outcom_for_stat_6)
                for outcom_for_save_file in outcom_for_save_files:
                    break
                name = "files_for_stat_6_add_id_" + str(id_outcom_for_stat_6)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_6_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Outcom_Data.objects.create(local_key=outcom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finaciar', project_id)

    if "description_for_stat_1" in form_button and form_button["description_for_stat_1"] != []:
        if "inc_for_stat_1" in form_button and form_button["inc_for_stat_1"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_1"]
            description = form_button["description_for_stat_1"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_1 = True
            add_stat_1 = Outcom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_1=status_1)
            add_data_stat_1 = Outcom_Data.objects.create(local_key=add_stat_1, who_update=who_create, date_update=add_stat_1.date_create)
            if "description_for_file_stat_1" in form_button and form_button["description_for_file_stat_1"] != []:
                if "files_for_stat_1" in form_file and form_file["files_for_stat_1"] != []:
                    local_key = add_data_stat_1
                    file = form_file["files_for_stat_1"]
                    description_file = form_button["description_for_file_stat_1"]
                    File_Outcom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finaciar', project_id)

    if "description_for_stat_2" in form_button and form_button["description_for_stat_2"] != []:
        if "inc_for_stat_2" in form_button and form_button["inc_for_stat_2"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_2"]
            description = form_button["description_for_stat_2"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_2 = True
            add_stat_2 = Outcom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_2=status_2)
            add_data_stat_2 = Outcom_Data.objects.create(local_key=add_stat_2, who_update=who_create, date_update=add_stat_2.date_create)
            if "description_for_file_stat_2" in form_button and form_button["description_for_file_stat_2"] != []:
                if "files_for_stat_2" in form_file and form_file["files_for_stat_2"] != []:
                    local_key = add_data_stat_2
                    file = form_file["files_for_stat_2"]
                    description_file = form_button["description_for_file_stat_2"]
                    File_Outcom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finaciar', project_id)

    if "description_for_stat_3" in form_button and form_button["description_for_stat_3"] != []:
        if "inc_for_stat_3" in form_button and form_button["inc_for_stat_3"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_3"]
            description = form_button["description_for_stat_3"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_3 = True
            add_stat_3 = Outcom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_3=status_3)
            add_data_stat_3 = Outcom_Data.objects.create(local_key=add_stat_3, who_update=who_create, date_update=add_stat_3.date_create)
            if "description_for_file_stat_3" in form_button and form_button["description_for_file_stat_3"] != []:
                if "files_for_stat_3" in form_file and form_file["files_for_stat_3"] != []:
                    local_key = add_data_stat_3
                    file = form_file["files_for_stat_3"]
                    description_file = form_button["description_for_file_stat_3"]
                    File_Outcom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finaciar', project_id)

    if "description_for_stat_4" in form_button and form_button["description_for_stat_4"] != []:
        if "inc_for_stat_4" in form_button and form_button["inc_for_stat_4"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_4"]
            description = form_button["description_for_stat_4"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_4 = True
            add_stat_4 = Outcom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_4=status_4)
            add_data_stat_4 = Outcom_Data.objects.create(local_key=add_stat_4, who_update=who_create, date_update=add_stat_4.date_create)
            if "description_for_file_stat_4" in form_button and form_button["description_for_file_stat_4"] != []:
                if "files_for_stat_4" in form_file and form_file["files_for_stat_4"] != []:
                    local_key = add_data_stat_4
                    file = form_file["files_for_stat_4"]
                    description_file = form_button["description_for_file_stat_4"]
                    File_Outcom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finaciar', project_id)

    if "description_for_stat_5" in form_button and form_button["description_for_stat_5"] != []:
        if "inc_for_stat_5" in form_button and form_button["inc_for_stat_5"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_5"]
            description = form_button["description_for_stat_5"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_5 = True
            add_stat_5 = Outcom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_5=status_5)
            add_data_stat_5 = Outcom_Data.objects.create(local_key=add_stat_5, who_update=who_create, date_update=add_stat_5.date_create)
            if "description_for_file_stat_5" in form_button and form_button["description_for_file_stat_5"] != []:
                if "files_for_stat_5" in form_file and form_file["files_for_stat_5"] != []:
                    local_key = add_data_stat_5
                    file = form_file["files_for_stat_5"]
                    description_file = form_button["description_for_file_stat_5"]
                    File_Outcom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finaciar', project_id)

    if "description_for_stat_6" in form_button and form_button["description_for_stat_6"] != []:
        if "inc_for_stat_6" in form_button and form_button["inc_for_stat_6"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_6"]
            description = form_button["description_for_stat_6"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_6 = True
            add_stat_6 = Outcom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_6=status_6)
            add_data_stat_6 = Outcom_Data.objects.create(local_key=add_stat_6, who_update=who_create, date_update=add_stat_6.date_create)
            if "description_for_file_stat_6" in form_button and form_button["description_for_file_stat_6"] != []:
                if "files_for_stat_6" in form_file and form_file["files_for_stat_6"] != []:
                    local_key = add_data_stat_6
                    file = form_file["files_for_stat_6"]
                    description_file = form_button["description_for_file_stat_6"]
                    File_Outcom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finaciar', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        list_all_des = list()
        list_all_del = list()
        list_all_outcom = list()
        for elem in form_button:
            elem_str = str(elem)
            if elem_str != "csrfmiddlewaretoken":

                if "description_stat_1_" in elem_str:
                    recult_rep = elem_str.replace("description_stat_1_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_2" in elem_str:
                    recult_rep = elem_str.replace("description_stat_2_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_3" in elem_str:
                    recult_rep = elem_str.replace("description_stat_3_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_4" in elem_str:
                    recult_rep = elem_str.replace("description_stat_4_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_5" in elem_str:
                    recult_rep = elem_str.replace("description_stat_5_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_6" in elem_str:
                    recult_rep = elem_str.replace("description_stat_6_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "outcom_sim_stat_1_" in elem_str:
                    recult_rep = elem_str.replace("outcom_sim_stat_1_", "")
                    id = int(recult_rep)
                    list_outcom = list()
                    list_outcom.append(int(id))
                    list_outcom.append(float(form_button[elem]))
                    list_all_outcom.append(list_outcom)

                if "outcom_sim_stat_2_" in elem_str:
                    recult_rep = elem_str.replace("outcom_sim_stat_2_", "")
                    id = int(recult_rep)
                    list_outcom = list()
                    list_outcom.append(int(id))
                    list_outcom.append(float(form_button[elem]))
                    list_all_outcom.append(list_outcom)

                if "outcom_sim_stat_3_" in elem_str:
                    recult_rep = elem_str.replace("outcom_sim_stat_3_", "")
                    id = int(recult_rep)
                    list_outcom = list()
                    list_outcom.append(int(id))
                    list_outcom.append(float(form_button[elem]))
                    list_all_outcom.append(list_outcom)

                if "outcom_sim_stat_4_" in elem_str:
                    recult_rep = elem_str.replace("outcom_sim_stat_4_", "")
                    id = int(recult_rep)
                    list_outcom = list()
                    list_outcom.append(int(id))
                    list_outcom.append(float(form_button[elem]))
                    list_all_outcom.append(list_outcom)

                if "outcom_sim_stat_5_" in elem_str:
                    recult_rep = elem_str.replace("outcom_sim_stat_5_", "")
                    id = int(recult_rep)
                    list_outcom = list()
                    list_outcom.append(int(id))
                    list_outcom.append(float(form_button[elem]))
                    list_all_outcom.append(list_outcom)

                if "outcom_sim_stat_6_" in elem_str:
                    recult_rep = elem_str.replace("outcom_sim_stat_6_", "")
                    id = int(recult_rep)
                    list_outcom = list()
                    list_outcom.append(int(id))
                    list_outcom.append(float(form_button[elem]))
                    list_all_outcom.append(list_outcom)

                if "del_stat_1_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_2_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_3_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_4_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_5_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_6_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

        if list_all_outcom != []:
            for pre_result in list_all_outcom:
                id = pre_result[0]
                for_re = Outcom.objects.get(id=id)
                outcom = pre_result[1]
                if for_re.inc_project != outcom:
                    Outcom.objects.filter(id=id).update(inc_project=outcom)

        if list_all_des != []:
            for pre_result in list_all_des:
                id = pre_result[0]
                for_re = Outcom.objects.get(id=id)
                description = pre_result[1]
                if for_re.inc_project != description:
                    Outcom.objects.filter(id=id).update(description=description)

        if list_all_del != []:
            for pre_result in list_all_del:
                id = int(pre_result)
                File_Outcom_Data.objects.filter(local_key__local_key__id=id).delete()
                Outcom_Data.objects.filter(local_key__id=id).delete()
                Outcom.objects.filter(id=id).delete()

        return redirect('finaciar', project_id)

    return render(request, 'projects/finaciar.html', locals())


def finacial(request, project_id):
    session_key = request.session.session_key
    prime = Data_Prime_Project.objects.get(prime_project__id=project_id)

    # Data for incom - HTML (Begin)
    all_incom_in_prime_project_status_1 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_1=True)
    incom_summ_status_1 = 0
    list_for_incom_status_1 = list()
    for incom_simple in all_incom_in_prime_project_status_1:
        incom_summ_status_1 = incom_summ_status_1 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        all_files = File_Incom_Data.objects.filter(local_key__local_key__id=incom_simple.local_key.id, local_key__local_key__status_1=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_incom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=incom_simple.local_key.id, incom_sim=incom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_incom_status_1.append(dict_for_save)

    all_incom_in_prime_project_status_2 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_2=True)
    incom_summ_status_2 = 0
    list_for_incom_status_2 = list()
    for incom_simple in all_incom_in_prime_project_status_2:
        incom_summ_status_2 = incom_summ_status_2 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        all_files = File_Incom_Data.objects.filter(local_key__local_key__id=incom_simple.local_key.id, local_key__local_key__status_2=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_incom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=incom_simple.local_key.id, incom_sim=incom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_incom_status_2.append(dict_for_save)

    all_incom_in_prime_project_status_3 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_3=True)
    incom_summ_status_3 = 0
    list_for_incom_status_3 = list()
    for incom_simple in all_incom_in_prime_project_status_3:
        incom_summ_status_3 = incom_summ_status_3 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        all_files = File_Incom_Data.objects.filter(local_key__local_key__id=incom_simple.local_key.id, local_key__local_key__status_3=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_incom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=incom_simple.local_key.id, incom_sim=incom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_incom_status_3.append(dict_for_save)

    all_incom_in_prime_project_status_4 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_4=True)
    incom_summ_status_4 = 0
    list_for_incom_status_4 = list()
    for incom_simple in all_incom_in_prime_project_status_4:
        incom_summ_status_4 = incom_summ_status_4 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        all_files = File_Incom_Data.objects.filter(local_key__local_key__id=incom_simple.local_key.id, local_key__local_key__status_4=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_incom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=incom_simple.local_key.id, incom_sim=incom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_incom_status_4.append(dict_for_save)

    all_incom_in_prime_project_status_5 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_5=True)
    incom_summ_status_5 = 0
    list_for_incom_status_5 = list()
    for incom_simple in all_incom_in_prime_project_status_5:
        incom_summ_status_5 = incom_summ_status_5 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        all_files = File_Incom_Data.objects.filter(local_key__local_key__id=incom_simple.local_key.id, local_key__local_key__status_5=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_incom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=incom_simple.local_key.id, incom_sim=incom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_incom_status_5.append(dict_for_save)

    all_incom_in_prime_project_status_6 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_6=True)
    incom_summ_status_6 = 0
    list_for_incom_status_6 = list()
    for incom_simple in all_incom_in_prime_project_status_6:
        incom_summ_status_6 = incom_summ_status_6 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        all_files = File_Incom_Data.objects.filter(local_key__local_key__id=incom_simple.local_key.id, local_key__local_key__status_6=True)
        list_all_files = list()
        for all_file in all_files:
            id = all_file.id
            file = all_file.file
            name_file_re = str(file)
            name_file = name_file_re.replace("file_atach_project_incom/", "")
            description_file = all_file.description_file
            who_create = all_file.who_create
            date_create = all_file.date_create
            dict_for_save_file = dict(id=id, name_file_re=name_file_re, name_file=name_file, description_file=description_file, who_create=who_create,
                                      date_create=date_create)
            list_all_files.append(dict_for_save_file)
        dict_for_save = dict(id=incom_simple.local_key.id, incom_sim=incom_sim, description=description, who_create=who_create,
                             date_create=date_create, who_update=who_update, date_update=date_update, list_all_files=list_all_files)
        list_for_incom_status_6.append(dict_for_save)
    # Data for incom - HTML (End)

    # Data for price (no_in) - HTML (Begin)
    project_for_main = Prime_Project.objects.get(id=project_id)
    if project_for_main.status_1 == True:
        view_for = "1"
        sum_incom = incom_summ_status_1
        # sum_outcom = outcom_summ_status_1
    if project_for_main.status_2 == True:
        view_for = "2"
        sum_incom = incom_summ_status_1 + incom_summ_status_2
        # sum_outcom = outcom_summ_status_1 + outcom_summ_status_2
    if project_for_main.status_3 == True:
        view_for = "3"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3
        # sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3
    if project_for_main.status_4 == True:
        view_for = "4"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3 + incom_summ_status_4
        # sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4
    if project_for_main.status_5 == True:
        view_for = "5"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3 + incom_summ_status_4 + incom_summ_status_5
        # sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4 + outcom_summ_status_5
    if project_for_main.status_6 == True:
        view_for = "6"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3 + incom_summ_status_4 + incom_summ_status_5 + incom_summ_status_6
        # sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4 + outcom_summ_status_5 + outcom_summ_status_6
    # prib = sum_incom - sum_outcom
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_button = request.POST
    form_file = request.FILES

    print(request.POST)
    print(request.FILES)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if elem_str != "csrfmiddlewaretoken":
                if "del_file_for_stat_1_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_1_", "")
                    id = int(recult_rep)
                    File_Incom_Data.objects.filter(id=id).delete()
                    return redirect('finacial', project_id)

                if "del_file_for_stat_2_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_2_", "")
                    id = int(recult_rep)
                    File_Incom_Data.objects.filter(id=id).delete()
                    return redirect('finacial', project_id)

                if "del_file_for_stat_3_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_3_", "")
                    id = int(recult_rep)
                    File_Incom_Data.objects.filter(id=id).delete()
                    return redirect('finacial', project_id)

                if "del_file_for_stat_4_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_4_", "")
                    id = int(recult_rep)
                    File_Incom_Data.objects.filter(id=id).delete()
                    return redirect('finacial', project_id)

                if "del_file_for_stat_5_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_5_", "")
                    id = int(recult_rep)
                    File_Incom_Data.objects.filter(id=id).delete()
                    return redirect('finacial', project_id)

                if "del_file_for_stat_6_" in elem_str:
                    recult_rep = elem_str.replace("del_file_for_stat_6_", "")
                    id = int(recult_rep)
                    File_Incom_Data.objects.filter(id=id).delete()
                    return redirect('finacial', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_1_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_1_", "")
                id_reload_file_stat_1 = elem_str.replace("reload_description_for_file_stat_1_", "")
                if id_reload_file_stat_1 == id_in_file:
                    new_data_reload = File_Incom_Data.objects.get(id=id_reload_file_stat_1)
                    name_form_button = "reload_description_for_file_stat_1_" + str(id_reload_file_stat_1)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_1_" + str(id_reload_file_stat_1)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_1).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Incom_Data.objects.get(id=id_reload_file_stat_1)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_1).delete()
                        File_Incom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finacial', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_2_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_2_", "")
                id_reload_file_stat_2 = elem_str.replace("reload_description_for_file_stat_2_", "")
                if id_reload_file_stat_2 == id_in_file:
                    new_data_reload = File_Incom_Data.objects.get(id=id_reload_file_stat_2)
                    name_form_button = "reload_description_for_file_stat_2_" + str(id_reload_file_stat_2)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_2_" + str(id_reload_file_stat_2)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_2).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Incom_Data.objects.get(id=id_reload_file_stat_2)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_2).delete()
                        File_Incom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finacial', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_3_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_3_", "")
                id_reload_file_stat_3 = elem_str.replace("reload_description_for_file_stat_3_", "")
                if id_reload_file_stat_3 == id_in_file:
                    new_data_reload = File_Incom_Data.objects.get(id=id_reload_file_stat_3)
                    name_form_button = "reload_description_for_file_stat_3_" + str(id_reload_file_stat_3)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_3_" + str(id_reload_file_stat_3)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_3).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Incom_Data.objects.get(id=id_reload_file_stat_3)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_3).delete()
                        File_Incom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finacial', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_4_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_4_", "")
                id_reload_file_stat_4 = elem_str.replace("reload_description_for_file_stat_4_", "")
                if id_reload_file_stat_4 == id_in_file:
                    new_data_reload = File_Incom_Data.objects.get(id=id_reload_file_stat_4)
                    name_form_button = "reload_description_for_file_stat_4_" + str(id_reload_file_stat_4)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_4_" + str(id_reload_file_stat_4)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_4).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Incom_Data.objects.get(id=id_reload_file_stat_4)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_4).delete()
                        File_Incom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finacial', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_5_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_5_", "")
                id_reload_file_stat_5 = elem_str.replace("reload_description_for_file_stat_5_", "")
                if id_reload_file_stat_5 == id_in_file:
                    new_data_reload = File_Incom_Data.objects.get(id=id_reload_file_stat_5)
                    name_form_button = "reload_description_for_file_stat_5_" + str(id_reload_file_stat_5)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_5_" + str(id_reload_file_stat_5)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_5).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Incom_Data.objects.get(id=id_reload_file_stat_5)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_5).delete()
                        File_Incom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finacial', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        for elem in form_button:
            elem_str = str(elem)
            if "reload_description_for_file_stat_6_" in elem_str:
                for form_fil in form_file:
                    break
                if form_fil != []:
                    str_form_fil = str(form_fil)
                    id_in_file = str_form_fil.replace("reload_files_for_stat_6_", "")
                id_reload_file_stat_6 = elem_str.replace("reload_description_for_file_stat_6_", "")
                if id_reload_file_stat_6 == id_in_file:
                    new_data_reload = File_Incom_Data.objects.get(id=id_reload_file_stat_6)
                    name_form_button = "reload_description_for_file_stat_6_" + str(id_reload_file_stat_6)
                    new_des = form_button[name_form_button]
                    name_form_file = "reload_files_for_stat_6_" + str(id_reload_file_stat_6)
                    new_file = form_file[name_form_file]
                    if new_data_reload.description_file != new_des:
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_6).update(description_file=new_des)
                    if new_data_reload.file != new_file:
                        for_local_key = File_Incom_Data.objects.get(id=id_reload_file_stat_6)
                        local_key = for_local_key.local_key
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        File_Incom_Data.objects.filter(id=id_reload_file_stat_6).delete()
                        File_Incom_Data.objects.create(local_key=local_key, file=new_file, description_file=new_des, who_create=who_create)
                        return redirect('finacial', project_id)

    if "description_for_file_stat_1_add" in form_button and form_button["description_for_file_stat_1_add"] != []:
        for elem in form_file:
            if "files_for_stat_1_add_id_" in elem:
                id_incom_for_stat_1 = int(elem.replace("files_for_stat_1_add_id_", ""))
                incom_for_save_files = Incom_Data.objects.filter(local_key__id=id_incom_for_stat_1)
                for incom_for_save_file in incom_for_save_files:
                    break
                name = "files_for_stat_1_add_id_" + str(id_incom_for_stat_1)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_1_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Incom_Data.objects.create(local_key=incom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finacial', project_id)

    if "description_for_file_stat_2_add" in form_button and form_button["description_for_file_stat_2_add"] != []:
        for elem in form_file:
            if "files_for_stat_2_add_id_" in elem:
                id_incom_for_stat_2 = int(elem.replace("files_for_stat_2_add_id_", ""))
                incom_for_save_files = Incom_Data.objects.filter(local_key__id=id_incom_for_stat_2)
                for incom_for_save_file in incom_for_save_files:
                    break
                name = "files_for_stat_2_add_id_" + str(id_incom_for_stat_2)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_2_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Incom_Data.objects.create(local_key=incom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finacial', project_id)

    if "description_for_file_stat_3_add" in form_button and form_button["description_for_file_stat_3_add"] != []:
        for elem in form_file:
            if "files_for_stat_3_add_id_" in elem:
                id_incom_for_stat_3 = int(elem.replace("files_for_stat_3_add_id_", ""))
                incom_for_save_files = Incom_Data.objects.filter(local_key__id=id_incom_for_stat_3)
                for incom_for_save_file in incom_for_save_files:
                    break
                name = "files_for_stat_3_add_id_" + str(id_incom_for_stat_3)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_3_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Incom_Data.objects.create(local_key=incom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finacial', project_id)

    if "description_for_file_stat_4_add" in form_button and form_button["description_for_file_stat_4_add"] != []:
        for elem in form_file:
            if "files_for_stat_4_add_id_" in elem:
                id_incom_for_stat_4 = int(elem.replace("files_for_stat_4_add_id_", ""))
                incom_for_save_files = Incom_Data.objects.filter(local_key__id=id_incom_for_stat_4)
                for incom_for_save_file in incom_for_save_files:
                    break
                name = "files_for_stat_4_add_id_" + str(id_incom_for_stat_4)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_4_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Incom_Data.objects.create(local_key=incom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finacial', project_id)

    if "description_for_file_stat_5_add" in form_button and form_button["description_for_file_stat_5_add"] != []:
        for elem in form_file:
            if "files_for_stat_5_add_id_" in elem:
                id_incom_for_stat_5 = int(elem.replace("files_for_stat_5_add_id_", ""))
                incom_for_save_files = Incom_Data.objects.filter(local_key__id=id_incom_for_stat_5)
                for incom_for_save_file in incom_for_save_files:
                    break
                name = "files_for_stat_5_add_id_" + str(id_incom_for_stat_5)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_5_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Incom_Data.objects.create(local_key=incom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finacial', project_id)

    if "description_for_file_stat_6_add" in form_button and form_button["description_for_file_stat_6_add"] != []:
        for elem in form_file:
            if "files_for_stat_6_add_id_" in elem:
                id_incom_for_stat_6 = int(elem.replace("files_for_stat_6_add_id_", ""))
                incom_for_save_files = Incom_Data.objects.filter(local_key__id=id_incom_for_stat_6)
                for incom_for_save_file in incom_for_save_files:
                    break
                name = "files_for_stat_6_add_id_" + str(id_incom_for_stat_6)
                file = form_file[name]
                description_file = form_button["description_for_file_stat_6_add"]
                who_create = User_Login.objects.get(id=int(request.session['user_id']))
                File_Incom_Data.objects.create(local_key=incom_for_save_file, file=file, description_file=description_file,
                                               who_create=who_create)
        return redirect('finacial', project_id)

    if "description_for_stat_1" in form_button and form_button["description_for_stat_1"] != []:
        if "inc_for_stat_1" in form_button and form_button["inc_for_stat_1"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_1"]
            description = form_button["description_for_stat_1"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_1 = True
            add_stat_1 = Incom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_1=status_1)
            add_data_stat_1 = Incom_Data.objects.create(local_key=add_stat_1, who_update=who_create, date_update=add_stat_1.date_create)
            if "description_for_file_stat_1" in form_button  and form_button["description_for_file_stat_1"] != []:
                if "files_for_stat_1" in form_file and form_file["files_for_stat_1"] != []:
                    local_key = add_data_stat_1
                    file = form_file["files_for_stat_1"]
                    description_file = form_button["description_for_file_stat_1"]
                    File_Incom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finacial', project_id)

    if "description_for_stat_2" in form_button and form_button["description_for_stat_2"] != []:
        if "inc_for_stat_2" in form_button and form_button["inc_for_stat_2"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_2"]
            description = form_button["description_for_stat_2"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_2 = True
            add_stat_2 = Incom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_2=status_2)
            add_data_stat_2 = Incom_Data.objects.create(local_key=add_stat_2, who_update=who_create, date_update=add_stat_2.date_create)
            if "description_for_file_stat_2" in form_button  and form_button["description_for_file_stat_2"] != []:
                if "files_for_stat_2" in form_file and form_file["files_for_stat_2"] != []:
                    local_key = add_data_stat_2
                    file = form_file["files_for_stat_2"]
                    description_file = form_button["description_for_file_stat_2"]
                    File_Incom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finacial', project_id)

    if "description_for_stat_3" in form_button and form_button["description_for_stat_3"] != []:
        if "inc_for_stat_3" in form_button and form_button["inc_for_stat_3"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_3"]
            description = form_button["description_for_stat_3"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_3 = True
            add_stat_3 = Incom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_3=status_3)
            add_data_stat_3 = Incom_Data.objects.create(local_key=add_stat_3, who_update=who_create, date_update=add_stat_3.date_create)
            if "description_for_file_stat_3" in form_button  and form_button["description_for_file_stat_3"] != []:
                if "files_for_stat_3" in form_file and form_file["files_for_stat_3"] != []:
                    local_key = add_data_stat_3
                    file = form_file["files_for_stat_3"]
                    description_file = form_button["description_for_file_stat_3"]
                    File_Incom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finacial', project_id)

    if "description_for_stat_4" in form_button and form_button["description_for_stat_4"] != []:
        if "inc_for_stat_4" in form_button and form_button["inc_for_stat_4"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_4"]
            description = form_button["description_for_stat_4"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_4 = True
            add_stat_4 = Incom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_4=status_4)
            add_data_stat_4 = Incom_Data.objects.create(local_key=add_stat_4, who_update=who_create, date_update=add_stat_4.date_create)
            if "description_for_file_stat_4" in form_button  and form_button["description_for_file_stat_4"] != []:
                if "files_for_stat_4" in form_file and form_file["files_for_stat_4"] != []:
                    local_key = add_data_stat_4
                    file = form_file["files_for_stat_4"]
                    description_file = form_button["description_for_file_stat_4"]
                    File_Incom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finacial', project_id)

    if "description_for_stat_5" in form_button and form_button["description_for_stat_5"] != []:
        if "inc_for_stat_5" in form_button and form_button["inc_for_stat_5"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_5"]
            description = form_button["description_for_stat_5"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_5 = True
            add_stat_5 = Incom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_5=status_5)
            add_data_stat_5 = Incom_Data.objects.create(local_key=add_stat_5, who_update=who_create, date_update=add_stat_5.date_create)
            if "description_for_file_stat_5" in form_button  and form_button["description_for_file_stat_5"] != []:
                if "files_for_stat_5" in form_file and form_file["files_for_stat_5"] != []:
                    local_key = add_data_stat_5
                    file = form_file["files_for_stat_5"]
                    description_file = form_button["description_for_file_stat_5"]
                    File_Incom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finacial', project_id)

    if "description_for_stat_6" in form_button and form_button["description_for_stat_6"] != []:
        if "inc_for_stat_6" in form_button and form_button["inc_for_stat_6"] != []:
            project = Prime_Project.objects.get(id=int(project_id))
            inc_project = form_button["inc_for_stat_6"]
            description = form_button["description_for_stat_6"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            status_6 = True
            add_stat_6 = Incom.objects.create(project=project, inc_project=inc_project, description=description, who_create=who_create,
                                              status_6=status_6)
            add_data_stat_6 = Incom_Data.objects.create(local_key=add_stat_6, who_update=who_create, date_update=add_stat_6.date_create)
            if "description_for_file_stat_6" in form_button  and form_button["description_for_file_stat_6"] != []:
                if "files_for_stat_6" in form_file and form_file["files_for_stat_6"] != []:
                    local_key = add_data_stat_6
                    file = form_file["files_for_stat_6"]
                    description_file = form_button["description_for_file_stat_6"]
                    File_Incom_Data.objects.create(local_key=local_key, file=file, description_file=description_file, who_create=who_create)
            return redirect('finacial', project_id)

    if "csrfmiddlewaretoken" in form_button and form_button["csrfmiddlewaretoken"] != []:
        list_all_des = list()
        list_all_del = list()
        list_all_incom = list()
        for elem in form_button:
            elem_str = str(elem)
            if elem_str != "csrfmiddlewaretoken":

                if "description_stat_1_" in elem_str:
                    recult_rep = elem_str.replace("description_stat_1_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_2" in elem_str:
                    recult_rep = elem_str.replace("description_stat_2_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_3" in elem_str:
                    recult_rep = elem_str.replace("description_stat_3_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_4" in elem_str:
                    recult_rep = elem_str.replace("description_stat_4_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_5" in elem_str:
                    recult_rep = elem_str.replace("description_stat_5_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "description_stat_6" in elem_str:
                    recult_rep = elem_str.replace("description_stat_6_", "")
                    id = int(recult_rep)
                    list_des = list()
                    list_des.append(int(id))
                    list_des.append(str(form_button[elem]))
                    list_all_des.append(list_des)

                if "incom_sim_stat_1_" in elem_str:
                    recult_rep = elem_str.replace("incom_sim_stat_1_", "")
                    id = int(recult_rep)
                    list_incom = list()
                    list_incom.append(int(id))
                    list_incom.append(float(form_button[elem]))
                    list_all_incom.append(list_incom)

                if "incom_sim_stat_2_" in elem_str:
                    recult_rep = elem_str.replace("incom_sim_stat_2_", "")
                    id = int(recult_rep)
                    list_incom = list()
                    list_incom.append(int(id))
                    list_incom.append(float(form_button[elem]))
                    list_all_incom.append(list_incom)

                if "incom_sim_stat_3_" in elem_str:
                    recult_rep = elem_str.replace("incom_sim_stat_3_", "")
                    id = int(recult_rep)
                    list_incom = list()
                    list_incom.append(int(id))
                    list_incom.append(float(form_button[elem]))
                    list_all_incom.append(list_incom)

                if "incom_sim_stat_4_" in elem_str:
                    recult_rep = elem_str.replace("incom_sim_stat_4_", "")
                    id = int(recult_rep)
                    list_incom = list()
                    list_incom.append(int(id))
                    list_incom.append(float(form_button[elem]))
                    list_all_incom.append(list_incom)

                if "incom_sim_stat_5_" in elem_str:
                    recult_rep = elem_str.replace("incom_sim_stat_5_", "")
                    id = int(recult_rep)
                    list_incom = list()
                    list_incom.append(int(id))
                    list_incom.append(float(form_button[elem]))
                    list_all_incom.append(list_incom)

                if "incom_sim_stat_6_" in elem_str:
                    recult_rep = elem_str.replace("incom_sim_stat_6_", "")
                    id = int(recult_rep)
                    list_incom = list()
                    list_incom.append(int(id))
                    list_incom.append(float(form_button[elem]))
                    list_all_incom.append(list_incom)

                if "del_stat_1_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_2_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_3_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_4_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_5_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

                if "del_stat_6_" in elem_str:
                    list_all_del.append(int(form_button[elem]))

        if list_all_incom != []:
            for pre_result in list_all_incom:
                id = pre_result[0]
                for_re = Incom.objects.get(id=id)
                incom = pre_result[1]
                if for_re.inc_project != incom:
                    Incom.objects.filter(id=id).update(inc_project=incom)

        if list_all_des != []:
            for pre_result in list_all_des:
                id = pre_result[0]
                for_re = Incom.objects.get(id=id)
                description = pre_result[1]
                if for_re.inc_project != description:
                    Incom.objects.filter(id=id).update(description=description)

        if list_all_del != []:
            for pre_result in list_all_del:
                id = int(pre_result)
                File_Incom_Data.objects.filter(local_key__local_key__id=id).delete()
                Incom_Data.objects.filter(local_key__id=id).delete()
                Incom.objects.filter(id=id).delete()

        return redirect('finacial', project_id)

    return render(request, 'projects/finacial.html', locals())


def project(request, project_id):
    session_key = request.session.session_key
    request.session['upd_sub_project_sub_main'] = False
    request.session['upd_sub_project_main_sub'] = False

    users_for_mod_create = User_Login.objects.filter()

    prime = Data_Prime_Project.objects.get(prime_project__id=project_id)
    request.session['project_id'] = prime.prime_project.id

    date = prime.date_create_project
    date_strt = prime.date_start_project
    date_dld = prime.date_deadline_project

    strt_prj = datetime.toordinal(date_strt)
    dld_prj = datetime.toordinal(date_dld)
    now_prg = datetime.toordinal(datetime.now())
    days_proj = dld_prj - strt_prj
    days_now = now_prg - strt_prj
    proc_ras = round((days_now * 100) / days_proj)

    file_for_project_main = File_For_Project.objects.filter(boss_project__id=project_id)

    all_company_partners = Contacts.objects.filter(prime_project__id=project_id)
    list_contacts = list()
    for company_partner in all_company_partners:
        data_contacts = Data_Contacts.objects.filter(local_key=company_partner)
        result_find_contacts = dict(contact=company_partner, data_contacts=data_contacts)
        list_contacts.append(result_find_contacts)


    list_for_file_project = list()
    for file_for in file_for_project_main:
        id = file_for.id
        search_name_file = str(file_for.file)
        name = search_name_file.replace("file_atach_project/", "")
        description_file = file_for.description_file
        who_create = file_for.who_create
        date_create = file_for.date_create
        for_way = file_for.file

        dict_for_file_project = dict(name=name, description_file=description_file, who_create=who_create, date_create=date_create,
                                     for_way=for_way, id=id)
        list_for_file_project.append(dict_for_file_project)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# Data for incom - HTML (Begin)
    all_incom_in_prime_project_status_1 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_1=True)
    incom_summ_status_1 = 0
    list_for_incom_status_1 = list()
    for incom_simple in all_incom_in_prime_project_status_1:
        incom_summ_status_1 = incom_summ_status_1 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        dict_for_save = dict(incom_sim=incom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_incom_status_1.append(dict_for_save)

    all_incom_in_prime_project_status_2 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_2=True)
    incom_summ_status_2 = 0
    list_for_incom_status_2 = list()
    for incom_simple in all_incom_in_prime_project_status_2:
        incom_summ_status_2 = incom_summ_status_2 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        dict_for_save = dict(incom_sim=incom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_incom_status_2.append(dict_for_save)

    all_incom_in_prime_project_status_3 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_3=True)
    incom_summ_status_3 = 0
    list_for_incom_status_3 = list()
    for incom_simple in all_incom_in_prime_project_status_3:
        incom_summ_status_3 = incom_summ_status_3 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        dict_for_save = dict(incom_sim=incom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_incom_status_3.append(dict_for_save)

    all_incom_in_prime_project_status_4 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_4=True)
    incom_summ_status_4 = 0
    list_for_incom_status_4 = list()
    for incom_simple in all_incom_in_prime_project_status_4:
        incom_summ_status_4 = incom_summ_status_4 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        dict_for_save = dict(incom_sim=incom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_incom_status_4.append(dict_for_save)

    all_incom_in_prime_project_status_5 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_5=True)
    incom_summ_status_5 = 0
    list_for_incom_status_5 = list()
    for incom_simple in all_incom_in_prime_project_status_5:
        incom_summ_status_5 = incom_summ_status_5 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        dict_for_save = dict(incom_sim=incom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_incom_status_5.append(dict_for_save)

    all_incom_in_prime_project_status_6 = Incom_Data.objects.filter(local_key__project__id=project_id, local_key__status_6=True)
    incom_summ_status_6 = 0
    list_for_incom_status_6 = list()
    for incom_simple in all_incom_in_prime_project_status_6:
        incom_summ_status_6 = incom_summ_status_6 + int(incom_simple.local_key.inc_project)
        incom_sim = incom_simple.local_key.inc_project
        description = incom_simple.local_key.description
        who_create = incom_simple.local_key.who_create
        date_create = incom_simple.local_key.date_create
        who_update = incom_simple.who_update
        date_update = incom_simple.date_update
        dict_for_save = dict(incom_sim=incom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_incom_status_6.append(dict_for_save)
# Data for incom - HTML (End)

# Data for outcom - HTML (Begin)
    all_outcom_in_prime_project_status_1 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_1=True)
    outcom_summ_status_1 = 0
    list_for_outcom_status_1 = list()
    for outcom_simple in all_outcom_in_prime_project_status_1:
        outcom_summ_status_1 = outcom_summ_status_1 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        dict_for_save = dict(outcom_sim=outcom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_outcom_status_1.append(dict_for_save)

    all_outcom_in_prime_project_status_2 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_2=True)
    outcom_summ_status_2 = 0
    list_for_outcom_status_2 = list()
    for outcom_simple in all_outcom_in_prime_project_status_2:
        outcom_summ_status_2 = outcom_summ_status_2 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        dict_for_save = dict(outcom_sim=outcom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_outcom_status_2.append(dict_for_save)

    all_outcom_in_prime_project_status_3 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_3=True)
    outcom_summ_status_3 = 0
    list_for_outcom_status_3 = list()
    for outcom_simple in all_outcom_in_prime_project_status_3:
        outcom_summ_status_3 = outcom_summ_status_3 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        dict_for_save = dict(outcom_sim=outcom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_outcom_status_3.append(dict_for_save)

    all_outcom_in_prime_project_status_4 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_4=True)
    outcom_summ_status_4 = 0
    list_for_outcom_status_4 = list()
    for outcom_simple in all_outcom_in_prime_project_status_4:
        outcom_summ_status_4 = outcom_summ_status_4 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        dict_for_save = dict(outcom_sim=outcom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_outcom_status_4.append(dict_for_save)

    all_outcom_in_prime_project_status_5 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_5=True)
    outcom_summ_status_5 = 0
    list_for_outcom_status_5 = list()
    for outcom_simple in all_outcom_in_prime_project_status_5:
        outcom_summ_status_5 = outcom_summ_status_5 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        dict_for_save = dict(outcom_sim=outcom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_outcom_status_5.append(dict_for_save)

    all_outcom_in_prime_project_status_6 = Outcom_Data.objects.filter(local_key__project__id=project_id, local_key__status_6=True)
    outcom_summ_status_6 = 0
    list_for_outcom_status_6 = list()
    for outcom_simple in all_outcom_in_prime_project_status_6:
        outcom_summ_status_6 = outcom_summ_status_6 + int(outcom_simple.local_key.inc_project)
        outcom_sim = outcom_simple.local_key.inc_project
        description = outcom_simple.local_key.description
        who_create = outcom_simple.local_key.who_create
        date_create = outcom_simple.local_key.date_create
        who_update = outcom_simple.who_update
        date_update = outcom_simple.date_update
        dict_for_save = dict(outcom_sim=outcom_sim, description=description, who_create=who_create, date_create=date_create, who_update=who_update, date_update=date_update)
        list_for_outcom_status_6.append(dict_for_save)
# Data for outcom - HTML (End)

# Data for price (no_in) - HTML (Begin)
    project_for_main = Prime_Project.objects.get(id=project_id)
    if project_for_main.status_1 == True:
        view_for = "1"
        sum_incom = incom_summ_status_1
        sum_outcom = outcom_summ_status_1
    if project_for_main.status_2 == True:
        view_for = "2"
        sum_incom = incom_summ_status_1 + incom_summ_status_2
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2
    if project_for_main.status_3 == True:
        view_for = "3"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3
    if project_for_main.status_4 == True:
        view_for = "4"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3 + incom_summ_status_4
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4
    if project_for_main.status_5 == True:
        view_for = "5"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3 + incom_summ_status_4 + incom_summ_status_5
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4 + outcom_summ_status_5
    if project_for_main.status_6 == True:
        view_for = "6"
        sum_incom = incom_summ_status_1 + incom_summ_status_2 + incom_summ_status_3 + incom_summ_status_4 + incom_summ_status_5 + incom_summ_status_6
        sum_outcom = outcom_summ_status_1 + outcom_summ_status_2 + outcom_summ_status_3 + outcom_summ_status_4 + outcom_summ_status_5 + outcom_summ_status_6
    prib = sum_incom - sum_outcom
# Data for price (no_in) - HTML (End)

# Data for price - HTML (Begin)
    all_incom_status_1 = Incom_Data.objects.filter(local_key__status_1=True)
    all_outcom_status_1 = Outcom_Data.objects.filter(local_key__status_1=True)
    all_price_nofillter_status_1 = list()
    time_list_status_1 = list()
    for elem in all_incom_status_1:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='incom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_1.append(dict_nofiltr)
        time_list_status_1.append(time)
    for elem in all_outcom_status_1:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='outcom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_1.append(dict_nofiltr)
        time_list_status_1.append(time)
    time_list_status_1.sort()
    result_status_pre_ststus_1 = list()
    for elem in time_list_status_1:
        for elem_2 in all_price_nofillter_status_1:
            if elem_2["date_create"] == elem and elem_2 not in result_status_pre_ststus_1:
                result_status_pre_ststus_1.append(elem_2)
    summ_incom_res_stat_1 = 0
    summ_outcom_res_stat_1 = 0
    list_for_bill_status_1 = list()
    for elem in result_status_pre_ststus_1:
        if elem["type"] == "incom":
            id_find = elem["id"]
            inss = Incom_Data.objects.filter(local_key__status_1=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "доход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_incom_res_stat_1 = summ_incom_res_stat_1 + int(incom_sim)
            all_files = File_Incom_Data.objects.filter(local_key__local_key__status_1=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_incom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        if elem["type"] == "outcom":
            id_find = elem["id"]
            inss = Outcom_Data.objects.filter(local_key__status_1=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "расход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_outcom_res_stat_1 = summ_outcom_res_stat_1 + int(incom_sim)
            all_files = File_Outcom_Data.objects.filter(local_key__local_key__status_1=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_outcom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        dict_for_save = dict(date_create=date_create, who_create=who_create, type=type_el, description=description, incom_sim=incom_sim,
                             list_all_files=list_all_files, date_update=date_update, who_update=who_update)
        list_for_bill_status_1.append(dict_for_save)
        prib_stat_1 = summ_incom_res_stat_1 - summ_outcom_res_stat_1

    all_incom_status_2 = Incom_Data.objects.filter(local_key__status_2=True)
    all_outcom_status_2 = Outcom_Data.objects.filter(local_key__status_2=True)
    all_price_nofillter_status_2 = list()
    time_list_status_2 = list()
    for elem in all_incom_status_2:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='incom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_2.append(dict_nofiltr)
        time_list_status_2.append(time)
    for elem in all_outcom_status_2:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='outcom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_2.append(dict_nofiltr)
        time_list_status_2.append(time)
    time_list_status_2.sort()
    result_status_pre_ststus_2 = list()
    for elem in time_list_status_2:
        for elem_2 in all_price_nofillter_status_2:
            if elem_2["date_create"] == elem and elem_2 not in result_status_pre_ststus_2:
                result_status_pre_ststus_2.append(elem_2)
    summ_incom_res_stat_2 = 0
    summ_outcom_res_stat_2 = 0
    list_for_bill_status_2 = list()
    for elem in result_status_pre_ststus_2:
        if elem["type"] == "incom":
            id_find = elem["id"]
            inss = Incom_Data.objects.filter(local_key__status_2=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "доход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_incom_res_stat_2 = summ_incom_res_stat_2 + int(incom_sim)
            all_files = File_Incom_Data.objects.filter(local_key__local_key__status_2=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_incom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        if elem["type"] == "outcom":
            id_find = elem["id"]
            inss = Outcom_Data.objects.filter(local_key__status_2=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "расход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_outcom_res_stat_2 = summ_outcom_res_stat_2 + int(incom_sim)
            all_files = File_Outcom_Data.objects.filter(local_key__local_key__status_2=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_outcom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        dict_for_save = dict(date_create=date_create, who_create=who_create, type=type_el, description=description, incom_sim=incom_sim,
                             list_all_files=list_all_files, date_update=date_update, who_update=who_update)
        list_for_bill_status_2.append(dict_for_save)
        prib_stat_2 = summ_incom_res_stat_2 - summ_outcom_res_stat_2

    all_incom_status_3 = Incom_Data.objects.filter(local_key__status_3=True)
    all_outcom_status_3 = Outcom_Data.objects.filter(local_key__status_3=True)
    all_price_nofillter_status_3 = list()
    time_list_status_3 = list()
    for elem in all_incom_status_3:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='incom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_3.append(dict_nofiltr)
        time_list_status_3.append(time)
    for elem in all_outcom_status_3:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='outcom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_3.append(dict_nofiltr)
        time_list_status_3.append(time)
    time_list_status_3.sort()
    result_status_pre_ststus_3 = list()
    for elem in time_list_status_3:
        for elem_2 in all_price_nofillter_status_3:
            if elem_2["date_create"] == elem and elem_2 not in result_status_pre_ststus_3:
                result_status_pre_ststus_3.append(elem_2)
    summ_incom_res_stat_3 = 0
    summ_outcom_res_stat_3 = 0
    list_for_bill_status_3 = list()
    for elem in result_status_pre_ststus_3:
        if elem["type"] == "incom":
            id_find = elem["id"]
            inss = Incom_Data.objects.filter(local_key__status_3=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "доход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_incom_res_stat_3 = summ_incom_res_stat_3 + int(incom_sim)
            all_files = File_Incom_Data.objects.filter(local_key__local_key__status_3=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_incom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        if elem["type"] == "outcom":
            id_find = elem["id"]
            inss = Outcom_Data.objects.filter(local_key__status_3=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "расход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_outcom_res_stat_3 = summ_outcom_res_stat_3 + int(incom_sim)
            all_files = File_Outcom_Data.objects.filter(local_key__local_key__status_3=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_outcom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        dict_for_save = dict(date_create=date_create, who_create=who_create, type=type_el, description=description, incom_sim=incom_sim,
                             list_all_files=list_all_files, date_update=date_update, who_update=who_update)
        list_for_bill_status_3.append(dict_for_save)
        prib_stat_3 = summ_incom_res_stat_3 - summ_outcom_res_stat_3

    all_incom_status_4 = Incom_Data.objects.filter(local_key__status_4=True)
    all_outcom_status_4 = Outcom_Data.objects.filter(local_key__status_4=True)
    all_price_nofillter_status_4 = list()
    time_list_status_4 = list()
    for elem in all_incom_status_4:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='incom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_4.append(dict_nofiltr)
        time_list_status_4.append(time)
    for elem in all_outcom_status_4:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='outcom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_4.append(dict_nofiltr)
        time_list_status_4.append(time)
    time_list_status_4.sort()
    result_status_pre_ststus_4 = list()
    for elem in time_list_status_4:
        for elem_2 in all_price_nofillter_status_4:
            if elem_2["date_create"] == elem and elem_2 not in result_status_pre_ststus_4:
                result_status_pre_ststus_4.append(elem_2)
    summ_incom_res_stat_4 = 0
    summ_outcom_res_stat_4 = 0
    list_for_bill_status_4 = list()
    for elem in result_status_pre_ststus_4:
        if elem["type"] == "incom":
            id_find = elem["id"]
            inss = Incom_Data.objects.filter(local_key__status_4=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "доход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_incom_res_stat_4 = summ_incom_res_stat_4 + int(incom_sim)
            all_files = File_Incom_Data.objects.filter(local_key__local_key__status_4=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_incom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        if elem["type"] == "outcom":
            id_find = elem["id"]
            inss = Outcom_Data.objects.filter(local_key__status_4=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "расход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_outcom_res_stat_4 = summ_outcom_res_stat_4 + int(incom_sim)
            all_files = File_Outcom_Data.objects.filter(local_key__local_key__status_4=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_outcom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        dict_for_save = dict(date_create=date_create, who_create=who_create, type=type_el, description=description, incom_sim=incom_sim,
                             list_all_files=list_all_files, date_update=date_update, who_update=who_update)
        list_for_bill_status_4.append(dict_for_save)
        prib_stat_4 = summ_incom_res_stat_4 - summ_outcom_res_stat_4

    all_incom_status_5 = Incom_Data.objects.filter(local_key__status_5=True)
    all_outcom_status_5 = Outcom_Data.objects.filter(local_key__status_5=True)
    all_price_nofillter_status_5 = list()
    time_list_status_5 = list()
    for elem in all_incom_status_5:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='incom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_5.append(dict_nofiltr)
        time_list_status_5.append(time)
    for elem in all_outcom_status_5:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='outcom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_5.append(dict_nofiltr)
        time_list_status_5.append(time)
    time_list_status_5.sort()
    result_status_pre_ststus_5 = list()
    for elem in time_list_status_5:
        for elem_2 in all_price_nofillter_status_5:
            if elem_2["date_create"] == elem and elem_2 not in result_status_pre_ststus_5:
                result_status_pre_ststus_5.append(elem_2)
    summ_incom_res_stat_5 = 0
    summ_outcom_res_stat_5 = 0
    list_for_bill_status_5 = list()
    for elem in result_status_pre_ststus_5:
        if elem["type"] == "incom":
            id_find = elem["id"]
            inss = Incom_Data.objects.filter(local_key__status_5=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "доход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_incom_res_stat_5 = summ_incom_res_stat_5 + int(incom_sim)
            all_files = File_Incom_Data.objects.filter(local_key__local_key__status_5=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_incom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        if elem["type"] == "outcom":
            id_find = elem["id"]
            inss = Outcom_Data.objects.filter(local_key__status_5=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "расход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_outcom_res_stat_5 = summ_outcom_res_stat_5 + int(incom_sim)
            all_files = File_Outcom_Data.objects.filter(local_key__local_key__status_5=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_outcom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        dict_for_save = dict(date_create=date_create, who_create=who_create, type=type_el, description=description, incom_sim=incom_sim,
                             list_all_files=list_all_files, date_update=date_update, who_update=who_update)
        list_for_bill_status_5.append(dict_for_save)
        prib_stat_5 = summ_incom_res_stat_5 - summ_outcom_res_stat_5

    all_incom_status_6 = Incom_Data.objects.filter(local_key__status_6=True)
    all_outcom_status_6 = Outcom_Data.objects.filter(local_key__status_6=True)
    all_price_nofillter_status_6 = list()
    time_list_status_6 = list()
    for elem in all_incom_status_6:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='incom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_6.append(dict_nofiltr)
        time_list_status_6.append(time)
    for elem in all_outcom_status_6:
        time = datetime.toordinal(elem.local_key.date_create)
        dict_nofiltr = dict(type='outcom', id=elem.local_key.id, date_create=time)
        all_price_nofillter_status_6.append(dict_nofiltr)
        time_list_status_6.append(time)
    time_list_status_6.sort()
    result_status_pre_ststus_6 = list()
    for elem in time_list_status_6:
        for elem_2 in all_price_nofillter_status_6:
            if elem_2["date_create"] == elem and elem_2 not in result_status_pre_ststus_6:
                result_status_pre_ststus_6.append(elem_2)
    summ_incom_res_stat_6 = 0
    summ_outcom_res_stat_6 = 0
    list_for_bill_status_6 = list()
    for elem in result_status_pre_ststus_6:
        if elem["type"] == "incom":
            id_find = elem["id"]
            inss = Incom_Data.objects.filter(local_key__status_6=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "доход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_incom_res_stat_6 = summ_incom_res_stat_6 + int(incom_sim)
            all_files = File_Incom_Data.objects.filter(local_key__local_key__status_6=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_incom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        if elem["type"] == "outcom":
            id_find = elem["id"]
            inss = Outcom_Data.objects.filter(local_key__status_6=True, local_key__id=id_find)
            for ins in inss:
                break
            date_create = ins.local_key.date_create
            who_create = ins.local_key.who_create
            type_el = "расход"
            description = ins.local_key.description
            incom_sim = ins.local_key.inc_project
            date_update = ins.date_update
            who_update = ins.who_update
            summ_outcom_res_stat_6 = summ_outcom_res_stat_6 + int(incom_sim)
            all_files = File_Outcom_Data.objects.filter(local_key__local_key__status_6=True, local_key=ins)
            list_all_files = list()
            for all_file in all_files:
                id_f = all_file.id
                file = all_file.file
                name_file_re = str(file)
                name_file = name_file_re.replace("file_atach_project_outcom/", "")
                description_file = all_file.description_file
                who_create = all_file.who_create
                date_create = all_file.date_create
                dict_for_save_file = dict(id=id_f, name_file_re=name_file_re, name_file=name_file, description_file=description_file,
                                          who_create=who_create, date_create=date_create)
                list_all_files.append(dict_for_save_file)
        dict_for_save = dict(date_create=date_create, who_create=who_create, type=type_el, description=description, incom_sim=incom_sim,
                             list_all_files=list_all_files, date_update=date_update, who_update=who_update)
        list_for_bill_status_6.append(dict_for_save)
        prib_stat_6 = summ_incom_res_stat_6 - summ_outcom_res_stat_6

    prib_prom_stat_1 = prib_stat_1
    prib_prom_stat_2 = prib_stat_1 + prib_stat_2
    prib_prom_stat_3 = prib_stat_1 + prib_stat_2 + prib_stat_3
    prib_prom_stat_4 = prib_stat_1 + prib_stat_2 + prib_stat_3 + prib_stat_4
    prib_prom_stat_5 = prib_stat_1 + prib_stat_2 + prib_stat_3 + prib_stat_4 + prib_stat_5
    prib_prom_stat_6 = prib_stat_1 + prib_stat_2 + prib_stat_3 + prib_stat_4 + prib_stat_5 + prib_stat_6


# Transform id numbers in list (Begin)
    prime_project_main = Prime_Project.objects.get(id=project_id)

    if prime_project_main.status_1 == True:
        list_all_active_subproject = Sub_Project.objects.filter(prime_project=prime_project_main, status_1=True)
    if prime_project_main.status_2 == True:
        list_all_active_subproject = Sub_Project.objects.filter(prime_project=prime_project_main, status_2=True)
    if prime_project_main.status_3 == True:
        list_all_active_subproject = Sub_Project.objects.filter(prime_project=prime_project_main, status_3=True)
    if prime_project_main.status_4 == True:
        list_all_active_subproject = Sub_Project.objects.filter(prime_project=prime_project_main, status_4=True)
    if prime_project_main.status_5 == True:
        list_all_active_subproject = Sub_Project.objects.filter(prime_project=prime_project_main, status_5=True)
    if prime_project_main.status_6 == True:
        list_all_active_subproject = Sub_Project.objects.filter(prime_project=prime_project_main, status_6=True)

    list_id = list()
    for subproject in list_all_active_subproject:
        id = subproject.id
        list_id.append(id)
    list_id = sorted(list_id)
    pair = list()
    result_out_par = list()
    for subproject in list_all_active_subproject:
        map_for_s = subproject.pair
        map_for_s_2 = map_for_s.replace(",", "")
        cort_for_p = map_for_s_2.split(" ")
        if len(cort_for_p) == 2:
            id_main = cort_for_p[0]
            id_go = cort_for_p[1]
            index_position_main = list_id.index(int(id_main))
            index_for_go = index_position_main + 1
            list_id.remove(int(id_go))
            list_id.insert(index_for_go, int(id_go))
    list_all_active_subproject_true = list()
    for id in list_id:
        list_all_active_subproject_true.append(Sub_Project.objects.get(id=int(id)))
# Transform id numbers in list (End)
    result_summ_sub = list()
    for prom in list_all_active_subproject_true:
        id_project_prom = prom.id
        for_list_sub_name_project = prom.name_project
        for_list_sub_description_project = prom.description_project
        for_list_sub_do_it = prom.do_it

        # for_list_sub_create_name = prom.who_create_project.name
        # for_list_sub_create_last_name = prom.who_create_project.last_name
        # for_list_sub_create_surname = prom.who_create_project.surname

        result_create = prom.who_create_project
        # result_create = for_list_sub_create_name + ' ' + for_list_sub_create_last_name + ' ' + for_list_sub_create_surname

        proms = Sub_Project_Prime_Data.objects.filter(local_key_id=id_project_prom)
        for promn in proms:
            break

        # for_list_sub_boss_name = promn.who_boss_project.name
        # for_list_sub_boss_last_name = promn.who_boss_project.last_name
        # for_list_sub_boss_surname = promn.who_boss_project.surname

        result_boss = promn.who_boss_project
        # result_boss = for_list_sub_boss_name + ' ' + for_list_sub_boss_last_name + ' ' + for_list_sub_boss_surname

        for_list_sub_rss = promn.level_project * 50

        for_list_sub_level = promn.level_project

        date_create_project = promn.date_create_project
        date_start_project = promn.date_start_project
        date_deadline_project = promn.date_deadline_project
        date_end_project = promn.date_fact_end

        start_prj = datetime.toordinal(date_start_project)
        dedlayn_prj = datetime.toordinal(date_deadline_project)
        now_day = datetime.toordinal(datetime.now())
        for_days_proj = dedlayn_prj - start_prj
        for_days_now = now_day - start_prj

        for_list_sub_proc_ras = round((for_days_now * 100) / for_days_proj)

        if date_end_project != None:
            for_list_date_end = date_end_project.strftime("%d-%m-%Y")
        else:
            for_list_date_end = []

        for_list_date_create = date_create_project.strftime("%d-%m-%Y")

        for_list_date_start = date_start_project.strftime("%d-%m-%Y")
        for_list_date_start_day = str(date_start_project.strftime("%d"))
        for_list_date_start_month = str(date_start_project.strftime("%m"))
        for_list_date_start_year = str(date_start_project.strftime("%Y"))

        for_list_date_dedline = date_deadline_project.strftime("%d-%m-%Y")
        for_list_date_dedline_day = str(date_deadline_project.strftime("%d"))
        for_list_date_dedline_month = str(date_deadline_project.strftime("%m"))
        for_list_date_dedline_year = str(date_deadline_project.strftime("%Y"))

        map_for_search = prom.map
        status_1 = prom.status_1
        status_2 = prom.status_2
        status_3 = prom.status_3
        status_4 = prom.status_4
        status_5 = prom.status_5
        status_6 = prom.status_6

        all_sub_p = Sub_Project.objects.filter(status_1=status_1, status_2=status_2, status_3=status_3, status_4=status_4,
                                               status_5=status_5, status_6=status_6)
        list_for_del_low = list()
        list_for_del_him = list()
        for sub_p in all_sub_p:
            str_map_for_search = str(map_for_search)
            str_sub_p_map = str(sub_p.map)
            len_map_for_search = len(str_map_for_search)
            srez = str_sub_p_map[0:len_map_for_search]
            if srez == str_map_for_search and sub_p.id != prom.id:
                results = Sub_Project_Prime_Data.objects.filter(local_key__id=sub_p.id)
                for result in results:
                    break
                list_for_del_low.append(result.local_key.id)
                list_for_del_him.append(result.local_key)

        list_for_del_low.append(prom.id)
        list_id_new = sorted(list_for_del_low)
        pair = list()
        result_out_par = list()
        for elem in list_for_del_him:
            map_for_s = elem.pair
            map_for_s_2 = map_for_s.replace(",", "")
            cort_for_p = map_for_s_2.split(" ")
            if len(cort_for_p) == 2:
                id_main = cort_for_p[0]
                id_go = cort_for_p[1]
                index_position_main = list_id_new.index(int(id_main))
                index_for_go = index_position_main + 1
                list_id_new.remove(int(id_go))
                list_id_new.insert(index_for_go, int(id_go))

        list_id_new.remove(prom.id)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        list_all_f_d_s = list()
        for elem in list_id_new:
            elem_ress = Sub_Project_Prime_Data.objects.filter(local_key__id=elem)
            for elem_res in elem_ress:
                break
            id_p = elem_res.local_key.id
            n_p = elem_res.local_key.name_project
            d_p = elem_res.local_key.description_project
            w_c_p = elem_res.local_key.who_create_project
            w_b_p = elem_res.who_boss_project
            d_c_p = elem_res.date_create_project
            d_s_p = elem_res.date_start_project
            d_e_p = elem_res.date_deadline_project
            lev_p = elem_res.level_project
            r_l_p = lev_p * 25

            start_sproj = datetime.toordinal(d_s_p)
            dealine_sproj = datetime.toordinal(d_e_p)
            now_date_real = datetime.toordinal(datetime.now())
            f_d_p = dealine_sproj - start_sproj

            f_d_n = now_date_real - start_sproj
            for_l_s_p_r = round((f_d_n * 100) / f_d_p)
            dict_for_dict_sub_del = dict(id_sub_project=id_p, name_project=n_p, description_project=d_p, who_create_project=w_c_p,
                                         who_boss_project=w_b_p, rass=r_l_p, level_project=lev_p, date_create_project=d_c_p,
                                         date_start_project=d_s_p, date_deadline_project=d_e_p, sub_proc_ras=for_l_s_p_r)
            list_all_f_d_s.append(dict_for_dict_sub_del)

        dict_for_viev = dict(id_subproject=id_project_prom, name_project=for_list_sub_name_project, description_project=for_list_sub_description_project, do_it=for_list_sub_do_it,
                             who_create_project=result_create, who_boss_project=result_boss, rass=for_list_sub_rss, level_project=for_list_sub_level,
                             date_end_project=for_list_date_end, date_create_project=for_list_date_create,
                             date_start_project=for_list_date_start, date_start_day=for_list_date_start_day, date_start_month=for_list_date_start_month, date_start_year=for_list_date_start_year,
                             date_deadline_project=for_list_date_dedline, date_dedline_day=for_list_date_dedline_day, date_dedline_month=for_list_date_dedline_month, date_dedline_year=for_list_date_dedline_year,
                             sub_proc_ras=for_list_sub_proc_ras, list_for_del=list_all_f_d_s)

        result_summ_sub.append(dict_for_viev)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    project_for_mess = Prime_Project.objects.get(id=project_id)
    if project_for_mess.status_1 == True:
        send_meseges = Comment_For_Project.objects.filter(boss_project__id=project_id, status_1=True)
    if project_for_mess.status_2 == True:
        send_meseges = Comment_For_Project.objects.filter(boss_project__id=project_id, status_2=True)
    if project_for_mess.status_3 == True:
        send_meseges = Comment_For_Project.objects.filter(boss_project__id=project_id, status_3=True)
    if project_for_mess.status_4 == True:
        send_meseges = Comment_For_Project.objects.filter(boss_project__id=project_id, status_4=True)
    if project_for_mess.status_5 == True:
        send_meseges = Comment_For_Project.objects.filter(boss_project__id=project_id, status_5=True)
    if project_for_mess.status_6 == True:
        send_meseges = Comment_For_Project.objects.filter(boss_project__id=project_id, status_6=True)

    # send_meseges = Comment_For_Project.objects.filter(boss_project__id=project_id)

    list_for_mesage = list()
    for send_mesege in send_meseges:
        if send_mesege.who_create.id == int(request.session['user_id']):
            i_true = True
        else:
            i_true = False
        text = str(send_mesege.text_comment)
        data = send_mesege.date_create
        name = send_mesege.who_create

        # id_send_mesege = send_mesege.id
        # boss_project = Prime_Project.objects.get(id=id_send_mesege)

        files_for_view = File_For_Comment.objects.filter(boss_comment=send_mesege)
        list_files = list()
        patch = ""
        view_file = False
        for fil in files_for_view:
            view_file = True
            patch = str(fil.file)
            str_name_file = patch.replace("file_atach_comment/", "")
            dict_file = dict(name=str_name_file, query=fil)
            list_files.append(dict_file)

        dict_for_mesage = dict(i_true=i_true, text=text, data=data, name=name, files_for_view=list_files, patch=patch, view_file=view_file)

        list_for_mesage.append(dict_for_mesage)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    form_button = request.POST

    print(request.POST)
    print(request.FILES)


    def func_done_subproject(id_for_done_subproject):
        sub_project_for_done = Sub_Project.objects.get(id=int(id_for_done_subproject))
        status_1 = sub_project_for_done.status_1
        status_2 = sub_project_for_done.status_2
        status_3 = sub_project_for_done.status_3
        status_4 = sub_project_for_done.status_4
        status_5 = sub_project_for_done.status_5
        status_6 = sub_project_for_done.status_6
        map_sub_project_for_done = sub_project_for_done.map
        print(map_sub_project_for_done, type(map_sub_project_for_done))
        all_sub_go_status = Sub_Project.objects.filter(status_1=status_1, status_2=status_2, status_3=status_3, status_4=status_4,
                                                       status_5=status_5, status_6=status_6)
        len_basis_map = len(map_sub_project_for_done)
        list_sub_for_done = list()
        for sub_go_status in all_sub_go_status:
            map_sub_proj_sub_del = sub_go_status.map
            srez = map_sub_proj_sub_del[0:len_basis_map]
            if srez == map_sub_project_for_done and sub_go_status.id != int(id_for_done_subproject):
                list_sub_for_done.append(sub_go_status.id)
        for elem in list_sub_for_done:
            now_date = datetime.now()
            res_for_trues = Sub_Project_Prime_Data.objects.filter(local_key__id=elem)
            for res in res_for_trues:
                break
            res.date_fact_end = now_date
            res.save()
            Sub_Project.objects.filter(id=elem).update(do_it=True)

        now_date = datetime.now()
        for_trues = Sub_Project_Prime_Data.objects.filter(local_key__id=sub_project_for_done.id)
        for for_true in for_trues:
            break
        for_true.date_fact_end = now_date
        for_true.save()
        Sub_Project.objects.filter(id=sub_project_for_done.id).update(do_it=True)

    def func_del_subproject(id_for_del_subproject):
        print(id_for_del_subproject, type(id_for_del_subproject))
        sub_project_for_del = Sub_Project.objects.get(id=int(id_for_del_subproject))
        status_1 = sub_project_for_del.status_1
        status_2 = sub_project_for_del.status_2
        status_3 = sub_project_for_del.status_3
        status_4 = sub_project_for_del.status_4
        status_5 = sub_project_for_del.status_5
        status_6 = sub_project_for_del.status_6
        map_sub_project_for_del = sub_project_for_del.map
        print(map_sub_project_for_del, type(map_sub_project_for_del))
        all_sub_go_status = Sub_Project.objects.filter(status_1=status_1, status_2=status_2, status_3=status_3, status_4=status_4,
                                                       status_5=status_5, status_6=status_6)
        len_basis_map = len(map_sub_project_for_del)
        list_sub_for_del = list()
        for sub_go_status in all_sub_go_status:
            map_sub_proj_sub_del = sub_go_status.map
            srez = map_sub_proj_sub_del[0:len_basis_map]
            if srez == map_sub_project_for_del and sub_go_status.id != int(id_for_del_subproject):
                list_sub_for_del.append(sub_go_status.id)
        for elem in list_sub_for_del:
            sub_subs = Sub_Project_Sub_Data.objects.filter(local_key__local_key__id=elem)
            sub_subs_main = Sub_Project_Sub_Data.objects.filter(local_key__local_key__id=int(id_for_del_subproject))
            for sub_sub in sub_subs:
                break
            for sub_sub_main in sub_subs_main:
                break
            sub_prims = Sub_Project_Prime_Data.objects.filter(local_key__id=elem)
            sub_prims_main = Sub_Project_Prime_Data.objects.filter(local_key__id=int(id_for_del_subproject))
            for sub_prim in sub_prims:
                break
            for sub_prim_main in sub_prims_main:
                break
            sub = Sub_Project.objects.get(id=elem)
            sub_sub.delete()
            sub_sub_main.delete()
            sub_prim.delete()
            sub_prim_main.delete()
            sub.delete()
        sub_project_for_del.delete()

    def func_reload_subproject(**kwargs):
        form_button = kwargs
        name_subproject = form_button['name_subproject_reload'][0]
        who_work = form_button['who_work_reload'][0]
        who_boss_project = User_Login.objects.get(id=int(who_work))
        date_start_project_month = form_button['date_start_project_month_reload'][0]
        date_start_project_day = form_button['date_start_project_day_reload'][0]
        date_start_project_year = form_button['date_start_project_year_reload'][0]
        date_start = dt.date(int(date_start_project_year), int(date_start_project_month), int(date_start_project_day))
        date_end_project_month = form_button['date_end_project_month_reload'][0]
        date_end_project_day = form_button['date_end_project_day_reload'][0]
        date_end_project_year = form_button['date_end_project_year_reload'][0]
        date_end = dt.date(int(date_end_project_year), int(date_end_project_month), int(date_end_project_day))
        for elem in form_button:
            if "description_subproject_reload_" in elem:
                id_elem = elem.replace("description_subproject_reload_", "")
                description_subproject = form_button[elem][0]
                reload_subproject = Sub_Project.objects.get(id=int(id_elem))
                reload_subproject_prime_datas = Sub_Project_Prime_Data.objects.filter(local_key__id=int(id_elem))
                for reload_subproject_prime_data in reload_subproject_prime_datas:
                    break
                if reload_subproject.name_project != name_subproject or reload_subproject.description_project != description_subproject:
                    reload_subproject.name_project = name_subproject
                    reload_subproject.description_project = description_subproject
                    reload_subproject.save()
                if reload_subproject_prime_data.who_boss_project != who_boss_project or reload_subproject_prime_data.date_start_project != date_start or reload_subproject_prime_data.date_deadline_project != date_end:
                    reload_subproject_prime_data.who_boss_project = who_boss_project
                    reload_subproject_prime_data.date_start_project = date_start
                    reload_subproject_prime_data.date_deadline_project = date_end
                    reload_subproject_prime_data.save()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    if "done_subproject" in form_button and form_button["done_subproject"] != []:
        id_for_done_subproject = form_button["done_subproject"]
        func_done_subproject(id_for_done_subproject)
        return redirect('project', project_id)

    if "del_subproject" in form_button and form_button["del_subproject"] != []:
        id_for_del_subproject = form_button["del_subproject"]
        func_del_subproject(id_for_del_subproject)
        return redirect('project', project_id)

    if "name_subproject_reload" in form_button and "who_work_reload" in form_button:
        func_reload_subproject(**form_button)
        return redirect('project', project_id)


    if "name_subproject_low" in form_button and form_button["name_subproject_low"] != []:
        name_subproject = form_button["name_subproject_low"]
        id_who_work = int(form_button["who_work_low"])
        who_work = User_Login.objects.get(id=id_who_work)

        for element in form_button:
            if element != "csrfmiddlewaretoken":
                if "description_subproject_low_" in element:
                    str_element = str(element)
                    id_cheng = int(str_element.replace("description_subproject_low_", ""))
                    name_description = "description_subproject_low_" + str(id_cheng)

        description_subproject = form_button[name_description]

        date_start_project_month = form_button["date_start_project_month_low"]
        date_start_project_day = form_button["date_start_project_day_low"]
        date_start_project_year = form_button["date_start_project_year_low"]
        date_end_project_month = form_button["date_end_project_month_low"]
        date_end_project_day = form_button["date_end_project_day_low"]
        date_end_project_year = form_button["date_end_project_year_low"]
        prime_project = Prime_Project.objects.get(id=project_id)
        status_1 = prime_project.status_1
        status_2 = prime_project.status_2
        status_3 = prime_project.status_3
        status_4 = prime_project.status_4
        status_5 = prime_project.status_5
        status_6 = prime_project.status_6

        who_create = User_Login.objects.get(id=int(request.session['user_id']))

        create_subproject = Sub_Project.objects.create(name_project=name_subproject, description_project=description_subproject,
                                                       prime_project=prime_project, who_create_project=who_create, status_1=status_1,
                                                       status_2=status_2, status_3=status_3, status_4=status_4, status_5=status_5,
                                                       status_6=status_6)
        key_yacor_project = str('#ps' + str(create_subproject.id))

        pair_for_save = str(id_cheng) + ", " + str(create_subproject.id)


        m_s_p = Sub_Project.objects.get(id=id_cheng)
        sub_projects_main = Sub_Project_Prime_Data.objects.filter(local_key=Sub_Project.objects.get(id=id_cheng))
        for sub_project_main in sub_projects_main:
            break

        re_mapc = m_s_p.map
        re_level = sub_project_main.level_project
        new_level = int(re_level) + 1

        new_map = str(re_mapc) + " " + str(create_subproject.id) + ","

        Sub_Project.objects.filter(id=create_subproject.id).update(pair=pair_for_save, map=new_map)
        date_end = dt.date(int(date_end_project_year), int(date_end_project_month), int(date_end_project_day))
        date_start = dt.date(int(date_start_project_year), int(date_start_project_month), int(date_start_project_day))
        create_subproject_prime_data = Sub_Project_Prime_Data.objects.create(local_key=create_subproject, who_boss_project=who_work,
                                                                             key_yacor_project=key_yacor_project, level_project=new_level,
                                                                             date_start_project=date_start,
                                                                             date_deadline_project=date_end)
        Sub_Project_Sub_Data.objects.create(local_key=create_subproject_prime_data, boss_key=create_subproject)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if "name_subproject" in form_button and form_button["name_subproject"] != []:
        name_subproject = form_button["name_subproject"]
        id_who_work = int(form_button["who_work"])
        who_work = User_Login.objects.get(id=id_who_work)
        description_subproject = form_button["description_subproject"]
        date_start_project_month = form_button["date_start_project_month"]
        date_start_project_day = form_button["date_start_project_day"]
        date_start_project_year = form_button["date_start_project_year"]
        date_end_project_month = form_button["date_end_project_month"]
        date_end_project_day = form_button["date_end_project_day"]
        date_end_project_year = form_button["date_end_project_year"]
        prime_project = Prime_Project.objects.get(id=project_id)
        status_1 = prime_project.status_1
        status_2 = prime_project.status_2
        status_3 = prime_project.status_3
        status_4 = prime_project.status_4
        status_5 = prime_project.status_5
        status_6 = prime_project.status_6

        who_create = User_Login.objects.get(id=int(request.session['user_id']))

        create_subproject = Sub_Project.objects.create(name_project=name_subproject, description_project=description_subproject,
                                                       prime_project=prime_project, who_create_project=who_create, status_1=status_1,
                                                       status_2=status_2, status_3=status_3, status_4=status_4, status_5=status_5,
                                                       status_6=status_6)
        key_yacor_project = str('#ps' + str(create_subproject.id))
        for_save = str(create_subproject.id) + ", "
        Sub_Project.objects.filter(id=create_subproject.id).update(pair=for_save, map=for_save)
        date_end = dt.date(int(date_end_project_year), int(date_end_project_month), int(date_end_project_day))
        date_start = dt.date(int(date_start_project_year), int(date_start_project_month), int(date_start_project_day))
        create_subproject_prime_data = Sub_Project_Prime_Data.objects.create(local_key=create_subproject, who_boss_project=who_work,
                                                                             key_yacor_project=key_yacor_project, level_project=1,
                                                                             date_start_project=date_start,
                                                                             date_deadline_project=date_end)
        Sub_Project_Sub_Data.objects.create(local_key=create_subproject_prime_data, boss_key=create_subproject)



    if "next_stady" in form_button:
        if form_button["all_complite"] == "true":
            id_for_resend = form_button["next_stady"]
            project_for_resend = Prime_Project.objects.get(id=id_for_resend)
            if project_for_resend.status_1 == True:
                Prime_Project.objects.filter(id=id_for_resend).update(status_1=False, status_2=True)
            if project_for_resend.status_2 == True:
                Prime_Project.objects.filter(id=id_for_resend).update(status_2=False, status_3=True)
            if project_for_resend.status_3 == True:
                Prime_Project.objects.filter(id=id_for_resend).update(status_3=False, status_4=True)
            if project_for_resend.status_4 == True:
                Prime_Project.objects.filter(id=id_for_resend).update(status_4=False, status_5=True)
            if project_for_resend.status_5 == True:
                Prime_Project.objects.filter(id=id_for_resend).update(status_5=False, status_6=True)

            return redirect('project', project_id)

    if "reload_description_file_id" in form_button:
        if form_button["del_file_main_project"] != None:
            id_for_del = form_button["del_file_main_project"]
            file_for_del = File_For_Project.objects.get(id=id_for_del)
            file_for_del.delete()
            return redirect('project', project_id)

    if "del_file_main_project" in form_button:
        if form_button["del_file_main_project"] != None:
            id_for_del = form_button["del_file_main_project"]
            file_for_del = File_For_Project.objects.get(id=id_for_del)
            file_for_del.delete()
            return redirect('project', project_id)

    if "description_file" in form_button:
        form_files = request.FILES
        if form_files != {}:
            form_files = form_files["files_for_project"]
            who_create = User_Login.objects.get(id=int(request.session['user_id']))
            boss_project = Prime_Project.objects.get(id=project_id)
            description_file = form_button["description_file"]
            File_For_Project.objects.create(file=form_files, description_file=description_file, boss_project=boss_project,
                                            who_create=who_create)
            return redirect('project', project_id)

    if "text_comment_for_project" in form_button:
        who_create = User_Login.objects.get(id=int(request.session['user_id']))
        boss_project = Prime_Project.objects.get(id=project_id)
        date_create = datetime.now()
        if boss_project.status_1 == True:
            boss_comment = Comment_For_Project.objects.create(text_comment=form_button["text_comment_for_project"],
                                                              who_create=who_create,
                                                              boss_project=boss_project, date_create=date_create,
                                                              status_1=True)
        if boss_project.status_2 == True:
            boss_comment = Comment_For_Project.objects.create(text_comment=form_button["text_comment_for_project"],
                                                              who_create=who_create,
                                                              boss_project=boss_project, date_create=date_create,
                                                              status_2=True)
        if boss_project.status_3 == True:
            boss_comment = Comment_For_Project.objects.create(text_comment=form_button["text_comment_for_project"],
                                                              who_create=who_create,
                                                              boss_project=boss_project, date_create=date_create,
                                                              status_3=True)
        if boss_project.status_4 == True:
            boss_comment = Comment_For_Project.objects.create(text_comment=form_button["text_comment_for_project"],
                                                              who_create=who_create,
                                                              boss_project=boss_project, date_create=date_create,
                                                              status_4=True)
        if boss_project.status_5 == True:
            boss_comment = Comment_For_Project.objects.create(text_comment=form_button["text_comment_for_project"],
                                                              who_create=who_create,
                                                              boss_project=boss_project, date_create=date_create,
                                                              status_5=True)
        if boss_project.status_6 == True:
            boss_comment = Comment_For_Project.objects.create(text_comment=form_button["text_comment_for_project"],
                                                              who_create=who_create,
                                                              boss_project=boss_project, date_create=date_create,
                                                              status_6=True)
        form_files = request.FILES.getlist('files_for_comment_for_project')
        if form_files != None:
            for file in form_files:
                File_For_Comment.objects.create(file=file, boss_comment=boss_comment)
        return redirect('project', project_id)

    if "del_project" in form_button:
        if form_button["del_project"] != None:
            for file in form_button["del_project"]:
                print("Запрос на удаление главного проекта - ", file)

            # Find all sub_projects who connect to main_project (Begin)
            all_sup_projects_for_del = Sub_Project.objects.filter(prime_project__id=int(form_button["del_project"]))
            # Find all sub_projects who connect to main_project (End)

            # Find main_projects (Begin)
            main_priject_for_del = Prime_Project.objects.get(id=form_button["del_project"])
            # Find main_projects (End)

            all_sup_projects_for_del.delete()
            main_priject_for_del.delete()

        return redirect('projects')

    if "upd_project" in form_button:
        id_upd_project = form_button["upd_project"]
        return redirect('upd_project', id_upd_project)

    if "int_sub_project" in form_button:
        id_int_project = form_button["int_sub_project"]
        print("Вход в подпроект с ИД - ", form_button["int_sub_project"])
        return redirect('int_sub_project', int_sub_project_id=id_int_project)


    if "sub_project_go" in form_button:
        id_int_project = form_button["sub_project_go"]
        return redirect('int_sub_project', int_sub_project_id=id_int_project)

    # Del SUBPROJECT element (Begin)
    if "del_sub_project" in form_button:
        all_sup_project = Sub_Project.objects.filter(prime_project__id=prime.id)

        # Make list for del (Begin)
        list_project_for_del = list()
        for element_que in all_sup_project:
            id_elem = element_que.id
            map_elem = element_que.map
            if str(form_button["del_sub_project"]) in map_elem:
                list_project_for_del.append(id_elem)
        # Make list for del (End)

        # Bloc del element (Begin)
        for elem_for_del in list_project_for_del:
            object_for_del = Sub_Project.objects.get(id=elem_for_del)
            object_for_del.delete()
        # Bloc del element (End)

        return redirect('project', prime.id)
    # Del SUBPROJECT element (End)

    if "upd_sub_project_sub" in form_button:
        id_upd_sub_project = form_button["upd_sub_project_sub"]
        upd_sub_project_id = id_upd_sub_project
        request.session['upd_sub_project_main_sub'] = True
        return redirect('upd_sub_project', upd_sub_project_id)

    for element in form_button:
        if element != "csrfmiddlewaretoken":
            if "reload_description_file_id_" in element:
                print("Производиться обновление файла")
                id_cheng = element.replace("reload_description_file_id_", "")
                result_file_reload = File_For_Project.objects.get(id=int(id_cheng))
                print("Производим замену файла в проекте ... ИД файла - ", int(id_cheng))
                text_for_form_file_reload = "reload_description_file_id_" + str(id_cheng)
                new_description = form_button[text_for_form_file_reload]

                r_files = request.FILES
                if r_files != {}:
                    new_files = r_files["reload_files_for_project"]
                    if new_files != result_file_reload.file:
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        boss_project = Prime_Project.objects.get(id=project_id)
                        File_For_Project.objects.filter(id=int(id_cheng)).delete()
                        File_For_Project.objects.create(file=new_files, description_file=new_description, boss_project=boss_project, who_create=who_create)
                else:
                    if new_description != result_file_reload.description_file:
                        File_For_Project.objects.filter(id=int(id_cheng)).update(description_file=new_description)

                return redirect('project', project_id)


    return render(request, 'projects/project.html', locals())




def create_new_subproject(request, create_new_subproject_id):

    form_new_subproject = Form_Create_New_SUBProject(request.POST or None)
    if request.method == "POST":
        if form_new_subproject.is_valid():
            form_new_subproject = form_new_subproject.cleaned_data
            who_create_project = User_Login.objects.get(id=int(request.session['user_id']))
            prime_project = Prime_Project.objects.get(id=int(request.session['project_id']))

            if prime_project.status_1 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_1=True)
            if prime_project.status_2 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_2=True)
            if prime_project.status_3 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_3=True)
            if prime_project.status_4 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_4=True)
            if prime_project.status_5 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_5=True)
            if prime_project.status_6 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_6=True)

            key_yacor_project = str('#ps' + str(create_subproject.id))

            for_save = str(create_subproject.id) + ", "
            Sub_Project.objects.filter(id=create_subproject.id).update(pair=for_save, map=for_save)

            create_subproject_prime_data = Sub_Project_Prime_Data.objects.create(local_key=create_subproject, who_boss_project=form_new_subproject['who_boss_project'],
                                                                                 key_yacor_project=key_yacor_project, level_project=1,
                                                                                 date_start_project=form_new_subproject['date_start_project'],
                                                                                 date_deadline_project=form_new_subproject['date_deadline_project'])

            Sub_Project_Sub_Data.objects.create(local_key=create_subproject_prime_data, boss_key=create_subproject)

            return redirect('project', project_id=request.session['project_id'])

    return render(request, 'projects/create_new_subproject.html', locals())


def create_new_subproject_low(request, create_new_subproject_low_id):

    sub_project_main = Sub_Project.objects.get(id=int(create_new_subproject_low_id))
    sub_projects_prime_data_main = Sub_Project_Prime_Data.objects.filter(local_key__id=int(create_new_subproject_low_id))
    sub_projects_sub_data_main = Sub_Project_Sub_Data.objects.filter(local_key__local_key__id=int(create_new_subproject_low_id))

    for sub_project_prime_data_main in sub_projects_prime_data_main:
        level_sub_project_main = int(sub_project_prime_data_main.level_project)

    level_sub_project_main = level_sub_project_main + 1

    form_new_subproject = Form_Create_New_SUBProject(request.POST or None)
    if request.method == "POST":
        if form_new_subproject.is_valid():
            form_new_subproject = form_new_subproject.cleaned_data

            prime_project = Prime_Project.objects.get(id=int(request.session['project_id']))
            who_create_project = User_Login.objects.get(id=int(request.session['user_id']))

            if prime_project.status_1 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_1=True)
            if prime_project.status_2 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_2=True)
            if prime_project.status_3 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_3=True)
            if prime_project.status_4 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_4=True)
            if prime_project.status_5 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_5=True)
            if prime_project.status_6 == True:
                create_subproject = Sub_Project.objects.create(name_project=form_new_subproject['name'],
                                                               description_project=form_new_subproject[
                                                                   'description_project'],
                                                               prime_project=prime_project,
                                                               who_create_project=who_create_project, status_6=True)

            key_yacor_project = str('#ps' + str(create_subproject.id))

            create_subproject_prime_data = Sub_Project_Prime_Data.objects.create(local_key=create_subproject, who_boss_project=form_new_subproject['who_boss_project'],
                                                                                 key_yacor_project=key_yacor_project, level_project=level_sub_project_main,
                                                                                 date_start_project=form_new_subproject['date_start_project'],
                                                                                 date_deadline_project=form_new_subproject['date_deadline_project'])

            Sub_Project_Sub_Data.objects.create(local_key=create_subproject_prime_data, boss_key=sub_project_main)

            pref = Sub_Project.objects.get(id=sub_project_main.id)
            str_map_boss = pref.map
            for_save = str(str_map_boss) + str(create_subproject.id) + ", "
            Sub_Project.objects.filter(id=create_subproject.id).update(map=for_save)

            list_for_save = [sub_project_main.id, create_subproject.id]
            str_for_save = str(list_for_save)
            str_for_save = str_for_save.replace("[", "")
            str_for_save = str_for_save.replace("]", "")
            Sub_Project.objects.filter(id=create_subproject.id).update(pair=str_for_save)

            return redirect('project', project_id=request.session['project_id'])

    return render(request, 'projects/create_new_subproject_low.html', locals())


def upd_project(request, upd_project_id):

    data_main_projects = Data_Prime_Project.objects.filter(prime_project__id=upd_project_id)

    for data_main_project in data_main_projects:
        break

    datatime_start = datetime.strptime(str(data_main_project.date_start_project), '%Y-%m-%d')
    data_start = str(datatime_start)[:10]
    datatime_deadline = datetime.strptime(str(data_main_project.date_deadline_project), '%Y-%m-%d')
    data_deadline = str(datatime_deadline)[:10]

    info_for_send = dict(name=data_main_project.prime_project.name_project,
                         description_project=data_main_project.prime_project.description_project,
                         who_boss_project=data_main_project.who_boss_project,
                         date_start_project=data_start,
                         date_deadline_project=data_deadline)

    form = Form_Create_New_Project(request.POST or None)
    print("полученный request.POST - ", request.POST)

    data_result = request.POST
    # print("Элемент названия - ", data_result["name"])
    if request.method == "POST":
        Data_Prime_Project.objects.filter(prime_project__id=upd_project_id).update(who_boss_project=data_result["who_boss_project"],
                                                                                   date_start_project=data_result["date_start_project"],
                                                                                   date_deadline_project=data_result["date_deadline_project"])
        Prime_Project.objects.filter(id=upd_project_id).update(name_project=data_result["name"], description_project=data_result["description_project"])

        print("Обновление проведено успешно!")
        return redirect('project', project_id=upd_project_id)

    return render(request, 'projects/upd_project.html', locals())


def int_sub_project(request, int_sub_project_id):
    resave = False
    request.session['id_main_sub_project'] = 0

    sub_projects = Sub_Project_Sub_Data.objects.filter(local_key__local_key__id=int(int_sub_project_id))

    for sub_project in sub_projects:
        break

    all_incom_objects = Incom.objects.filter(sub_project=Sub_Project.objects.get(id=int_sub_project_id))
    sum_incom = int(0)
    for incom_object in all_incom_objects:
        sum_incom = sum_incom + int(incom_object.inc_sub_project)

    all_outcom_objects = Outcom.objects.filter(sub_project=Sub_Project.objects.get(id=int_sub_project_id))
    sum_outcom = int(0)
    for outcom_object in all_outcom_objects:
        sum_outcom = sum_outcom + int(outcom_object.inc_sub_project)

    prib = int(sum_incom) - int(sum_outcom)

    if sum_incom == 0:
        result_proc = round(((0 - sum_outcom) * 100) / 1)
    else:
        result_proc = round(((sum_incom - sum_outcom) * 100) / sum_incom)



    if result_proc >= 0:
        result_proc_dict = dict(znac='+', res=result_proc)

    if result_proc < 0:
        result_proc_dict = dict(znac='-', res=abs(result_proc))

    date = sub_project.local_key.date_create_project
    date_strt = sub_project.local_key.date_start_project
    date_dld = sub_project.local_key.date_deadline_project

    strt_prj = datetime.toordinal(date_strt)
    dld_prj = datetime.toordinal(date_dld)
    now_prg = datetime.toordinal(datetime.now())
    days_proj = dld_prj - strt_prj
    days_now = now_prg - strt_prj

    proc_ras = round((days_now * 100) / days_proj)

    main_for_fin = Sub_Project.objects.get(id=int(int_sub_project_id))

    all_fin_incoms = Incom.objects.filter(sub_project=main_for_fin)

    result_incom = list()
    for fin_incom in all_fin_incoms:
        id = fin_incom.id
        sub_project_v = fin_incom.sub_project
        inc_sub_project_v = fin_incom.inc_sub_project
        description_v = fin_incom.description
        who_create_v = fin_incom.who_create
        date_create_v = fin_incom.date_create

        prom_datas = Incom_Data.objects.filter(local_key=fin_incom)
        for prom_data in prom_datas:
            break

        who_update_v = prom_data.who_update
        date_update_v = prom_data.date_update

        dict_for_result = dict(id=id, sub_project=sub_project_v, inc_sub_project=inc_sub_project_v, description=description_v, who_create=who_create_v,
                 date_create=date_create_v, who_update=who_update_v, date_update=date_update_v)

        result_incom.append(dict_for_result)

    all_fin_outcoms = Outcom.objects.filter(sub_project=main_for_fin)

    result_outcom = list()
    for fin_outcom in all_fin_outcoms:
        id = fin_outcom.id
        sub_project_v = fin_outcom.sub_project
        inc_sub_project_v = fin_outcom.inc_sub_project
        description_v = fin_outcom.description
        who_create_v = fin_outcom.who_create
        date_create_v = fin_outcom.date_create

        prom_datas = Outcom_Data.objects.filter(local_key=fin_outcom)
        print("prom_datas - ", prom_datas)
        for prom_datar in prom_datas:
            print("prom_data - ", prom_datar)
            break
        # print("prom_data - ", prom_datar)
        #
        #
        who_update_v = prom_datar.who_update
        print("who_update_v - ", who_update_v)
        date_update_v = prom_datar.date_update
        print("date_update_v - ", date_update_v)

        dict_for_result = dict(id=id, sub_project=sub_project_v, inc_sub_project=inc_sub_project_v, description=description_v, who_create=who_create_v,
                 date_create=date_create_v, who_update=who_update_v, date_update=date_update_v)

        result_outcom.append(dict_for_result)



    print("Вход осуществлен по ИД подпроекта - ", int_sub_project_id)
    print("Начинаем собирать информация по ИД прикрепленным ниже по уровню")
    main_sub_projects = Sub_Project.objects.get(id=int_sub_project_id)
    print("Вход осуществлен по подпроекту - ", main_sub_projects)
    find_map = main_sub_projects.map
    print("Карта подпроекта под которым вошли - ", find_map)

    main_project_id = main_sub_projects.prime_project.id
    print("Главный проект найден - ", main_project_id)

    id_sub_project_sub_data = Sub_Project_Sub_Data.objects.filter(local_key__local_key__prime_project__id=main_project_id)
    print("Список всех подпроектов имеющих отношение к главному проекту - ", id_sub_project_sub_data)

    list_for_work = list()
    for sub_for_work in id_sub_project_sub_data:
        map_diver_sub_project = sub_for_work.local_key.local_key.map
        position_map_in = map_diver_sub_project.find(find_map)

        if position_map_in > -1 and sub_for_work.local_key.local_key.id != main_sub_projects.id:
            print("Подпроект имеет идентичнуя карту по позиции - ", position_map_in)
            print("ИД подпроекта - ", sub_for_work.local_key.local_key.id)
            print("Наименование подпроекта - ", sub_for_work.local_key.local_key.name_project)
            list_for_work.append(sub_for_work.local_key.local_key.id)


    print("Ведущий подпроект - ", int_sub_project_id)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Find level sub_project (Begin)
    sub_project_for_view = main_sub_projects.id
    find_level_subs = Sub_Project_Prime_Data.objects.filter(local_key__id=sub_project_for_view)
    for find_level_sub in find_level_subs:
        break
    level_not = find_level_sub.level_project
    print("Уровень главного подпроекта - ", level_not)
    # Find level sub_project (End)
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    list_for_work = sorted(list_for_work)

    if list_for_work == []:
        return render(request, 'projects/int_sub_project.html', locals())


    print("Список подпроектов которые должны быть отображены - ", list_for_work)



    pair = list()
    num = list()
    for sub_project_for_work in list_for_work:
        list_sub_data = Sub_Project_Sub_Data.objects.filter(local_key__local_key__id=sub_project_for_work)
        for sub_data in list_sub_data:
            break
        id_boss = sub_data.boss_key.id
        id_boss = sub_data.boss_key.id
        dict_id_for_save = dict(id_boss=id_boss, id_himself=sub_project_for_work)

        pair.append(dict_id_for_save)

        num.append(id_boss)
        num.append(sub_project_for_work)


    print("Пары ИД для обработки - ", pair)
    num = sorted(num)
    print("Список всех ИД которые фигурируют в парах - ", num)

    etalon_num = list()
    for nu in num:
        if nu not in etalon_num:
            etalon_num.append(nu)

    print("Список ИД эталонный - ", etalon_num)
    print("Список ИД идущий на обрабоку - ", list_for_work)

    list_for_work = etalon_num


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
    re_list = list()
    for one in pair:
        id_boss = one['id_boss']
        id_himself = one['id_himself']

        if id_boss != id_himself:
            position_now = list_for_work.index(id_himself)
            position_move = int(list_for_work.index(id_boss)) + 1

            if position_now != position_move:
                list_for_work.remove(id_himself)
                list_for_work.insert(position_move, id_himself)

    list_for_work.remove(main_sub_projects.id)

    # Find level sub_project (Begin)
    sub_project_for_view = main_sub_projects.id
    find_level_subs = Sub_Project_Prime_Data.objects.filter(local_key__id=sub_project_for_view)
    for find_level_sub in find_level_subs:
        break
    level_not = find_level_sub.level_project
    # Find level sub_project (End)

    print('Результат обработки - ', list_for_work)

    list_all_active_subproject_true = list()
    for id in list_for_work:
        list_all_active_subproject_true.append(Sub_Project.objects.get(id=int(id)))

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    print("Проверка полного списка для вывода - ", list_all_active_subproject_true)
    result_summ_sub = list()

    for prom in list_all_active_subproject_true:
        id_project_prom = prom.id
        for_list_sub_name_project = prom.name_project
        for_list_sub_description_project = prom.description_project

        for_list_sub_create_name = prom.who_create_project.name
        for_list_sub_create_last_name = prom.who_create_project.last_name
        for_list_sub_create_surname = prom.who_create_project.surname

        result_create = for_list_sub_create_name + ' ' + for_list_sub_create_last_name + ' ' + for_list_sub_create_surname

        proms = Sub_Project_Prime_Data.objects.filter(local_key_id=id_project_prom)
        for promn in proms:
            break

        for_list_sub_boss_name = promn.who_boss_project.name
        for_list_sub_boss_last_name = promn.who_boss_project.last_name
        for_list_sub_boss_surname = promn.who_boss_project.surname

        result_boss = for_list_sub_boss_name + ' ' + for_list_sub_boss_last_name + ' ' + for_list_sub_boss_surname

        for_list_sub_rss = (int(promn.level_project) - level_not) * 50

        for_list_sub_level = promn.level_project

        date_create_project = promn.date_create_project
        date_start_project = promn.date_start_project
        date_deadline_project = promn.date_deadline_project

        start_prj = datetime.toordinal(date_start_project)
        dedlayn_prj = datetime.toordinal(date_deadline_project)
        now_day = datetime.toordinal(datetime.now())
        for_days_proj = dedlayn_prj - start_prj
        for_days_now = now_day - start_prj

        for_list_sub_proc_ras = round((for_days_now * 100) / for_days_proj)

        for_list_date_create = date_create_project.strftime("%d-%m-%Y")
        for_list_date_start = date_start_project.strftime("%d-%m-%Y")
        for_list_date_dedline = date_deadline_project.strftime("%d-%m-%Y")

        dict_for_viev = dict(id_subproject=id_project_prom, name_project=for_list_sub_name_project, description_project=for_list_sub_description_project,
                             who_create_project=result_create, who_boss_project=result_boss, rass=for_list_sub_rss ,level_project=for_list_sub_level,
                             date_create_project=for_list_date_create, date_start_project=for_list_date_start, date_deadline_project=for_list_date_dedline,
                             sub_proc_ras=for_list_sub_proc_ras)

        result_summ_sub.append(dict_for_viev)

    form_button = request.POST

    print("request.POST - ", form_button)

    if "incom_send" in form_button:
        print("Внесение дохода - ", form_button["incom_send"])
        for_create_sub_project = Sub_Project.objects.get(id=int_sub_project_id)
        for_create_user = User_Login.objects.get(id=int(request.session['user_id']))
        local_key = Incom.objects.create(sub_project=for_create_sub_project, inc_sub_project=form_button["incom_send"], who_create=for_create_user, description=form_button["comment"])
        Incom_Data.objects.create(local_key=local_key, who_update=for_create_user, date_update=local_key.date_create)
        print("Создание доходной позиции закончено!")
        return redirect('int_sub_project', int_sub_project_id)

    if "outcom_send" in form_button:
        print("Внесение расхода - ", form_button["outcom_send"])
        for_create_sub_project = Sub_Project.objects.get(id=int_sub_project_id)
        for_create_user = User_Login.objects.get(id=int(request.session['user_id']))
        local_key = Outcom.objects.create(sub_project=for_create_sub_project, inc_sub_project=form_button["outcom_send"], who_create=for_create_user, description=form_button["comment"])
        Outcom_Data.objects.create(local_key=local_key, who_update=for_create_user, date_update=local_key.date_create)
        print("Создание расходной позиции закончено!")
        return redirect('int_sub_project', int_sub_project_id)


    if "int_sub_project" in form_button:
        id_int_project = form_button["int_sub_project"]
        print("Вход в подпроект с ИД - ", form_button["int_sub_project"])
        return redirect('int_sub_project', int_sub_project_id=id_int_project)

    if "upd_sub_project_main" in form_button:
        id_upd_sub_project = form_button["upd_sub_project_main"]
        print("Вход в подпроект с ИД - ", form_button["upd_sub_project_main"])
        # request.session['sub_project_id'] = form_button["int_sub_project"]
        request.session['upd_sub_project_sub_main'] = True
        return redirect('upd_sub_project', id_upd_sub_project)

    if "upd_sub_project_sub" in form_button:
        id_upd_sub_project = form_button["upd_sub_project_sub"]
        request.session['upd_sub_project_sub_sub'] = True
        request.session['id_main_sub_project'] = int_sub_project_id
        return redirect('upd_sub_project', id_upd_sub_project)

    if "del_sub_project_main" in form_button:
        id_int_project = form_button["del_sub_project_main"]
        main_sub_project = Sub_Project.objects.get(id=id_int_project)
        map_main_sub_project = str(main_sub_project.map)
        prime_main_sub_project = main_sub_project.prime_project.id

        all_sub_projects = Sub_Project.objects.filter(prime_project__id=prime_main_sub_project)

        list_el_for_del = list()
        for sub_proj in all_sub_projects:
            map_for_search = sub_proj.map
            find_map = map_for_search.find(map_main_sub_project)

            if find_map > -1:
                if int(id_int_project) != int(sub_proj.id):
                    list_el_for_del.append(sub_proj.id)
        Sub_Project.objects.get(id=int(id_int_project)).delete()
        for element in list_el_for_del:
            Sub_Project.objects.get(id=int(element)).delete()

        return redirect('project', prime_main_sub_project)

    if "del_sub_project" in form_button:
        id_int_project = form_button["del_sub_project"]
        main_sub_project = Sub_Project.objects.get(id=id_int_project)
        map_main_sub_project = str(main_sub_project.map)
        prime_main_sub_project = main_sub_project.prime_project.id

        all_sub_projects = Sub_Project.objects.filter(prime_project__id=prime_main_sub_project)

        list_el_for_del = list()
        for sub_proj in all_sub_projects:
            map_for_search = sub_proj.map
            find_map = map_for_search.find(map_main_sub_project)

            if find_map > -1:
                if int(id_int_project) != int(sub_proj.id):
                    list_el_for_del.append(sub_proj.id)
        Sub_Project.objects.get(id=int(id_int_project)).delete()
        for element in list_el_for_del:
            Sub_Project.objects.get(id=int(element)).delete()
        return redirect('project', prime_main_sub_project)


    list_elems = list()
    list_cheng_incom = list()
    list_cheng_incom_description = list()
    list_cheng_incom_del = list()
    for elem in form_button:
        if elem != "csrfmiddlewaretoken":
            if "cheng_incom_id_" in elem:
                for_work = elem.replace("cheng_incom_id_", "")
                name = "cheng_incom_id_" + str(for_work)
                result = form_button[name]
                prom_incom_sum = Incom.objects.get(id=int(for_work))
                if prom_incom_sum.inc_sub_project != result:
                    Incom.objects.filter(id=int(for_work)).update(inc_sub_project=result)
                    main_obj = Incom.objects.get(id=int(for_work))
                    sub_main = Incom_Data.objects.filter(local_key__id=main_obj.id)
                    if bool(sub_main) != False:
                        resave = True
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        sub_main.update(who_update=who_create, date_update=datetime.now())

            if "cheng_incom_description_id_" in elem:
                for_work = elem.replace("cheng_incom_description_id_", "")
                name = "cheng_incom_description_id_" + str(for_work)
                result = form_button[name]
                prom_incom_description = Incom.objects.get(id=int(for_work))
                if prom_incom_description.description != result:
                    Incom.objects.filter(id=int(for_work)).update(description=result)
                    main_obj = Incom.objects.get(id=int(for_work))
                    sub_main = Incom_Data.objects.filter(local_key__id=main_obj.id)
                    if bool(sub_main) != False:
                        resave = True
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        sub_main.update(who_update=who_create, date_update=datetime.now())

            if "cheng_incom_del" in elem:
                resave = True
                if form_button["cheng_incom_del"] != None:
                    str_for_del = form_button["cheng_incom_del"]
                    if "," not in str_for_del:
                        id = int(str_for_del)
                        Incom.objects.filter(id=id).delete()
                    else:
                        list_for_del = str_for_del.split(", ")
                        for elem_for_del in list_for_del:
                            Incom.objects.filter(id=int(elem_for_del)).delete()

            if "cheng_outcom_id_" in elem:
                for_work = elem.replace("cheng_outcom_id_", "")
                name = "cheng_outcom_id_" + str(for_work)
                result = form_button[name]
                prom_outcom_sum = Outcom.objects.get(id=int(for_work))
                if prom_outcom_sum.inc_sub_project != result:
                    Outcom.objects.filter(id=int(for_work)).update(inc_sub_project=result)
                    main_obj = Outcom.objects.get(id=int(for_work))
                    sub_main = Outcom_Data.objects.filter(local_key__id=main_obj.id)
                    if bool(sub_main) != False:
                        resave = True
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        sub_main.update(who_update=who_create, date_update=datetime.now())

            if "cheng_outcom_description_id_" in elem:
                for_work = elem.replace("cheng_outcom_description_id_", "")
                name = "cheng_outcom_description_id_" + str(for_work)
                result = form_button[name]
                prom_outcom_description = Outcom.objects.get(id=int(for_work))
                if prom_outcom_description.description != result:
                    Outcom.objects.filter(id=int(for_work)).update(description=result)
                    main_obj = Outcom.objects.get(id=int(for_work))
                    sub_main = Outcom_Data.objects.filter(local_key__id=main_obj.id)
                    if bool(sub_main) != False:
                        resave = True
                        who_create = User_Login.objects.get(id=int(request.session['user_id']))
                        sub_main.update(who_update=who_create, date_update=datetime.now())

            if "cheng_outcom_del" in elem:
                resave = True
                if form_button["cheng_outcom_del"] != None:
                    str_for_del = form_button["cheng_outcom_del"]
                    if "," not in str_for_del:
                        id = int(str_for_del)
                        Outcom.objects.filter(id=id).delete()
                    else:
                        list_for_del = str_for_del.split(", ")
                        for elem_for_del in list_for_del:
                            Outcom.objects.filter(id=int(elem_for_del)).delete()

    if resave == True:
        return redirect('int_sub_project', int_sub_project_id)

    return render(request, 'projects/int_sub_project.html', locals())


def upd_sub_project(request, upd_sub_project_id):
    save_sub_project = ""

    if request.session['upd_sub_project_sub_sub'] == True:
        print("Производим обновление (изменение) в подпроекте мини подпроекта")
        id_main_sub_project = request.session['id_main_sub_project']
        save_sub_project = "update_sub_sub"

    if request.session['upd_sub_project_sub_main'] == True:
        print("Производим обновление (изменение) в подпроекте главного подпроекта")
        save_sub_project = "update_sub_main"

    if request.session['upd_sub_project_main_sub'] == True:
        print("Производим обновление (изменение) в подпроекте главного проекта")
        save_sub_project = "update_main_sub"


    data_main_sub_projects = Sub_Project_Sub_Data.objects.filter(local_key__local_key__id=upd_sub_project_id)

    for data_main_sub_project in data_main_sub_projects:
        break

    data_main_sub_project_prime_data = data_main_sub_project.local_key
    id_data_main_sub_project_prime_data = data_main_sub_project_prime_data.id
    data_sub_project = data_main_sub_project_prime_data.local_key
    id_data_sub_project = data_sub_project.id
    id_main_project = data_sub_project.prime_project.id

    datatime_start = datetime.strptime(str(data_main_sub_project.local_key.date_start_project), '%Y-%m-%d')
    data_start = str(datatime_start)[:10]
    datatime_deadline = datetime.strptime(str(data_main_sub_project.local_key.date_deadline_project), '%Y-%m-%d')
    data_deadline = str(datatime_deadline)[:10]

    info_for_send = dict(name=data_main_sub_project.local_key.local_key.name_project,
                         description_project=data_main_sub_project.local_key.local_key.description_project,
                         who_boss_project=data_main_sub_project.local_key.who_boss_project,
                         date_start_project=data_start,
                         date_deadline_project=data_deadline)

    print("полученный request.POST - ", request.POST)

    if save_sub_project == "update_sub_sub":
        if request.method == "POST":
            data_result = request.POST
            Sub_Project_Prime_Data.objects.filter(id=id_data_main_sub_project_prime_data).update(
                who_boss_project=data_result["who_boss_project"],
                date_start_project=data_result["date_start_project"],
                date_deadline_project=data_result["date_deadline_project"])
            Sub_Project.objects.filter(id=id_data_sub_project).update(name_project=data_result["name"],
                                                                      description_project=data_result[
                                                                          "description_project"])
            print("Обновление мини подпроекта на мини подпроекте проведено успешно!")
            request.session['upd_sub_project_sub_sub'] = False
            return redirect('int_sub_project', id_main_sub_project)

    if save_sub_project == "update_main_sub":
        if request.method == "POST":
            data_result = request.POST
            Sub_Project_Prime_Data.objects.filter(id=id_data_main_sub_project_prime_data).update(who_boss_project=data_result["who_boss_project"],
                                                                                                 date_start_project=data_result["date_start_project"],
                                                                                                 date_deadline_project=data_result["date_deadline_project"])
            Sub_Project.objects.filter(id=id_data_sub_project).update(name_project=data_result["name"],
                                                                      description_project=data_result["description_project"])
            print("Обновление мини подпроекта на основном подпроекте проведено успешно!")
            request.session['upd_sub_project_main_sub'] = False
            for_main_go = Sub_Project.objects.get(id=id_data_sub_project)
            id_main_project = for_main_go.prime_project.id
            return redirect('project', id_main_project)

    if save_sub_project == "update_sub_main":
        if request.method == "POST":
            data_result = request.POST
            Sub_Project_Prime_Data.objects.filter(id=id_data_main_sub_project_prime_data).update(
                who_boss_project=data_result["who_boss_project"],
                date_start_project=data_result["date_start_project"],
                date_deadline_project=data_result["date_deadline_project"])
            Sub_Project.objects.filter(id=id_data_sub_project).update(name_project=data_result["name"],
                                                                      description_project=data_result[
                                                                          "description_project"])
            print("Обновление главного подпроекта на главном подпроекте проведено успешно!")
            request.session['upd_sub_project_sub_main'] = False
            for_main_sub_go = Sub_Project.objects.get(id=id_data_sub_project)
            upd_sub_project_id = for_main_sub_go.id
            return redirect('int_sub_project', upd_sub_project_id)

    return render(request, 'projects/upd_sub_project.html', locals())