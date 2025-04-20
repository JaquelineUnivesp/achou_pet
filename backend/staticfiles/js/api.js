// frontend/static/js/api.js
const API_BASE_URL = 'https://achou-pet.onrender.com';

async function fetchPets() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/pets/`);
    if (!response.ok) {
      throw new Error('Erro ao buscar pets');
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro na API:', error);
    return [];
  }
}
