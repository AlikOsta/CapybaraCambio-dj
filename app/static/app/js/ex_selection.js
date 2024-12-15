document.addEventListener("DOMContentLoaded", () => {
  'use strict';
  const toggleModal = (modal, action) => {
    const modalContent = modal.querySelector(".modal-content");
    if (action === "open") {
      modal.classList.add("show");
      modalContent.classList.add("show");
    } else {
      modal.classList.remove("show");
      modalContent.classList.remove("show");
    }
  };

  // Управление основным модальным окном
  const modal = document.getElementById("modal");
  const addBtn = document.getElementById("add_btn");
  const closeModalBtn = document.getElementById("close-modal");
  const form = modal.querySelector("form");
  const previewImage = document.querySelector(".image-preview__image");
  const svgIcon = document.querySelector(".svg");
  const fileLabelText = document.querySelector(".file-label-text");

  // Функция сброса формы выбора файла
  const resetFileInput = () => {
    previewImage.style.display = "none";
    previewImage.src = "";
    svgIcon.style.display = "block";
    fileLabelText.textContent = "Выберите логотип";
  };

  // Открытие модального окна
  addBtn.addEventListener("click", () => toggleModal(modal, "open"));

  // Закрытие по кнопке
  closeModalBtn.addEventListener("click", () => {
    toggleModal(modal, "close");
    form.reset();
    resetFileInput();
  });

  // Закрытие по клику вне модального окна
  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      toggleModal(modal, "close");
      form.reset();
      resetFileInput();
    }
  });

  // Управление файлом
  const fileInput = document.querySelector("input[type='file']");

  if (fileInput) {
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          previewImage.src = reader.result;
          previewImage.style.display = "block";
          svgIcon.style.display = "none"; 
          fileLabelText.textContent = file.name.length > 20
            ? `${file.name.substring(0, 17)}...`
            : file.name;
        };
        reader.readAsDataURL(file);
      } else {
        resetFileInput();
      }
    });
  }

  const balanceModal = document.getElementById("modal-balance");
  const balanceBtn = document.getElementById("add_balanse");
  const closeBalanceBtn = document.getElementById("close-modal-balance");

  if (balanceModal && balanceBtn && closeBalanceBtn) {
      // Открытие модального окна
      balanceBtn.addEventListener("click", () => {
          balanceModal.classList.add("show");
          balanceModal.querySelector(".modal-content").classList.add("show");
      });

      // Закрытие по кнопке
      closeBalanceBtn.addEventListener("click", () => {
          balanceModal.classList.remove("show");
          balanceModal.querySelector(".modal-content").classList.remove("show");
      });

      // Закрытие по клику вне модального окна
      balanceModal.addEventListener("click", (e) => {
          if (e.target === balanceModal) {
              balanceModal.classList.remove("show");
              balanceModal.querySelector(".modal-content").classList.remove("show");
          }
      });
  }

  // Проверка баланса
  const errorMessage = document.querySelector(".error");

  const updateButtonState = () => {
    const addBtn = document.querySelector(".btn-primary");
    if (userBalance < exchangePrice) {
      addBtn.disabled = true;
      errorMessage.textContent = `Ваш баланс: ${userBalance} coin. Не хватает ${exchangePrice - userBalance} coin.`;
    } else {
      addBtn.disabled = false;
      errorMessage.textContent = "";
    }
  };

  updateButtonState();
});
