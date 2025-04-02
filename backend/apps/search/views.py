from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.serializers.json import DjangoJSONEncoder
import requests
from apps.pet_registration.models import PetAdoption, BreedingPet, LostPet
from django.contrib.gis.geos import Point
from geopy.geocoders import Nominatim
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

# Função auxiliar para converter localização em ponto geográfico
def location_to_point(location_str):
    geolocator = Nominatim(user_agent="achou_pet")
    try:
        location = geolocator.geocode(location_str)
        if location:
            logger.info(f"Geocodificação OK: {location_str} -> ({location.latitude}, {location.longitude})")
            return Point(location.longitude, location.latitude)
        logger.warning(f"Geocodificação falhou para: {location_str}")
        return None
    except Exception as e:
        logger.error(f"Erro ao geocodificar {location_str}: {str(e)}")
        return None

# View genérica para busca de todos os tipos de pets (sem alterações)
def search_pets(request):
    filter_type = request.GET.get('type', 'all')
    search_query = request.GET.get('q', '').strip()

    lost_pets = LostPet.objects.none()
    adoption_pets = PetAdoption.objects.none()
    breeding_pets = BreedingPet.objects.none()

    if filter_type in ['lost', 'all']:
        lost_pets = LostPet.objects.all()
        if search_query:
            lost_pets = lost_pets.filter(
                Q(name__icontains=search_query) |
                Q(breed__icontains=search_query) |
                Q(color__icontains=search_query) |
                Q(lost_location__icontains=search_query)
            )

    if filter_type in ['adoption', 'all']:
        adoption_pets = PetAdoption.objects.all()
        if search_query:
            adoption_pets = adoption_pets.filter(
                Q(pet_name__icontains=search_query) |
                Q(observations__icontains=search_query) |
                Q(breed__icontains=search_query) |
                Q(color__icontains=search_query)
            )

    if filter_type in ['breeding', 'all']:
        breeding_pets = BreedingPet.objects.all()
        if search_query:
            breeding_pets = breeding_pets.filter(
                Q(pet_name__icontains=search_query) |
                Q(breeding_reason__icontains=search_query) |
                Q(breed__icontains=search_query) |  # Adicionado
                Q(color__icontains=search_query)    # Adicionado
            )

    context = {
        'lost_pets': lost_pets.order_by('-created_at'),
        'adoption_pets': adoption_pets.order_by('-created_at'),
        'breeding_pets': breeding_pets.order_by('-created_at'),
        'filter_type': filter_type,
        'search_query': search_query,
    }
    return render(request, 'search/search_pets.html', context)

# View para busca de pets perdidos/encontrados (sem alterações)
def search_lost_pets(request):
    status = request.GET.get('status', '')
    species = request.GET.get('species', '')
    size = request.GET.get('size', '')
    breed = request.GET.get('breed', '').strip()
    color = request.GET.get('color', '').strip()
    sex = request.GET.get('sex', '')
    search_query = request.GET.get('q', '').strip()

    lost_pets = LostPet.objects.all()

    if search_query:
        lost_pets = lost_pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(color__icontains=search_query) |
            Q(lost_location__icontains=search_query)
        )

    if status:
        lost_pets = lost_pets.filter(status=status)
    if species:
        lost_pets = lost_pets.filter(species=species)
    if size:
        lost_pets = lost_pets.filter(size=size)
    if breed:
        lost_pets = lost_pets.filter(breed__icontains=breed)
    if color:
        lost_pets = lost_pets.filter(color__icontains=color)
    if sex:
        lost_pets = lost_pets.filter(sex=sex)

    context = {
        'lost_pets': lost_pets.order_by('-created_at'),
        'status': status,
        'species': species,
        'size': size,
        'breed': breed,
        'color': color,
        'sex': sex,
        'search_query': search_query,
    }
    return render(request, 'search/search_lost.html', context)

# View para busca de pets para adoção (sem alterações)
def search_adoption_pets(request):
    search_query = request.GET.get('q', '').strip()
    age = request.GET.get('age', '')
    is_neutered = request.GET.get('is_neutered', '')
    vaccinated = request.GET.get('vaccinated', '')
    sociable_animals = request.GET.get('sociable_animals', '')
    sociable_children = request.GET.get('sociable_children', '')
    sociable_strangers = request.GET.get('sociable_strangers', '')
    sex = request.GET.get('sex', '')
    size_by_age = request.GET.get('size_by_age', '')
    location = request.GET.get('location', '')
    distance = request.GET.get('distance', '')

    logger.info(f"Parâmetros recebidos: {request.GET}")
    adoption_pets = PetAdoption.objects.filter(status='adoption')
    logger.info(f"Pets iniciais com status 'adoption': {adoption_pets.count()}")

    if search_query:
        adoption_pets = adoption_pets.filter(
            Q(pet_name__icontains=search_query) |
            Q(observations__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(color__icontains=search_query)
        )
        logger.info(f"Filtro genérico: {adoption_pets.count()} pets")

    if age:
        adoption_pets = adoption_pets.filter(approximate_age__iexact=age)
        logger.info(f"Filtro idade ({age}): {adoption_pets.count()} pets")

    if is_neutered:
        neutered_value = 'yes' if is_neutered.lower() in ['yes', 'sim', 'true', '1'] else 'no'
        adoption_pets = adoption_pets.filter(is_neutered=neutered_value)
        logger.info(f"Filtro castrado ({neutered_value}): {adoption_pets.count()} pets")

    if vaccinated:
        vaccinated_value = 'yes' if vaccinated.lower() in ['yes', 'sim', 'true', '1'] else 'no'
        adoption_pets = adoption_pets.filter(is_vaccinated=vaccinated_value)
        logger.info(f"Filtro vacinado ({vaccinated_value}): {adoption_pets.count()} pets")

    if sociable_animals:
        adoption_pets = adoption_pets.filter(sociable_with_animals=sociable_animals)
        logger.info(f"Filtro animais ({sociable_animals}): {adoption_pets.count()} pets")

    if sociable_children:
        adoption_pets = adoption_pets.filter(sociable_with_children=sociable_children)
        logger.info(f"Filtro crianças ({sociable_children}): {adoption_pets.count()} pets")

    if sociable_strangers:
        adoption_pets = adoption_pets.filter(sociable_with_strangers=sociable_strangers)
        logger.info(f"Filtro estranhos ({sociable_strangers}): {adoption_pets.count()} pets")

    if sex:
        valid_sex = ['macho', 'fêmea']
        if sex in valid_sex:
            adoption_pets = adoption_pets.filter(sex__iexact=sex)
            logger.info(f"Filtro sexo ({sex}): {adoption_pets.count()} pets")
        else:
            logger.warning(f"Sexo inválido: {sex}. Esperado: {valid_sex}")

    if size_by_age:
        valid_sizes = ['filhote', 'adulto', 'idoso']
        if size_by_age in valid_sizes:
            adoption_pets = adoption_pets.filter(size_by_age__iexact=size_by_age)
            logger.info(f"Filtro tamanho ({size_by_age}): {adoption_pets.count()} pets")
        else:
            logger.warning(f"Tamanho inválido: {size_by_age}. Esperado: {valid_sizes}")

    if location:
        if distance:
            try:
                distance_km = float(distance)
                user_location = location_to_point(location)
                if user_location:
                    adoption_pets = adoption_pets.filter(
                        latitude__isnull=False,
                        longitude__isnull=False
                    )
                    adoption_pets = adoption_pets.filter(location__icontains=location)
                    logger.info(f"Filtro texto (sem PostGIS): {adoption_pets.count()} pets")
                else:
                    adoption_pets = adoption_pets.filter(location__icontains=location)
                    logger.info(f"Filtro texto (geocode falhou): {adoption_pets.count()} pets")
            except ValueError:
                logger.error(f"Distância inválida: {distance}")
                adoption_pets = adoption_pets.filter(location__icontains=location)
                logger.info(f"Filtro texto (distância inválida): {adoption_pets.count()} pets")
        else:
            adoption_pets = adoption_pets.filter(location__icontains=location)
            logger.info(f"Filtro texto: {adoption_pets.count()} pets")

    logger.info(f"Total de pets após todos os filtros: {adoption_pets.count()}")

    months = list(range(0, 12))
    years = list(range(1, 31))

    context = {
        'adoption_pets': adoption_pets,
        'search_query': search_query,
        'age': age,
        'is_neutered': is_neutered,
        'vaccinated': vaccinated,
        'sociable_animals': sociable_animals,
        'sociable_children': sociable_children,
        'sociable_strangers': sociable_strangers,
        'sex': sex,
        'size_by_age': size_by_age,
        'location': location,
        'distance': distance,
        'months': months,
        'years': years,
    }
    return render(request, 'search/search_adoption.html', context)

# View ajustada para busca de pets para reprodução
def search_breeding_pets(request):
    search_query = request.GET.get('q', '').strip()
    species = request.GET.get('species', '').strip()
    sex = request.GET.get('sex', '').strip()
    size_by_age = request.GET.get('size_by_age', '').strip()
    approximate_age = request.GET.get('approximate_age', '').strip()
    is_neutered = request.GET.get('is_neutered', '').strip()
    is_vaccinated = request.GET.get('is_vaccinated', '').strip()
    has_pedigree = request.GET.get('has_pedigree', '').strip()
    has_bred_before = request.GET.get('has_bred_before', '').strip()
    cost_sharing = request.GET.get('cost_sharing', '').strip()
    location = request.GET.get('location', '').strip()
    distance = request.GET.get('distance', '').strip()
    breed = request.GET.get('breed', '').strip()  # Adicionado
    color = request.GET.get('color', '').strip()  # Adicionado
    phone_for_notifications = request.GET.get('phone_for_notifications', '').strip()  # Adicionado

    logger.info(f"Parâmetros recebidos: {request.GET}")
    breeding_pets = BreedingPet.objects.all()
    logger.info(f"Pets iniciais para cruzamento: {breeding_pets.count()}")

    if search_query:
        breeding_pets = breeding_pets.filter(
            Q(pet_name__icontains=search_query) |
            Q(breeding_reason__icontains=search_query) |
            Q(breed__icontains=search_query) |  # Adicionado
            Q(color__icontains=search_query)    # Adicionado
        )
        logger.info(f"Filtro genérico ({search_query}): {breeding_pets.count()} pets")

    if species:
        valid_species = ['dog', 'cat']
        if species in valid_species:
            breeding_pets = breeding_pets.filter(species__iexact=species)
            logger.info(f"Filtro espécie ({species}): {breeding_pets.count()} pets")
        else:
            logger.warning(f"Espécie inválida: {species}. Esperado: {valid_species}")

    if sex:
        valid_sex = ['macho', 'fêmea']
        if sex in valid_sex:
            breeding_pets = breeding_pets.filter(sex__iexact=sex)
            logger.info(f"Filtro sexo ({sex}): {breeding_pets.count()} pets")
        else:
            logger.warning(f"Sexo inválido: {sex}. Esperado: {valid_sex}")

    if size_by_age:
        valid_sizes = ['filhote', 'adulto', 'idoso']
        if size_by_age in valid_sizes:
            breeding_pets = breeding_pets.filter(size_by_age__iexact=size_by_age)
            logger.info(f"Filtro tamanho ({size_by_age}): {breeding_pets.count()} pets")
        else:
            logger.warning(f"Tamanho inválido: {size_by_age}. Esperado: {valid_sizes}")

    if approximate_age:
        breeding_pets = breeding_pets.filter(approximate_age__icontains=approximate_age)
        logger.info(f"Filtro idade ({approximate_age}): {breeding_pets.count()} pets")

    if is_neutered:
        neutered_value = 'yes' if is_neutered.lower() in ['yes', 'sim', 'true', '1'] else 'no'
        breeding_pets = breeding_pets.filter(is_neutered=neutered_value)
        logger.info(f"Filtro castrado ({neutered_value}): {breeding_pets.count()} pets")

    if is_vaccinated:
        vaccinated_value = 'yes' if is_vaccinated.lower() in ['yes', 'sim', 'true', '1'] else 'no'
        breeding_pets = breeding_pets.filter(is_vaccinated=vaccinated_value)
        logger.info(f"Filtro vacinado ({vaccinated_value}): {breeding_pets.count()} pets")

    if has_pedigree:
        pedigree_value = 'yes' if has_pedigree.lower() in ['yes', 'sim', 'true', '1'] else 'no'
        breeding_pets = breeding_pets.filter(has_pedigree=pedigree_value)
        logger.info(f"Filtro pedigree ({pedigree_value}): {breeding_pets.count()} pets")

    if has_bred_before:
        bred_value = 'yes' if has_bred_before.lower() in ['yes', 'sim', 'true', '1'] else 'no'
        breeding_pets = breeding_pets.filter(has_bred_before=bred_value)
        logger.info(f"Filtro já cruzou ({bred_value}): {breeding_pets.count()} pets")

    if cost_sharing:
        breeding_pets = breeding_pets.filter(cost_sharing__icontains=cost_sharing)
        logger.info(f"Filtro divisão de custos ({cost_sharing}): {breeding_pets.count()} pets")

    if breed:
        breeding_pets = breeding_pets.filter(breed__icontains=breed)
        logger.info(f"Filtro raça ({breed}): {breeding_pets.count()} pets")

    if color:
        breeding_pets = breeding_pets.filter(color__icontains=color)
        logger.info(f"Filtro cor ({color}): {breeding_pets.count()} pets")

    if phone_for_notifications:
        breeding_pets = breeding_pets.filter(phone_for_notifications__icontains=phone_for_notifications)
        logger.info(f"Filtro telefone ({phone_for_notifications}): {breeding_pets.count()} pets")

    if location:
        if distance:
            try:
                distance_km = float(distance)
                user_location = location_to_point(location)
                if user_location:
                    breeding_pets = breeding_pets.filter(
                        latitude__isnull=False,
                        longitude__isnull=False
                    )
                    breeding_pets = breeding_pets.filter(location__icontains=location)
                    logger.info(f"Filtro texto (sem PostGIS): {breeding_pets.count()} pets")
                else:
                    breeding_pets = breeding_pets.filter(location__icontains=location)
                    logger.info(f"Filtro texto (geocode falhou): {breeding_pets.count()} pets")
            except ValueError:
                logger.error(f"Distância inválida: {distance}")
                breeding_pets = breeding_pets.filter(location__icontains=location)
                logger.info(f"Filtro texto (distância inválida): {breeding_pets.count()} pets")
        else:
            breeding_pets = breeding_pets.filter(location__icontains=location)
            logger.info(f"Filtro texto: {breeding_pets.count()} pets")

    logger.info(f"Total de pets após todos os filtros: {breeding_pets.count()}")

    context = {
        'breeding_pets': breeding_pets.order_by('-created_at'),
        'search_query': search_query,
        'species': species,
        'sex': sex,
        'size_by_age': size_by_age,
        'approximate_age': approximate_age,
        'is_neutered': is_neutered,
        'is_vaccinated': is_vaccinated,
        'has_pedigree': has_pedigree,
        'has_bred_before': has_bred_before,
        'cost_sharing': cost_sharing,
        'location': location,
        'distance': distance,
        'breed': breed,  # Adicionado
        'color': color,  # Adicionado
        'phone_for_notifications': phone_for_notifications,  # Adicionado
    }
    return render(request, 'search/search_breeding.html', context)

# API consolidada ajustada
@require_GET
def api_pets(request):
    try:
        source = request.GET.get('source', 'all')
        search_query = request.GET.get('q', '').strip()
        status = request.GET.get('status', '')
        species = request.GET.get('species', '')
        size = request.GET.get('size', '')
        breed = request.GET.get('breed', '').strip()
        color = request.GET.get('color', '').strip()
        sex = request.GET.get('sex', '')
        size_by_age = request.GET.get('size_by_age', '')  # Adicionado para BreedingPet

        pet_data = []

        if source in ['lost', 'all']:
            lost_pets = LostPet.objects.all()
            if search_query:
                lost_pets = lost_pets.filter(
                    Q(name__icontains=search_query) |
                    Q(breed__icontains=search_query) |
                    Q(color__icontains=search_query) |
                    Q(lost_location__icontains=search_query)
                )
            if status:
                lost_pets = lost_pets.filter(status=status)
            if species:
                lost_pets = lost_pets.filter(species=species)
            if size:
                lost_pets = lost_pets.filter(size=size)
            if breed:
                lost_pets = lost_pets.filter(breed__icontains=breed)
            if color:
                lost_pets = lost_pets.filter(color__icontains=color)
            if sex:
                lost_pets = lost_pets.filter(sex=sex)

            for pet in lost_pets:
                logger.info(f"LostPet {pet.name}: Sexo={pet.sex}")
                pet_data.append({
                    'id': str(pet.id),
                    'nome': pet.name if pet.name else "Sem nome",
                    'tipo': pet.status,
                    'especie': pet.get_species_display() if pet.species else "Não especificada",
                    'sexo': pet.sex if pet.sex else "Não especificado",
                    'address': pet.lost_location if pet.lost_location else "Local não informado",
                    'data_hora': pet.lost_date.isoformat() if pet.lost_date else pet.created_at.isoformat(),
                    'latitude': float(pet.latitude) if pet.latitude is not None else None,
                    'longitude': float(pet.longitude) if pet.longitude is not None else None,
                    'imagem1': pet.photo1.url if pet.photo1 else None,
                })

        if source in ['adoption', 'all']:
            adoption_pets = PetAdoption.objects.all()
            if search_query:
                adoption_pets = adoption_pets.filter(
                    Q(pet_name__icontains=search_query) |
                    Q(observations__icontains=search_query) |
                    Q(breed__icontains=search_query) |
                    Q(color__icontains=search_query)
                )
            if species:
                adoption_pets = adoption_pets.filter(species=species)
            if breed:
                adoption_pets = adoption_pets.filter(breed__icontains=breed)
            if color:
                adoption_pets = adoption_pets.filter(color__icontains=color)
            if sex:
                valid_sex_values = ['macho', 'fêmea']
                if sex in valid_sex_values:
                    adoption_pets = adoption_pets.filter(sex__iexact=sex)
                    logger.info(f"API: Após filtro de sexo ({sex}): {adoption_pets.count()} pets")
                else:
                    logger.warning(f"API: Valor inválido para sexo: {sex}")

            for pet in adoption_pets:
                logger.info(f"AdoptionPet {pet.pet_name}: Sexo={pet.sex}")
                pet_data.append({
                    'id': str(pet.id),
                    'nome': pet.pet_name if pet.pet_name else "Sem nome",
                    'tipo': 'adoption',
                    'especie': pet.get_species_display() if pet.species else "Não especificada",
                    'sexo': pet.sex if pet.sex else "Não especificado",
                    'tamanho': pet.get_size_by_age_display() if pet.size_by_age else "Não especificado",
                    'address': pet.location if pet.location else "Local não informado",
                    'data_hora': pet.created_at.isoformat(),
                    'latitude': float(pet.latitude) if pet.latitude is not None else None,
                    'longitude': float(pet.longitude) if pet.longitude is not None else None,
                    'imagem1': pet.photo_1.url if pet.photo_1 else None,
                })

        if source in ['breeding', 'all']:
            breeding_pets = BreedingPet.objects.all()
            if search_query:
                breeding_pets = breeding_pets.filter(
                    Q(pet_name__icontains=search_query) |
                    Q(breeding_reason__icontains=search_query) |
                    Q(breed__icontains=search_query) |  # Adicionado
                    Q(color__icontains=search_query)    # Adicionado
                )
            if species:
                valid_species = ['dog', 'cat']
                if species in valid_species:
                    breeding_pets = breeding_pets.filter(species__iexact=species)
                    logger.info(f"API: Após filtro de espécie ({species}): {breeding_pets.count()} pets")
                else:
                    logger.warning(f"API: Espécie inválida: {species}")
            if sex:
                valid_sex = ['macho', 'fêmea']
                if sex in valid_sex:
                    breeding_pets = breeding_pets.filter(sex__iexact=sex)
                    logger.info(f"API: Após filtro de sexo ({sex}): {breeding_pets.count()} pets")
                else:
                    logger.warning(f"API: Sexo inválido: {sex}")
            if size_by_age:
                valid_sizes = ['filhote', 'adulto', 'idoso']
                if size_by_age in valid_sizes:
                    breeding_pets = breeding_pets.filter(size_by_age__iexact=size_by_age)
                    logger.info(f"API: Após filtro de tamanho ({size_by_age}): {breeding_pets.count()} pets")
                else:
                    logger.warning(f"API: Tamanho inválido: {size_by_age}")
            if breed:
                breeding_pets = breeding_pets.filter(breed__icontains=breed)
                logger.info(f"API: Após filtro de raça ({breed}): {breeding_pets.count()} pets")
            if color:
                breeding_pets = breeding_pets.filter(color__icontains=color)
                logger.info(f"API: Após filtro de cor ({color}): {breeding_pets.count()} pets")

            for pet in breeding_pets:
                logger.info(f"BreedingPet {pet.pet_name}: Sexo={pet.sex}")
                pet_data.append({
                    'id': str(pet.id),
                    'nome': pet.pet_name if pet.pet_name else "Sem nome",
                    'tipo': 'breeding',
                    'especie': pet.get_species_display() if pet.species else "Não especificada",
                    'sexo': pet.sex if pet.sex else "Não especificado",
                    'tamanho': pet.get_size_by_age_display() if pet.size_by_age else "Não especificado",
                    'breed': pet.breed if pet.breed else "Não especificada",  # Adicionado
                    'color': pet.color if pet.color else "Não especificada",  # Adicionado
                    'phone_for_notifications': pet.phone_for_notifications if pet.phone_for_notifications else "Não informado",  # Adicionado
                    'address': pet.location if pet.location else "Local não informado",
                    'data_hora': pet.created_at.isoformat(),
                    'latitude': float(pet.latitude) if pet.latitude is not None else None,
                    'longitude': float(pet.longitude) if pet.longitude is not None else None,
                    'imagem1': pet.photo_1.url if pet.photo_1 else None,
                })

        logger.info(f"API retornou {len(pet_data)} pets")
        return JsonResponse(pet_data, safe=False, encoder=DjangoJSONEncoder)

    except Exception as e:
        logger.error(f"Erro ao carregar pets na API: {str(e)}")
        return JsonResponse({
            'error': 'Erro ao carregar os pets',
            'detail': str(e)
        }, status=500)

# API para obter a localização do usuário (sem alterações)
@require_GET
def get_user_location(request):
    try:
        response = requests.get('https://ipinfo.io/json?token=91e3040b4f78f5')
        response.raise_for_status()
        data = response.json()

        loc = data.get('loc')
        if not loc:
            logger.warning("Localização não encontrada na resposta da API ipinfo")
            return JsonResponse({'error': 'Localização não encontrada'}, status=404)

        latitude, longitude = loc.split(',')
        logger.info(f"Localização do usuário: ({latitude}, {longitude})")
        return JsonResponse({
            'latitude': float(latitude),
            'longitude': float(longitude),
        }, encoder=DjangoJSONEncoder)

    except requests.RequestException as e:
        logger.error(f"Erro ao obter localização do usuário: {str(e)}")
        return JsonResponse({'error': 'Erro ao obter a localização', 'detail': str(e)}, status=500)
    except ValueError as e:
        logger.error(f"Erro ao processar localização: {str(e)}")
        return JsonResponse({'error': 'Erro ao processar a localização', 'detail': str(e)}, status=500)