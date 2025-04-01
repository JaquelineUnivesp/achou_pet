import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import AdoptionPetForm, BreedingPetForm, LostPetForm
from .locationiq import LocationIQ
from .models import BreedingPet, LostPet, PetAdoption

# Configuração do logger
logger = logging.getLogger(__name__)

# -----------------------------------
# Funções Gerais
# -----------------------------------

@login_required
def success_view(request):
    """Página de sucesso após ações concluídas."""
    return render(request, 'pet_registration/success.html')

def autocomplete(request):
    """Autocompletar localização via LocationIQ."""
    query = request.GET.get('q', '')
    if query:
        locationiq = LocationIQ()
        results = locationiq.autocomplete(query)
        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'No query provided'}, status=400)

def reverse_geocode(request):
    """Reverter geocodificação via LocationIQ."""
    lat = request.GET.get('lat', '')
    lon = request.GET.get('lon', '')
    if lat and lon:
        locationiq = LocationIQ()
        results = locationiq.reverse_geocode(lat, lon)
        return JsonResponse(results, safe=False)
    return JsonResponse({'error': 'No latitude or longitude provided'}, status=400)

# -----------------------------------
# Listagem de Pets do Usuário
# -----------------------------------

@login_required
def user_pets_list(request):
    """Lista todos os pets cadastrados pelo usuário (perdidos, adoção e reprodução)."""
    user = request.user
    logger.info(f"Usuário logado: {user.email}")

    try:
        lost_pets = LostPet.objects.filter(user=user).order_by('-created_at')
        logger.info(f"Total de pets perdidos encontrados: {lost_pets.count()}")

        adoption_pets = PetAdoption.objects.filter(owner=user).order_by('-created_at')
        logger.info(f"Total de pets para adoção encontrados: {adoption_pets.count()}")

        breeding_pets = BreedingPet.objects.filter(owner=user).order_by('-created_at')
        logger.info(f"Total de pets para reprodução encontrados: {breeding_pets.count()}")

        context = {
            'lost_pets': lost_pets,
            'adoption_pets': adoption_pets,
            'breeding_pets': breeding_pets,
        }
    except Exception as e:
        logger.error(f"Erro ao buscar pets: {e}")
        context = {'lost_pets': [], 'adoption_pets': [], 'breeding_pets': []}

    return render(request, 'pet_registration/user_pets_list.html', context)

# -----------------------------------
# Pets Perdidos (LostPet)
# -----------------------------------

@login_required
def register_lost_pet(request):
    """Cadastra um pet perdido."""
    if request.method == 'POST':
        print("Dados recebidos no POST:", request.POST)  # Depuração
        form = LostPetForm(request.POST, request.FILES)
        if form.is_valid():
            lost_pet = form.save(commit=False)
            lost_pet.user = request.user
            lost_pet.save()
            print("Pet salvo com sucesso:", lost_pet.id)  # Depuração
            return redirect('pet_registration:success')
        else:
            print("Erros no formulário:", form.errors)  # Depuração
    else:
        form = LostPetForm()
    return render(request, 'pet_registration/register_lost_pet.html', {'form': form})

@login_required
def pet_detail(request, pet_id):
    """Exibe detalhes de um pet perdido."""
    pet = get_object_or_404(LostPet, id=pet_id, user=request.user)
    print(f"Foto 1: {pet.photo1.url if pet.photo1 else 'Nenhuma foto'}")
    return render(request, 'pet_registration/pet_detail.html', {'pet': pet})

@login_required
def edit_pet(request, pet_id):
    """Edita um pet perdido cadastrado."""
    pet = get_object_or_404(LostPet, id=pet_id, user=request.user)
    if request.method == 'POST':
        form = LostPetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet atualizado com sucesso!")
            return redirect('pet_registration:user_pets_list')
    else:
        form = LostPetForm(instance=pet)
    return render(request, 'pet_registration/edit_pet.html', {'form': form, 'pet': pet})

@login_required
def delete_pet(request, pet_id):
    """Deleta um pet perdido."""
    pet = get_object_or_404(LostPet, id=pet_id, user=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet deletado com sucesso!")
        return redirect('pet_registration:user_pets_list')
    return render(request, 'pet_registration/delete_pet.html', {'pet': pet})

# -----------------------------------
# Pets para Adoção (PetAdoption)
# -----------------------------------

@login_required
def register_adoption_pet(request):
    """Cadastra um pet para adoção."""
    if request.method == 'POST':
        form = AdoptionPetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, 'Pet cadastrado com sucesso para adoção!')
            return redirect('pet_registration:success')
        else:
            messages.error(request, 'Erro ao cadastrar o pet. Verifique os dados.')
            print("Erros no formulário:", form.errors)
    else:
        form = AdoptionPetForm()
    return render(request, 'pet_registration/register_adoption_pet.html', {'form': form})

@login_required
def adoption_pet_detail(request, pet_id):
    """Exibe detalhes de um pet para adoção."""
    pet = get_object_or_404(PetAdoption, id=pet_id, owner=request.user)
    return render(request, 'pet_registration/adoption_pet_detail.html', {'pet': pet})

@login_required
def edit_adoption_pet(request, pet_id):
    """Edita um pet para adoção."""
    pet = get_object_or_404(PetAdoption, id=pet_id, owner=request.user)
    if request.method == 'POST':
        form = AdoptionPetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet de adoção atualizado com sucesso!")
            return redirect('pet_registration:user_pets_list')
    else:
        form = AdoptionPetForm(instance=pet)
    return render(request, 'pet_registration/edit_adoption_pet.html', {'form': form, 'pet': pet})

@login_required
def delete_adoption_pet(request, pet_id):
    """Deleta um pet para adoção."""
    pet = get_object_or_404(PetAdoption, id=pet_id, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet de adoção deletado com sucesso!")
        return redirect('pet_registration:user_pets_list')
    return render(request, 'pet_registration/delete_adoption_pet.html', {'pet': pet})

# -----------------------------------
# Pets para Reprodução (BreedingPet)
# -----------------------------------

@login_required
def register_breeding_pet(request):
    """Cadastra um pet para reprodução."""
    if request.method == 'POST':
        form = BreedingPetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, 'Pet cadastrado com sucesso para reprodução!')
            return redirect('pet_registration:success')
        else:
            messages.error(request, 'Erro ao cadastrar o pet. Verifique os dados.')
    else:
        form = BreedingPetForm()
    return render(request, 'pet_registration/register_breeding_pet.html', {'form': form})

@login_required
def breeding_pet_detail(request, pet_id):
    """Exibe detalhes de um pet para reprodução."""
    pet = get_object_or_404(BreedingPet, id=pet_id, owner=request.user)
    return render(request, 'pet_registration/breeding_pet_detail.html', {'pet': pet})

@login_required
def edit_breeding_pet(request, pet_id):
    """Edita um pet para reprodução."""
    pet = get_object_or_404(BreedingPet, id=pet_id, owner=request.user)
    if request.method == 'POST':
        form = BreedingPetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, "Pet de reprodução atualizado com sucesso!")
            return redirect('pet_registration:user_pets_list')
    else:
        form = BreedingPetForm(instance=pet)
    return render(request, 'pet_registration/edit_breeding_pet.html', {'form': form, 'pet': pet})

@login_required
def delete_breeding_pet(request, pet_id):
    """Deleta um pet para reprodução."""
    pet = get_object_or_404(BreedingPet, id=pet_id, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet de reprodução deletado com sucesso!")
        return redirect('pet_registration:user_pets_list')
    return render(request, 'pet_registration/delete_breeding_pet.html', {'pet': pet})

# -----------------------------------
# Busca de Pets para Adoção
# -----------------------------------

from django.shortcuts import render
from django.db.models import Q
from apps.pet_registration.models import PetAdoption
import logging

logger = logging.getLogger(__name__)

def search_adoption_pets(request):
    # Capturar todos os parâmetros do GET
    query = request.GET.get('query', '').strip()
    age = request.GET.get('age', '').strip()
    is_neutered = request.GET.get('is_neutered', '').strip()
    is_vaccinated = request.GET.get('vaccinated', '').strip()
    sociable_animals = request.GET.get('sociable_animals', '').strip()
    sociable_children = request.GET.get('sociable_children', '').strip()
    sociable_strangers = request.GET.get('sociable_strangers', '').strip()
    sex = request.GET.get('sex', '').strip()
    size_by_age = request.GET.get('size_by_age', '').strip()
    location = request.GET.get('location', '').strip()
    distance = request.GET.get('distance', '').strip()

    # Log para depuração
    logger.info(f"Parâmetros recebidos: {request.GET}")

    # Filtrar inicialmente por status 'adoption'
    adoption_pets = PetAdoption.objects.filter(status='adoption')
    logger.info(f"Pets iniciais com status 'adoption': {adoption_pets.count()}")

    # Filtro genérico (query)
    if query:
        adoption_pets = adoption_pets.filter(
            Q(pet_name__icontains=query) |
            Q(observations__icontains=query) |
            Q(behavior__icontains=query) |
            Q(health_issues__icontains=query) |
            Q(approximate_age__icontains=query)
        )
        logger.info(f"Filtro query ({query}): {adoption_pets.count()} pets")

    # Filtro de idade aproximada
    if age:
        adoption_pets = adoption_pets.filter(approximate_age__icontains=age)
        logger.info(f"Filtro idade ({age}): {adoption_pets.count()} pets")

    # Filtro de castração
    if is_neutered:
        adoption_pets = adoption_pets.filter(is_neutered=is_neutered)
        logger.info(f"Filtro castrado ({is_neutered}): {adoption_pets.count()} pets")

    # Filtro de vacinação
    if is_vaccinated:
        adoption_pets = adoption_pets.filter(is_vaccinated=is_vaccinated)
        logger.info(f"Filtro vacinado ({is_vaccinated}): {adoption_pets.count()} pets")

    # Filtro de sociabilidade com animais
    if sociable_animals:
        adoption_pets = adoption_pets.filter(sociable_with_animals=sociable_animals)
        logger.info(f"Filtro sociável com animais ({sociable_animals}): {adoption_pets.count()} pets")

    # Filtro de sociabilidade com crianças
    if sociable_children:
        adoption_pets = adoption_pets.filter(sociable_with_children=sociable_children)
        logger.info(f"Filtro sociável com crianças ({sociable_children}): {adoption_pets.count()} pets")

    # Filtro de sociabilidade com estranhos
    if sociable_strangers:
        adoption_pets = adoption_pets.filter(sociable_with_strangers=sociable_strangers)
        logger.info(f"Filtro sociável com estranhos ({sociable_strangers}): {adoption_pets.count()} pets")

    # Filtro de sexo (novo)
    if sex:
        valid_sex = ['macho', 'fêmea']
        if sex in valid_sex:
            adoption_pets = adoption_pets.filter(sex__iexact=sex)  # Case-insensitive
            logger.info(f"Filtro sexo ({sex}): {adoption_pets.count()} pets")
        else:
            logger.warning(f"Sexo inválido: {sex}. Esperado: {valid_sex}")

    # Filtro de tamanho por idade (novo)
    if size_by_age:
        valid_sizes = ['filhote', 'adulto', 'idoso']
        if size_by_age in valid_sizes:
            adoption_pets = adoption_pets.filter(size_by_age__iexact=size_by_age)  # Case-insensitive
            logger.info(f"Filtro tamanho por idade ({size_by_age}): {adoption_pets.count()} pets")
        else:
            logger.warning(f"Tamanho inválido: {size_by_age}. Esperado: {valid_sizes}")

    # Filtro de localização e distância (novo)
    if location:
        if distance:
            try:
                distance_km = float(distance)
                # Filtro básico por texto se não houver suporte GIS
                adoption_pets = adoption_pets.filter(location__icontains=location)
                logger.info(f"Filtro localização com distância ({location}, {distance_km} km): {adoption_pets.count()} pets")
                # Se PostGIS estiver configurado (opcional), adicione lógica de distância aqui
            except ValueError:
                logger.error(f"Distância inválida: {distance}")
                adoption_pets = adoption_pets.filter(location__icontains=location)
                logger.info(f"Filtro localização (distância inválida): {adoption_pets.count()} pets")
        else:
            adoption_pets = adoption_pets.filter(location__icontains=location)
            logger.info(f"Filtro localização ({location}): {adoption_pets.count()} pets")

    logger.info(f"Total de pets após todos os filtros: {adoption_pets.count()}")

    # Contexto para o template
    context = {
        'adoption_pets': adoption_pets,
        'query': query,
        'age': age,
        'is_neutered': is_neutered,
        'vaccinated': is_vaccinated,
        'sociable_animals': sociable_animals,
        'sociable_children': sociable_children,
        'sociable_strangers': sociable_strangers,
        'sex': sex,
        'size_by_age': size_by_age,
        'location': location,
        'distance': distance,
        'months': list(range(0, 12)),  # Para o filtro de idade no template
        'years': list(range(1, 31)),
    }
    return render(request, 'search/search_adoption.html', context)