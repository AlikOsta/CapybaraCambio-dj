document.addEventListener("DOMContentLoaded", () => {
  'use strict';

  // Инициализация модальных окон Bootstrap
  const exchangeModal = new bootstrap.Modal(document.getElementById('modal'));
  const balanceModal = new bootstrap.Modal(document.getElementById('modal-balance'));

  // Кнопки открытия модальных окон
  const addBtn = document.getElementById("add_btn");
  const balanceBtn = document.getElementById("add_balanse");

  // Управление формой обменника
  const form = document.querySelector("#modal form");
  const fileInput = form.querySelector("input[type='file']");
  const previewImage = document.querySelector(".image-preview__image");
  const fileLabelText = document.querySelector(".file-label-text");

  // Открытие модальных окон
  addBtn.addEventListener("click", () => exchangeModal.show());
  balanceBtn.addEventListener("click", () => balanceModal.show());

  // Обработка загрузки изображения
  fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        previewImage.src = reader.result;
        previewImage.classList.remove('d-none');
        fileLabelText.textContent = file.name.length > 20
          ? `${file.name.substring(0, 17)}...`
          : file.name;
      };
      reader.readAsDataURL(file);
    } else {
      resetFileInput();
    }
  });

  // Сброс формы при закрытии
  document.getElementById('modal').addEventListener('hidden.bs.modal', () => {
    form.reset();
    resetFileInput();
  });

  // Функция сброса предпросмотра файла
  const resetFileInput = () => {
    previewImage.classList.add('d-none');
    previewImage.src = '';
    fileLabelText.textContent = 'Выберите логотип';
  };

  // Проверка баланса
  const errorMessage = document.querySelector(".error");
  const updateButtonState = () => {
    const submitBtn = form.querySelector("button[type='submit']");
    if (userBalance < exchangePrice) {
      submitBtn.disabled = true;
      errorMessage.textContent = `Ваш баланс: ${userBalance} coin. Не хватает ${exchangePrice - userBalance} coin.`;
    } else {
      submitBtn.disabled = false;
      errorMessage.textContent = "";
    }
  };
  updateButtonState();
});

// Инициализация рейтинга
document.addEventListener("DOMContentLoaded", () => {
  const ratings = document.querySelectorAll('.rating');
  ratings.forEach(rating => {
    const ratingValue = parseFloat(rating.querySelector('.rating-number').textContent.replace(/[()]/g, ''));
    const starsInner = rating.querySelector('.stars-inner');
    if (ratingValue >= 0 && ratingValue <= 5) {
      const widthPercentage = (ratingValue / 5) * 100;
      starsInner.style.width = `${widthPercentage}%`;
    }
  });
});
