document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("modal");
  const modalContent = modal.querySelector(".modal-content");
  const addPairBtn = document.getElementById("add-pair-btn");
  const closeModalBtn = document.getElementById("close-modal");
  const errorMessage = document.querySelector(".error");

  const openModal = () => {
    modal.classList.add("show");
    modalContent.classList.add("show");
  };

  const closeModal = () => {
    modal.classList.remove("show");
    modalContent.classList.remove("show");
    form.reset();
    errorMessage.innerHTML = "";
  };

  addPairBtn.addEventListener("click", openModal);

  closeModalBtn.addEventListener("click", closeModal);

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      closeModal();
    }
  });

  // убрать дубли добавления пар
  // работает криво
  const form = modal.querySelector("form");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const csrfToken = formData.get("csrfmiddlewaretoken");
    const response = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        console.log("Закрытие модального окна");
        closeModal();
        location.reload();
        // после добавления закрыть окно, перезагрузить страницу
      } else {
        errorMessage.innerHTML = "Ошибка при добавлении пары.";
      }
    } else {
      errorMessage.innerHTML = "Ошибка при добавлении пары.";
    }
  });
});

// перенести а отдельный фал для редактирования
document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("id_logo");
  const logoPreview = document.getElementById("logo-preview");

  fileInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        logoPreview.src = e.target.result;
      };

      reader.readAsDataURL(file);
    }
  });
});
