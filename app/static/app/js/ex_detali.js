class ModalHandler {
  constructor(modalId, btnId, closeBtnId) {
      this.modal = document.getElementById(modalId);
      this.modalContent = this.modal.querySelector(".modal-content");
      this.openBtn = document.getElementById(btnId);
      this.closeBtn = document.getElementById(closeBtnId);
      this.form = this.modal.querySelector("form");
      this.errorMessage = this.modal.querySelector(".error");
      
      this.initializeEvents();
      this.initialImageSrc = this.previewImage?.src || '';
      this.initialLabelText = this.fileLabelText?.textContent || 'Ваш логотип';
  }

  initializeEvents() {
      this.openBtn?.addEventListener("click", () => this.openModal());
      this.closeBtn?.addEventListener("click", () => this.closeModal());
      this.modal?.addEventListener("click", (e) => {
          if (e.target === this.modal) this.closeModal();
      });
      this.form?.addEventListener("submit", (e) => this.handleSubmit(e));
  }

  openModal() {
      this.modal.classList.add("show");
      this.modalContent.classList.add("show");
  }

  resetFileInput() {
      if (this.previewImage && this.svgIcon && this.fileLabelText) {
          if (this.initialImageSrc) {
              this.previewImage.src = this.initialImageSrc;
              this.previewImage.style.display = 'block';
              this.svgIcon.style.display = 'none';
          } else {
              this.previewImage.style.display = 'none';
              this.previewImage.src = '';
              this.svgIcon.style.display = 'block';
          }
          this.fileLabelText.textContent = this.initialLabelText;
      }
  }

  closeModal() {    
      this.modal.classList.remove("show");
      this.modalContent.classList.remove("show");
      if (this.form) {
          this.form.reset();
          this.resetFileInput();
      }
      if (this.errorMessage) {
          this.errorMessage.innerHTML = "";
      }

      const bestRateInfo = document.querySelector('.best-rate-info');
      if (bestRateInfo) {
          bestRateInfo.querySelector('.best-rate-exchange').textContent = '';
          bestRateInfo.querySelector('.best-give-rate').textContent = '';
          bestRateInfo.querySelector('.best-get-rate').textContent = '';
      }
  }

  async handleSubmit(e) {
    e.preventDefault();
    const formData = new FormData(this.form);

    try {
        const response = await fetch(window.location.href, {
            method: "POST",
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
            body: formData,
        });

        // Проверяем HTTP статус ответа
        if (!response.ok) {
            const errorText = `Ошибка сервера: ${response.status} ${response.statusText}`;
            this.errorMessage.innerHTML = `Произошла ошибка: ${errorText}`;
            console.error(errorText, await response.text());
            return;
        }

        const data = await response.json();

        if (data.success) {
          this.closeModal();
          location.reload();
      } else {
            let errorDetails = "Неизвестная ошибка.";
            if (data.error) {
                if (data.error["__all__"]) {
                    errorDetails = data.error["__all__"].join(", "); 
                } else {
                    errorDetails = JSON.stringify(data.error, null, 2);
                }
            }

            this.errorMessage.innerHTML = `Ошибка: ${errorDetails}`;
            console.error("Ошибка ответа сервера:", data);
        }
    } catch (error) {
        this.errorMessage.innerHTML = `Ошибка при отправке формы: ${error.message}`;
        console.error("Ошибка при выполнении запроса:", error);
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const verifyModal = document.getElementById("modal-verify");
  const verifyBtn = document.getElementById("verify-btn");
  const closeVerifyBtn = document.getElementById("close-modal-verify");
  
  if (verifyModal && verifyBtn && closeVerifyBtn) {
    new ModalHandler("modal-verify", "verify-btn", "close-modal-verify");
  }

  const pairModal = document.getElementById("modal");
  const addPairBtn = document.getElementById("add-pair-btn");
  const closePairBtn = document.getElementById("close-modal");
  
  if (pairModal && addPairBtn && closePairBtn) {
    new ModalHandler("modal", "add-pair-btn", "close-modal");
  }

  const deliveryModal = document.getElementById("modal-delivery");
  const deliveryBtn = document.getElementById("delivery-btn");
  const closeDeliveryBtn = document.getElementById("close-modal-delivery");
  
  if (deliveryModal && deliveryBtn && closeDeliveryBtn) {
    new ModalHandler("modal-delivery", "delivery-btn", "close-modal-delivery");
  }

  const editDeliveryModal = document.getElementById("modal-edit-delivery");
  const editDeliveryBtn = document.getElementById("edit-delivery-btn");
  const closeEditDeliveryBtn = document.getElementById("close-edit-delivery");
  
  if (editDeliveryModal && editDeliveryBtn && closeEditDeliveryBtn) {
      new ModalHandler("modal-edit-delivery", "edit-delivery-btn", "close-edit-delivery");
  }

  const editExchangeModal = document.getElementById("modal-edit-exchange");
  const editExchangeBtn = document.getElementById("edit-exchange-btn");
  const closeEditExchangeBtn = document.getElementById("close-edit-exchange");
  
  if (editExchangeModal && editExchangeBtn && closeEditExchangeBtn) {
      new ModalHandler("modal-edit-exchange", "edit-exchange-btn", "close-edit-exchange");
  }

  const verifyInfoModal = document.getElementById("modal-verify-info");
  const showVerifyInfoBtn = document.getElementById("show-verify-info-btn");
  const closeVerifyInfoBtn = document.getElementById("close-verify-info");
  
  if (verifyInfoModal && showVerifyInfoBtn && closeVerifyInfoBtn) {
      new ModalHandler("modal-verify-info", "show-verify-info-btn", "close-verify-info");
  }
  
  const tabs = document.querySelectorAll('.tab');
  const tabLine = document.querySelector('.tab-line');

  if (tabs.length && tabLine) {
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => {
        document.querySelector('.tab.active')?.classList.remove('active');
        tab.classList.add('active');
        
        const contentType = tab.getAttribute('data-content');
        document.querySelectorAll('.content').forEach(contentBlock => {
          contentBlock.style.display = 'none';
        });

        document.getElementById(`${contentType}-content`).style.display = 'flex';
        tabLine.style.transform = `translateX(${index * 100}%)`;
      });
    });
  }
});


document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.querySelector("input[type='file']");
  const label = document.querySelector(".custom-file-label");
  const previewContainer = document.querySelector("#imagePreview");
  const previewImage = previewContainer.querySelector(".image-preview__image");

  const previewImage2 = previewImage


  if (fileInput && label) {
    fileInput.addEventListener("change", () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();

        reader.addEventListener("load", () => {
          previewImage.setAttribute("src", reader.result);
          previewImage.style.display = "block";
        });

        reader.readAsDataURL(file);

        const fileName = "Ноыовый логотип";
        label.querySelector(".file-label-text").textContent = fileName;
        label.classList.add("active");

      } else {
        previewImage.setAttribute("src", previewImage2);
        label.querySelector(".file-label-text").textContent = "Ваш логотип";
        label.classList.remove("active");
      }
    });
  }

  function updateStars(container, rating) {
    const stars = container.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
  }

});


document.addEventListener('DOMContentLoaded', function() {
  const verificationSelect = document.getElementById('verification-select');
  const priceDisplay = document.getElementById('verification-price');
  const logoDisplay = document.getElementById('selected-logo');

  if (verificationSelect) {
      verificationSelect.addEventListener('change', function() {
          const selectedOption = this.options[this.selectedIndex];
          const price = selectedOption.dataset.price || '0';
          const logo = selectedOption.dataset.logo || '';
          
          priceDisplay.textContent = price;
          logoDisplay.src = logo;
          logoDisplay.style.display = logo ? 'block' : 'none';
      });
  }
});

document.getElementById('give-select').addEventListener('change', function() {
  var selectedOption = this.options[this.selectedIndex];
  var logoUrl = selectedOption.getAttribute('data-logo');

  var giveLogoImg = document.querySelector('img.give_logo');
  if (giveLogoImg) {
    giveLogoImg.src = logoUrl || '';  
    giveLogoImg.alt = selectedOption.textContent || 'Логотип валюты';  
    giveLogoImg.style.display = logoUrl ? 'block' : 'none';
  }
});

document.getElementById('get-select').addEventListener('change', function() {
  var selectedOption = this.options[this.selectedIndex];
  var logoUrl = selectedOption.getAttribute('data-logo');

  var getLogoImg = document.querySelector('img.get_logo');
  if (getLogoImg) {
    getLogoImg.src = logoUrl || '';  
    getLogoImg.alt = selectedOption.textContent || 'Логотип валюты'; 
    getLogoImg.style.display = logoUrl ? 'block' : 'none';
  }
});


function openEditPairModal(element) {
  const pairId = element.dataset.pairId;
  const giveRate = element.dataset.giveRate;
  const getRate = element.dataset.getRate;
  const giveLogo = element.querySelector('.give_info img').src;
  const getLogo = element.querySelector('.get_info img').src;

  document.getElementById('edit-pair-id').value = pairId;
  document.getElementById('edit-give-rate').value = giveRate;
  document.getElementById('edit-get-rate').value = getRate;
  document.getElementById('edit-give-logo').src = giveLogo;
  document.getElementById('edit-get-logo').src = getLogo;

  const modal = document.getElementById('modal-edit-pair');
  modal.classList.add('show');
  modal.querySelector('.modal-content').classList.add('show');
}



document.addEventListener("DOMContentLoaded", () => {

    const editPairModal = document.getElementById("modal-edit-pair");
    const closeEditPairBtn = document.getElementById("close-edit-pair");
    
    if (editPairModal && closeEditPairBtn) {
        new ModalHandler("modal-edit-pair", null, "close-edit-pair");
    }
});


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


async function checkBestRate() {
  const giveCurrency = document.getElementById('give-select').value;
  const getCurrency = document.getElementById('get-select').value;

  if (giveCurrency && getCurrency) {
      const formData = new FormData();
      formData.append('give_currency', giveCurrency);
      formData.append('get_currency', getCurrency);
      formData.append('form_type', 'check_rate');

      try {
          const response = await fetch(window.location.href, {
              method: 'POST',
              headers: {
                  'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
              },
              body: formData
          });

          const data = await response.json();
          if (data.best_rate) {
              const bestRateInfo = document.querySelector('.best-rate-info');
              bestRateInfo.querySelector('.best-rate-exchange').textContent = data.best_rate.exchange_name;
              bestRateInfo.querySelector('.best-give-rate').textContent = data.best_rate.give_rate;
              bestRateInfo.querySelector('.best-get-rate').textContent = data.best_rate.get_rate;
          }
      } catch (error) {
          console.error('Ошибка при получении лучшего курса:', error);
      }
  }
}

