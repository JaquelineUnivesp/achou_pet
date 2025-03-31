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

def search_adoption_pets(request):
    """Página de busca de pets para adoção com filtros e busca genérica."""
    # Pegar os parâmetros da requisição GET
    query = request.GET.get('query', '')  # Novo campo de busca genérica
    age = request.GET.get('age', '')
    is_neutered = request.GET.get('is_neutered', '')
    is_vaccinated = request.GET.get('vaccinated', '')
    sociable_animals = request.GET.get('sociable_animals', '')
    sociable_children = request.GET.get('sociable_children', '')
    sociable_strangers = request.GET.get('sociable_strangers', '')

    # Filtrar os pets de adoção
    adoption_pets = PetAdoption.objects.filter(status='adoption')

    # Filtro de busca genérica
    if query:
        adoption_pets = adoption_pets.filter(
            Q(pet_name__icontains=query) |
            Q(observations__icontains=query) |
            Q(behavior__icontains=query) |
            Q(health_issues__icontains=query) |
            Q(approximate_age__icontains=query)
        )

    # Aplicar filtros específicos
    if age:
        adoption_pets = adoption_pets.filter(approximate_age__icontains=age)
    if is_neutered:
        adoption_pets = adoption_pets.filter(is_neutered=is_neutered)
    if is_vaccinated:
        adoption_pets = adoption_pets.filter(is_vaccinated=is_vaccinated)
    if sociable_animals:
        adoption_pets = adoption_pets.filter(sociable_with_animals=sociable_animals)
    if sociable_children:
        adoption_pets = adoption_pets.filter(sociable_with_children=sociable_children)
    if sociable_strangers:
        adoption_pets = adoption_pets.filter(sociable_with_strangers=sociable_strangers)

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
    }

    return render(request, 'search/search_adoption.html', context)