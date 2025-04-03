# backend/apps/pet_registration/services/pet_filter.py

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.contrib.gis.geos import Point
from django.db.models import QuerySet
import logging

logger = logging.getLogger(__name__)

def location_to_point(location_str: str) -> Point | None:
    """
    Converte uma string de localização em um ponto geográfico (longitude, latitude).
    """
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

def filter_by_location(queryset: QuerySet, location_str: str, max_km: float) -> QuerySet:
    """
    Filtra um queryset de pets (com latitude/longitude) por distância a uma localização textual.
    Retorna apenas os pets com distância <= max_km (em km).
    """
    user_point = location_to_point(location_str)
    if not user_point:
        logger.warning("Não foi possível converter localização. Filtro por texto.")
        return queryset.filter(location__icontains=location_str)

    filtered_ids = []
    for pet in queryset:
        if pet.latitude is not None and pet.longitude is not None:
            pet_coords = (float(pet.latitude), float(pet.longitude))
            user_coords = (user_point.y, user_point.x)  # Point(x=lon, y=lat)
            try:
                distance = geodesic(pet_coords, user_coords).km
                if distance <= max_km:
                    filtered_ids.append(pet.id)
            except Exception as e:
                logger.error(f"Erro ao calcular distância para pet {getattr(pet, 'id', 'desconhecido')}: {str(e)}")

    return queryset.filter(id__in=filtered_ids)
