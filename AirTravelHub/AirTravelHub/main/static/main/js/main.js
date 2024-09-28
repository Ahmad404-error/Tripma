
document.getElementById('openModal').addEventListener('click', function(){
    const modal = document.getElementById('register_content');
    const background = document.getElementById('register_center');
    background.classList.add('active');
    modal.classList.add('active');

});

document.getElementById('close_model').addEventListener('click', function(){
    const modal = document.getElementById('register_content');
    const background = document.getElementById('register_center');
    modal.classList.remove('active');
    background.classList.remove('active');
    document.body.classList.remove('no-scroll');

});


// Закрытие модального окна по клику на фон
document.getElementById('register_center').addEventListener('click', function(event) {
    const modal = document.getElementById('register_content');
    const background = document.getElementById('register_center');
    
    // Проверка, что клик был именно на фон, а не на само модальное окно
    if (event.target === event.currentTarget) {
        modal.classList.remove('active');
        background.classList.remove('active');
    }

});


