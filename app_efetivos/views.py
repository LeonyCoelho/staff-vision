from django.shortcuts import render, get_object_or_404, redirect
from app_efetivos.models import Establishment, Sector, Sub_Sector, Position, Shift, Global_Settings, Status, Theme, Worker, CustomUser, Dashboard_Presets, Preset_Settings
from .forms import EstablishmentForm, SectorForm, SubSectorForm, PositionForm, ShiftForm, StatusForm, ImageUploadForm, ImageUploadForm_Bg, PresetForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from openpyxl import Workbook, load_workbook
import pandas as pd
from .forms import UploadFileForm
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from collections import defaultdict
from django.urls import reverse
import json



###############################################################################
# DASHBOARD

def dashboard(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    user = request.user

    # Obtenha os presets associados ao usuário logado
    user_presets = user.customuser.preset.all()
    print(user_presets)

    # Inicialize worker_counts como uma lista vazia
    worker_counts = []

    if user_presets.exists():
        print('usuario com preset')
        
        # Crie uma lista de dicionários para armazenar a contagem de trabalhadores por setor e status
        for preset in user_presets:
            preset_settings = Preset_Settings.objects.filter(preset=preset).order_by('sector_position')
            preset_sectors = preset.preset_sectors.all()  # Setores associados a este preset

            for preset_setting in preset_settings:
                sector = preset_setting.sector

                # Verifique se este setor está contido nos setores do preset
                if sector in preset_sectors:
                    sector_width = preset_setting.sector_width
                    sector_data = {'sector': sector, 'status_counts': {}, 'sector_width': sector_width}

                    status_list = Status.objects.all()
                    for status in status_list:
                        count = Worker.objects.filter(sector_w=sector, status_w=status).count()
                        sector_data['status_counts'][status] = count

                    worker_counts.append(sector_data)

        context = {
            'globalsettings': globalsettings,
            'worker_counts': worker_counts,
            'status_list': status_list,
        }
        return render(request, 'dashboard.html', context)
    
    else:
        print('usuario sem preset')
        context = {
            'globalsettings': globalsettings,
        }
        return render(request, 'no_preset.html', context)












###############################################################################
# VIEW BY SECTOR

def view_by_sector(request, id):
    globalsettings = Global_Settings.objects.all().latest('id')
    selected_sector = get_object_or_404(Sector, id=id)
    sector_workers = Worker.objects.filter(sector_w=selected_sector)

    status_counts = {}

    for worker in sector_workers:
        for status in worker.status_w.all():
            status_name = status.status_name
            if status_name not in status_counts:
                status_counts[status_name] = {
                    'count': 1,
                    'status_obj': status,  # Adicione o objeto Status aqui
                }
            else:
                status_counts[status_name]['count'] += 1


    context = {
        'globalsettings':globalsettings,
        'selected_sector':selected_sector,
        'sector_workers':sector_workers,
        'status_counts': status_counts,
    }
    return render(request, 'view_by_sector.html', context)


###############################################################################
# VIEW BY STATUS

def view_by_status(request, id):
    globalsettings = Global_Settings.objects.all().latest('id')
    selected_status = get_object_or_404(Status, id=id)
    status_workers = Worker.objects.filter(status_w=selected_status)

    sector_counts = {}

    for worker in status_workers:
        for sector in worker.sector_w.all():
            sector_name = sector.sector_name
            if sector_name not in sector_counts:
                sector_counts[sector_name] = {
                    'count': 1,
                    'sector_obj': sector,  # Adicione o objeto sector aqui
                }
            else:
                sector_counts[sector_name]['count'] += 1


    context = {
        'globalsettings':globalsettings,
        'selected_status':selected_status,
        'status_workers':status_workers,
        'sector_counts': sector_counts,
    }
    return render(request, 'view_by_status.html', context)




###############################################################################
# USERS

def users(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    user_list = CustomUser.objects.all()

    user_data = []  # Lista para armazenar os dados de usuário a serem passados para o template

    for user in user_list:
        # Obtenha os nomes dos setores do usuário atual
        sector_names = ", ".join(sector.sector_name for sector in user.sector.all())
        
        user_data.append({
            'id': user.id,
            'username': user.get_username(),
            'name': user.name,
            'sector_names': sector_names,
            'is_staff': user.user.is_staff,
        })

    context = {
        'globalsettings': globalsettings,
        'user_data': user_data,  # Passa a lista de dados de usuário para o template
    }
    return render(request, 'users.html', context)

def edit_user(request, id):
    globalsettings = Global_Settings.objects.all().latest('id')
    sectors_list = Sector.objects.all()
    preset_list = Dashboard_Presets.objects.all()
    custom_user = get_object_or_404(CustomUser, id=id)

    if request.method == 'POST':
        name = request.POST['name']
        is_staff = request.POST.get('is_staff')
        is_staff = is_staff == '1' 
        sector_ids = request.POST.getlist('selected_items_sector')
        sectors = Sector.objects.filter(id__in=sector_ids)
        preset_id = request.POST.get('preset')
        selected_preset = Dashboard_Presets.objects.get(id=preset_id)
        custom_user.preset.clear() 
        custom_user.preset.add(selected_preset)
        custom_user.user.username = name
        custom_user.user.is_staff = is_staff
        custom_user.sector.set(sectors)
        custom_user.save()

        # Redirecione para a página de detalhes do usuário após a edição
        return redirect('users')

    context = {
        'globalsettings': globalsettings,
        'sectors_list': sectors_list,
        'custom_user': custom_user,
        'preset_list':preset_list,
    }
    return render(request, 'edit_user.html', context)

def delete_user(request, id):
    custom_user = get_object_or_404(CustomUser, id=id)
    
    if request.method == 'POST':
        custom_user.user.delete()
        return redirect('users')  # Redirecionar para a página de listagem de usuários após a exclusão
    
    context = {
        'custom_user': custom_user,
    }
    return redirect('users')

def new_user(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    sectors_list = Sector.objects.all()
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        is_staff = request.POST.get('is_staff') == '1'  # Verifique se o campo is_staff foi marcado


        if password != confirm_password:
            return render(request, 'new_user.html', {'wrong_password': True})
        if User.objects.filter(username=username).exists():
            return render(request, 'new_user.html', {'user_exists': True})

        # Obtenha a lista de setores selecionados
        sector_ids = request.POST.getlist('selected_items_sector')
        sectors = Sector.objects.filter(id__in=sector_ids)

        user = User.objects.create_user(username=username, password=password)
        user.is_staff = is_staff  # Defina a propriedade is_staff do usuário
        user.save()
        

        new_user = CustomUser.objects.create(
            user=user,
            name=name,
        )
        new_user.sector.set(sectors)
        new_user.save()

        return redirect('users')

    context = {
        'globalsettings': globalsettings,
        'sectors_list': sectors_list,
    }
    return render(request, 'new_user.html', context)



    context = {
        'globalsettings':globalsettings,
        'sectors_list':sectors_list,
    }
    return render(request, 'new_user.html', context)

###############################################################################
# DASHBOARD SETTINGS

def dashboard_settings(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    preset_list = Dashboard_Presets.objects.all()
    sector_list = Sector.objects.all()


    if request.method == 'POST':
        preset_form = PresetForm(request.POST)
        if preset_form.is_valid():
            preset_form.save()
            return redirect('dashboard_settings')

    preset_form = PresetForm()


    preset_details = {}
    for preset in preset_list:
        preset_details[preset.id] = {
            'preset_name': preset.preset_name,
        }

    context = {
        'globalsettings': globalsettings,
        'preset_list': preset_list,
        'sector_list': sector_list,
        'preset_form': preset_form,
        'preset_details': preset_details,  
    }
    return render(request, 'dashboard_settings.html', context)

def delete_selected_presets(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items_preset[]') 
        try:
            Dashboard_Presets.objects.filter(id__in=selected_items).delete()
        except Exception as e:
            print(e)
    return redirect('dashboard_settings') 

def edit_preset(request, id):
    globalsettings = Global_Settings.objects.all().latest('id')
    sectors_list = Sector.objects.all()
    preset = get_object_or_404(Dashboard_Presets, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        sector_ids = request.POST.getlist('selected_items_sector')  # Mude 'sector[]' para 'selected_items_sector'
        sectors = Sector.objects.filter(id__in=sector_ids)

        # Atualize o nome do preset
        preset.preset_name = name
        preset.save()

        # Use o método set() para definir os setores associados ao preset ManyToMany
        preset.preset_sectors.set(sectors)

        # Defina as posições e larguras progressivas para os setores
        position = 1  # Comece com a posição 1
        for sector in sectors:
            preset_settings, created = Preset_Settings.objects.get_or_create(preset=preset, sector=sector)
            preset_settings.sector_position = position
            preset_settings.sector_width = 3  # Altere a largura conforme necessário
            preset_settings.save()
            position += 1

        # Redirecione para a página de configurações do painel
        return HttpResponseRedirect(reverse('dashboard_settings'))  # Use HttpResponseRedirect para redirecionar

    context = {
        'globalsettings': globalsettings,
        'sectors_list': sectors_list,
        'preset': preset,
    }

    return render(request, 'edit_preset.html', context)
    
def update_position(request, id):
    if request.method == 'POST':
        preset_id = id
        sector_id = request.POST.get('sector_id')
        position = request.POST.get('position')
        width = request.POST.get('width')

        # Recupere o objeto Preset_Settings correspondente
        preset_settings = Preset_Settings.objects.get(preset__id=preset_id, sector__id=sector_id)

        # Atualize as posições e larguras
        preset_settings.sector_position = position
        preset_settings.sector_width = width
        print(sector_id,'==>',  preset_settings.sector_position)
        preset_settings.save()

    return redirect('edit_layout', id=id)

def auto_update_positions(request, id):
    print('Preset ID:', id)
    preset = get_object_or_404(Dashboard_Presets, id=id)

    # Obtenha os setores associados ao preset
    sectors = preset.preset_sectors.all()
    print('Setores associados:', sectors)

    # Defina as posições e larguras progressivas para os setores
    position = 1
    for sector in sectors:
        preset_settings, created = Preset_Settings.objects.get_or_create(preset=preset, sector=sector)
        preset_settings.sector_position = position
        preset_settings.sector_width = 4
        preset_settings.save()
        position += 1
        print(preset_settings.sector_id, '==>', preset_settings.sector_position)

    return redirect('dashboard_settings')  # Redireciona para a página de configurações do painel

def reset_update_positions(request, id):
    print('Preset ID:', id)
    preset = get_object_or_404(Dashboard_Presets, id=id)

    # Obtenha os setores associados ao preset
    sectors = preset.preset_sectors.all()
    print('Setores associados:', sectors)

    # Defina as posições e larguras progressivas para os setores
    position = 1
    for sector in sectors:
        preset_settings, created = Preset_Settings.objects.get_or_create(preset=preset, sector=sector)
        preset_settings.sector_position = position
        preset_settings.sector_width = 3
        preset_settings.save()
        position += 1
        print(preset_settings.sector_id, '==>', preset_settings.sector_position)

    return redirect('edit_layout', id=id)  # Redireciona para a página de configurações do painel

def update_positions(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Decodifique os dados JSON
            data = [int(sector_id) for sector_id in data]  # Converta os IDs para inteiros
            for index, sector_id in enumerate(data):
                preset_settings = Preset_Settings.objects.get(preset__id=id, sector__id=sector_id)
                new_position = index + 1

                # Atualize a posição do setor usando F() expressions para evitar violar a restrição única
                Preset_Settings.objects.filter(preset__id=id, sector_position__gte=new_position).update(
                    sector_position=F('sector_position') + 1
                )

                preset_settings.sector_position = new_position
                preset_settings.save()

            return JsonResponse({'message': 'Ordem atualizada com sucesso!'})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'message': f'Erro: {str(e)}'}, status=400)

    return JsonResponse({'message': 'Método de solicitação inválido.'}, status=400)



def edit_layout(request, id):
    globalsettings = Global_Settings.objects.all().latest('id')
    preset = get_object_or_404(Dashboard_Presets, id=id)
    preset_id = preset.id

    
    # Acesse a relação ManyToMany com a tabela intermediária 'preset_sectors' e, em seguida, acesse o id
    preset_sectors = preset.preset_sectors.through.objects.filter(dashboard_presets_id=id)

    print(preset_sectors)
    if  preset_sectors:
        print('preset contem setores')
        # Crie uma lista para armazenar os valores que você deseja imprimir
        values_to_print = []

        # Itere pelos setores e acesse os valores necessários
        for preset_sector in preset_sectors:
            preset_name = preset.preset_name
            preset_settings = []
            sector_name = preset_sector.sector.sector_name 
            sector_id_name = preset_sector.sector_id
            dashboard_presets_id = preset_sector.id
            try:
                preset_settings = Preset_Settings.objects.get(preset=preset, sector=preset_sector.sector)
                sector_position = preset_settings.sector_position
                sector_width = preset_settings.sector_width
            except Preset_Settings.DoesNotExist:
                sector_position = None
                sector_width = None

            values_to_print.append({
                'Preset': preset_name,
                'Sector': sector_name,
                'SectorID': sector_id_name,
                'ID': sector_id_name,
                'Order': sector_position,
                'Width': sector_width,
            })

        values_to_print = sorted(values_to_print, key=lambda x: x['Order'])

        context = {
            'globalsettings': globalsettings,
            'preset': preset,
            'values_to_print': values_to_print,
            'preset_sectors':preset_sectors,
            'preset_settings':preset_settings,
        }

        return render(request, 'edit_layout.html', context)
    else:
        print('preset nao contem setores')
        print(preset_id)
        context = {
            'globalsettings':globalsettings,
            'preset_id':preset_id,
        }
    return render(request, 'no_sector_preset.html', context)
    


def update_sector_width(request, sector_id, new_width):
    try:
        # Recupere o setor com base no `sector_id`
        sector_settings = Preset_Settings.objects.filter(sector_id=sector_id).first()


        # Atualize a largura do setor com o novo valor
        sector_settings.sector_width = new_width
        sector_settings.save()

        return JsonResponse({'message': 'Largura do setor atualizada com sucesso!'})
    except Preset_Settings.DoesNotExist:
        return JsonResponse({'message': 'Setor não encontrado.'}, status=400)



###############################################################################
# WORKERS

def new_worker(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    position_list = Position.objects.all()
    establishment_list = Establishment.objects.all()
    shift_list = Shift.objects.all()
    sector_list = Sector.objects.all()
    subSector_list = Sub_Sector.objects.all()
    user = request.user
    setores_usuario = user.customuser.sector.all() if hasattr(user, 'customuser') else None

    if setores_usuario:
        workers = Worker.objects.filter(sector_w__in=setores_usuario)
    else:
        workers = Worker.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        position_name = request.POST.get('position')
        establishment_name = request.POST.get('establishment')
        shift_name = request.POST.get('shift')
        sector_name = request.POST.get('sector')
        subSector_name = request.POST.get('subSector')

        # Recupere os objetos de Position, Establishment, Shift e Sector
        position = Position.objects.get(position_name=position_name)
        establishment = Establishment.objects.get(establishment_name=establishment_name)
        shift = Shift.objects.get(shift_name=shift_name)
        sector = Sector.objects.get(sector_name=sector_name)
        subSector = Sub_Sector.objects.get(subSector_name=subSector_name)

        # Crie uma instância de Worker com os valores fornecidos
        new_worker = Worker(
            name_w=name,
            number_w=number,
            observation_w="",  # Certifique-se de fornecer um valor padrão para este campo
        )

        # Salve a instância de Worker no banco de dados
        new_worker.save()

        # Adicione os objetos relacionados usando o método set()
        new_worker.position_w.set([position])
        new_worker.establishment_w.set([establishment])
        new_worker.shift_w.set([shift])
        new_worker.sector_w.set([sector])
        new_worker.subSector_w.set([subSector])

        if Worker.objects.filter(number_w=new_worker.number_w).exists():
            return render(request, 'new_worker.html', {'number_exists': True})
        
        return redirect('update_worker')



    context = {
        'globalsettings': globalsettings,
        'position_list': position_list,
        'establishment_list': establishment_list,
        'shift_list': shift_list,
        'sector_list': sector_list,
        'subSector_list': subSector_list,
        'setores_usuario':setores_usuario,
    }
    return render(request, 'new_worker.html', context)


def update_worker(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    sectors_list = Sector.objects.all()
    preset_list = Dashboard_Presets.objects.all()

    context = {
        'globalsettings':globalsettings,
        'sectors_list':sectors_list,
        'preset_list':preset_list,
    }
    return render(request, 'update_worker.html', context)



def update_worker(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    user = request.user
    setores_usuario = user.customuser.sector.all() if hasattr(user, 'customuser') else None

    if setores_usuario:
        workers = Worker.objects.filter(sector_w__in=setores_usuario)
    else:
        workers = Worker.objects.all()

    status_list = Status.objects.all()

    if request.method == 'POST':
        for worker in workers:
            status_w_key = f"status_w_{worker.id_worker}"
            observation_w_key = f"observation_w_{worker.id_worker}"
            status_name = request.POST.get(status_w_key)
            observation_w = request.POST.get(observation_w_key)

            if status_name:
                status_w = Status.objects.get(status_name=status_name)
                worker.status_w.set([status_w])

            if observation_w is not None:
                worker.observation_w = observation_w

            worker.save()

    context = {
        'globalsettings': globalsettings,
        'workers': workers,
        'status_list': status_list,
        'setores_usuario': setores_usuario,
    }
    return render(request, 'update_worker.html', context)

def adjust_worker(request):
    globalsettings = Global_Settings.objects.all().latest('id')
    position_list = Position.objects.all()
    establishment_list = Establishment.objects.all()
    shift_list = Shift.objects.all()
    sector_list = Sector.objects.all()
    subSector_list = Sub_Sector.objects.all()
    user = request.user
    setores_usuario = user.customuser.sector.all() if hasattr(user, 'customuser') else None

    if setores_usuario:
        workers = Worker.objects.filter(sector_w__in=setores_usuario)
    else:
        workers = Worker.objects.all().order_by('id')

    status_list = Status.objects.all()

    context = {
        'globalsettings': globalsettings,
        'workers': workers,
        'position_list': position_list,
        'establishment_list': establishment_list,
        'shift_list': shift_list,
        'sector_list': sector_list,
        'subSector_list': subSector_list,
        'status_list': status_list,
        'setores_usuario': setores_usuario,
    }
    return render(request, 'adjust_worker.html', context)

def edit_worker(request, id_worker):
    worker = get_object_or_404(Worker, id_worker=id_worker)
    globalsettings = Global_Settings.objects.all().latest('id')
    position_list = Position.objects.all()
    establishment_list = Establishment.objects.all()
    shift_list = Shift.objects.all()
    sector_list = Sector.objects.all()
    subSector_list = Sub_Sector.objects.all()
    user = request.user

    if request.method == 'POST':
        # Receba os dados do POST
        number_w = request.POST.get('number')
        name_w = request.POST.get('name')
        position_name = request.POST.get('position')
        establishment_name = request.POST.get('establishment')
        shift_name = request.POST.get('shift')
        sector_name = request.POST.get('sector')
        subSector_name = request.POST.get('subSector')

        # Atualize os campos do trabalhador
        worker.number_w = number_w
        worker.name_w = name_w

        # Atualize os campos many-to-many do trabalhador
        worker.position_w.set(Position.objects.filter(position_name=position_name))
        worker.establishment_w.set(Establishment.objects.filter(establishment_name=establishment_name))
        worker.shift_w.set(Shift.objects.filter(shift_name=shift_name))
        worker.sector_w.set(Sector.objects.filter(sector_name=sector_name))
        worker.subSector_w.set(Sub_Sector.objects.filter(subSector_name=subSector_name))

        # Salve as alterações
        worker.save()

        # Redirecione para a página de detalhes do trabalhador ou outra página apropriada
        return render(request, 'adjust_worker.html')

    context = {
        'globalsettings': globalsettings,
        'worker': worker,
        'position_list': position_list,
        'establishment_list': establishment_list,
        'shift_list': shift_list,
        'sector_list': sector_list,
        'subSector_list': subSector_list,
    }
    return render(request, 'edit_worker.html', context)






###############################################################################
# SETTINGS

def settings(request):
    globalsettings = Global_Settings.objects.all().latest('id')

    establishment_list = Establishment.objects.all()
    sectors_list = Sector.objects.all()
    subSectors_list = Sub_Sector.objects.all()
    position_list = Position.objects.all()
    shift_list = Shift.objects.all()
    status_list = Status.objects.all()
    theme_list = Theme.objects.all()


    logo_form = ImageUploadForm()
    bg_form = ImageUploadForm_Bg()
    form = UploadFileForm(request.POST, request.FILES)

    if request.method == 'POST':
        establishment_form = EstablishmentForm(request.POST)
        sector_form = SectorForm(request.POST)
        sub_sector_form = SubSectorForm(request.POST)
        position_form = PositionForm(request.POST)
        shift_form = ShiftForm(request.POST)
        status_form = StatusForm(request.POST)

        if establishment_form.is_valid():
            establishment_form.save()
            return redirect('settings')
        if sector_form.is_valid():
            sector_form.save()
            return redirect('settings')
        if sub_sector_form.is_valid():
            sub_sector_form.save()
            return redirect('settings')
        if position_form.is_valid():
            position_form.save()
            return redirect('settings')
        if shift_form.is_valid():
            shift_form.save()
            return redirect('settings')
        if status_form.is_valid():
            status_form.save()
            return redirect('settings')

    else:
        establishment_form = EstablishmentForm()
        sector_form = SectorForm()
        sub_sector_form = SubSectorForm()
        position_form = PositionForm(request.POST)
        shift_form = ShiftForm(request.POST)
        status_form = StatusForm(request.POST)
        
    
    
    context = {
        'establishment_list':establishment_list,
        'sectors_list':sectors_list,
        'subSectors_list':subSectors_list,
        'position_list':position_list,
        'shift_list':shift_list,
        'status_list':status_list,
        'theme_list':theme_list,
        'globalsettings':globalsettings,
        'logo_form':logo_form,
        'bg_form':bg_form,
        'form':form,


        'sector_form': sector_form,
        'establishment_form': establishment_form,
        'sub_sector_form':sub_sector_form,
        'position_form':position_form,
        'shift_form':shift_form,
        'status_form':status_form,

    }
    return render(request, 'settings.html', context)

###############################################################################
# SETTINGS ACTIONS

def change_logo(request):
        if request.method == 'POST':
            logo_form = ImageUploadForm(request.POST, request.FILES)
            if logo_form.is_valid():
                last_global_settings = Global_Settings.objects.latest('id')
                last_global_settings.logo_image = logo_form.cleaned_data['logo_image']
                last_global_settings.save()
                return redirect('settings')
        else:
            logo_form = ImageUploadForm()
        return redirect('settings')

def remove_logo(request):
    last_global_settings  = Global_Settings.objects.latest('id')
    last_global_settings.logo_image = "logos/default.png"
    last_global_settings.save()
    return redirect('settings')

def change_bg(request):
        if request.method == 'POST':
            bg_form = ImageUploadForm_Bg(request.POST, request.FILES)
            if bg_form.is_valid():
                last_global_settings  = Global_Settings.objects.latest('id')
                last_global_settings.bg_image = bg_form.cleaned_data['background_image']
                last_global_settings.save()
                return redirect('settings')
        else:
            bg_form = ImageUploadForm_Bg()
        return redirect('settings')

def remove_bg(request):
    last_global_settings  = Global_Settings.objects.latest('id')
    last_global_settings.bg_image = " "
    last_global_settings.save()
    return redirect('settings')

def change_settings(request):
    if request.method == 'POST':
        selected_theme = request.POST.get('theme')
        institution = request.POST.get('institution')
        global_settings = Global_Settings.objects.all().latest('id')
        theme = Theme.objects.get(theme_name=selected_theme)
        global_settings.theme.set([theme])
        global_settings.institution_name =  institution
        global_settings.save()
    return redirect('settings')

def export_workers_to_excel(request):
    # Busque os objetos Worker do banco de dados
    workers = Worker.objects.all()

    # Crie um novo arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Workers"

    # Adicione cabeçalhos às colunas
    ws.append(["ID", "Número", "Nome", "Posição", "Estabelecimento", "Turno", "Setor", "Subsetor", "Status", "Observação"])

    # Preencha as linhas com os dados dos trabalhadores
    for worker in workers:
        positions = ", ".join([str(pos) for pos in worker.position_w.all()])
        establishments = ", ".join([str(est) for est in worker.establishment_w.all()])
        shifts = ", ".join([str(shift) for shift in worker.shift_w.all()])
        sectors = ", ".join([str(sector) for sector in worker.sector_w.all()])
        sub_sectors = ", ".join([str(sub) for sub in worker.subSector_w.all()])
        statuses = ", ".join([str(status) for status in worker.status_w.all()])

        ws.append([worker.id_worker, worker.number_w, worker.name_w, positions, establishments, shifts, sectors, sub_sectors, statuses, worker.observation_w])

    # Crie uma resposta HTTP com o arquivo Excel
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=workers.xlsx"

    # Salve o arquivo Excel na resposta HTTP
    wb.save(response)

    return response

def import_workers_from_excel(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['excel_file']
            df = pd.read_excel(uploaded_file)
            total_rows = len(df)

            # Inicialize o progresso na sessão do usuário
            request.session['progress'] = 0

            for index, row in df.iterrows():
                number_w = row['Número']
                name_w = row['Nome']

                # Crie ou obtenha objetos Position, Establishment, Shift, etc. com base nos dados do Excel
                position_names = row['Posição'].split(", ")  # Se os dados forem separados por vírgula
                positions = [Position.objects.get_or_create(position_name=name)[0] for name in position_names]

                establishment_names = row['Estabelecimento'].split(", ")
                establishments = [Establishment.objects.get_or_create(establishment_name=name)[0] for name in establishment_names]

                shift_names = row['Turno'].split(", ")
                shifts = [Shift.objects.get_or_create(shift_name=name)[0] for name in shift_names]

                sector_names = row['Setor'].split(", ")
                sectors = [Sector.objects.get_or_create(sector_name=name)[0] for name in sector_names]

                sub_sector_names = row['Subsetor'].split(", ")
                sub_sectors = [Sub_Sector.objects.get_or_create(subSector_name=name)[0] for name in sub_sector_names]

                status_names = row['Status'].split(", ")
                statuses = [Status.objects.get_or_create(status_name=name)[0] for name in status_names]

                observation_w = row['Observação']

                # Crie um objeto Worker e associe os objetos Position, Establishment, etc.
                worker = Worker.objects.create(
                    number_w=number_w,
                    name_w=name_w,
                    observation_w=observation_w,
                )

                worker.position_w.set(positions)
                worker.establishment_w.set(establishments)
                worker.shift_w.set(shifts)
                worker.sector_w.set(sectors)
                worker.subSector_w.set(sub_sectors)
                worker.status_w.set(statuses)

                # Atualize o progresso na sessão do usuário
                request.session['progress'] = (index + 1) / total_rows * 100
                progress = request.session['progress']
                print('Importing worker',worker.name_w, progress)

            # Quando o processo estiver concluído, defina o progresso como 100
            request.session['progress'] = 100

            return redirect('settings')  # Redirecionar para uma página de sucesso
    else:
        form = UploadFileForm()

    return render(request, 'import_workers_form.html', {'form': form})

def remove_all_workers(request):
    if request.method == 'POST':
        workers = Worker.objects.all()
        workers.delete()
    return redirect('settings') 



def get_import_progress(request):
    progress = request.session.get('progress', 0)
    return JsonResponse({'progress': progress})


def delete_selected_establishments(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items_establishment[]') 
        try:
            Establishment.objects.filter(id__in=selected_items).delete()
        except Exception as e:
            print(e)
    return redirect('settings') 

def rename_establishment(request):
    if request.method == 'POST':
        new_establishment_name = request.POST.get('new_establishment_name')
        global_settings = Global_Settings.objects.all().latest('id')
        global_settings.establishment_title = new_establishment_name
        global_settings.save()
    return redirect('settings')


def delete_selected_sector(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items_sector[]')
        try:
            Sector.objects.filter(id__in=selected_items).delete()
        except Exception as e:
            print(e)
    return redirect('settings')

def rename_sector(request):
    if request.method == 'POST':
        new_sector_name = request.POST.get('new_sector_name')
        global_settings = Global_Settings.objects.all().latest('id')
        global_settings.sector_title = new_sector_name
        global_settings.save()
    return redirect('settings')


def delete_selected_sub_sector(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items_sub_sector[]')
        try:
            Sub_Sector.objects.filter(id__in=selected_items).delete()
        except Exception as e:
            print(e)
    return redirect('settings')

def rename_sub_sector(request):
    if request.method == 'POST':
        new_sub_sector_name = request.POST.get('new_sub_sector_name')
        global_settings = Global_Settings.objects.all().latest('id')
        global_settings.subSector_title = new_sub_sector_name
        global_settings.save()
    return redirect('settings')

def delete_selected_position(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items_position[]') 
        try:
            Position.objects.filter(id__in=selected_items).delete()
        except Exception as e:
            print(e)
    return redirect('settings') 

def rename_position(request):
    if request.method == 'POST':
        new_position_name = request.POST.get('new_position_name')
        global_settings = Global_Settings.objects.all().latest('id')
        global_settings.position_title = new_position_name
        global_settings.save()
    return redirect('settings')

def delete_selected_shift(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items_shift[]') 
        try:
            Shift.objects.filter(id__in=selected_items).delete()
        except Exception as e:
            print(e)
    return redirect('settings') 

def rename_shift(request):
    if request.method == 'POST':
        new_shift_name = request.POST.get('new_shift_name')
        global_settings = Global_Settings.objects.all().latest('id')
        global_settings.shift_title = new_shift_name
        global_settings.save()
    return redirect('settings')

def delete_selected_status(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items_status[]') 
        try:
            Status.objects.filter(id__in=selected_items).delete()
        except Exception as e:
            print(e)
    return redirect('settings') 

def rename_status(request):
    if request.method == 'POST':
        new_status_name = request.POST.get('new_status_name')
        global_settings = Global_Settings.objects.all().latest('id')
        global_settings.status_title = new_status_name
        global_settings.save()
    return redirect('settings')

def change_status_color(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('status_color_'):
                status_id = key.replace('status_color_', '')
                status = Status.objects.get(pk=status_id)
                status.status_color = value
                status.save()

    return redirect('settings')

###############################################################################
# AUTHENTICATION

def login(request):
    globalsettings = Global_Settings.objects.all().latest('id')


    context = {
        'globalsettings':globalsettings,
    }
    return render(request, 'login.html', context)

###############################################################################
# VIEW TEMPLATE

def view(request):
    globalsettings = Global_Settings.objects.all().latest('id')


    context = {
        'globalsettings':globalsettings,
    }
    return render(request, 'dashboard', context)
