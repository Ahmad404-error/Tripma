document.addEventListener('DOMContentLoaded', function () {
    // Найдем поле ввода для стран и контейнер для подсказок
    const countryInput = document.getElementById('citizenship');
    const suggestionsContainer = document.getElementById('citizenship_suggestions');

    // Добавим обработчик для события ввода текста
    countryInput.addEventListener('input', function () {
        const query = countryInput.value; // Получаем значение, которое ввел пользователь
        console.log(query)
        // Если пользователь ничего не ввел, очистим список подсказок
        if (!query) {
            suggestionsContainer.innerHTML = '';
            return;
        }

        // Отправляем запрос на сервер
        fetch(`/autocomplete/country/?term=${query}`)
            .then(response => response.json()) // Парсим JSON-ответ
            .then(data => {
                suggestionsContainer.innerHTML = ''; // Очистим контейнер подсказок

                // Пройдемся по каждому объекту из массива данных
                data.forEach(item => {
                    // Создаем новый элемент div для каждой подсказки
                    const suggestion = document.createElement('div');
                    suggestion.classList.add('autocomplete_suggestion');
                    suggestion.textContent = item.label; // Отображаем название страны

                    // Добавляем событие клика, чтобы при выборе подсказки вставлять значение в input
                    suggestion.addEventListener('click', function () {
                        countryInput.value = item.value; // Вставляем код страны
                        suggestionsContainer.innerHTML = ''; // Очищаем список подсказок
                    });

                    // Добавляем подсказку в контейнер
                    suggestionsContainer.appendChild(suggestion);
                });
            })
            .catch(error => {
                console.error('Error fetching country autocomplete data:', error);
            });
    });
});
