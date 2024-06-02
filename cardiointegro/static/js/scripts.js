window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY === 0) {
      header.classList.remove('backdrop-blur-full');
    } else {
      header.classList.add('backdrop-blur-full');
    }
  });


  document.querySelector('#openModalButton').addEventListener('click', function(event) {
    event.preventDefault(); // Предотвращение отправки формы
    // Здесь добавьте код для открытия модального окна
});
