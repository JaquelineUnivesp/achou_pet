document.getElementById('custom-date').addEventListener('change', function() {
    const selectedDate = new Date(this.value);
    const dayOfWeek = selectedDate.getDay(); // 0 (Domingo) a 6 (Sábado)

    // Verifica se é fim de semana
    if (dayOfWeek === 0 || dayOfWeek === 6) {
        this.style.color = 'orange'; // Altera a cor do texto para laranja
    } else {
        this.style.color = '#333'; // Volta ao padrão
    }

    // Verifica se é feriado (exemplo: Natal)
    const isHoliday = selectedDate.getMonth() === 11 && selectedDate.getDate() === 25; // 25 de Dezembro
    if (isHoliday) {
        this.style.color = 'orange'; // Altera a cor do texto para laranja
    }
});