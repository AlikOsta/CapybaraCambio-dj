document.addEventListener('DOMContentLoaded', function() {

  const form = document.querySelector('form');
  const errorMessage = document.querySelector('.error');
  const submitButton = document.querySelector('#add_ex');

  if (submitButton && typeof userBalance !== 'undefined' && typeof exchangePrice !== 'undefined') {
    if (userBalance < exchangePrice) {
      submitButton.disabled = true;
      errorMessage.textContent = `Ваш баланс: ${userBalance} coin. `;

    }
  }
});

const addExchangeModal = new bootstrap.Modal(document.getElementById('addExchangeModal'));

document.getElementById('addExchangeModal').addEventListener('hidden.bs.modal', event => {
  const form = event.target.querySelector('form');
  const previewImage = event.target.querySelector('.image-preview__image');
  const placeholderIcon = event.target.querySelector('.placeholder-icon');
  const fileLabelText = event.target.querySelector('.file-label-text');

  form.reset();
  previewImage.src = '';
  previewImage.classList.add('d-none');
  placeholderIcon.classList.remove('d-none');
  fileLabelText.textContent = 'Выберите логотип';
});

document.addEventListener("DOMContentLoaded", () => {
  const ratings = document.querySelectorAll('.rating');
  
  ratings.forEach(rating => {
    const ratingValue = parseFloat(rating.querySelector('.rating-value').textContent.replace(/[()]/g, ''));
    const starsInner = rating.querySelector('.stars-inner');
    if (ratingValue >= 0 && ratingValue <= 5) {
      const widthPercentage = (ratingValue / 5) * 100;
      starsInner.style.width = `${widthPercentage}%`;
    }
  });
});

document.addEventListener('DOMContentLoaded', function() {
  const logoInput = document.querySelector('input[type="file"]');
  const previewImage = document.querySelector('.image-preview__image');
  const placeholderIcon = document.querySelector('.placeholder-icon');

  logoInput.addEventListener('change', function() {
      const file = this.files[0];
      if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
              previewImage.src = e.target.result;
              previewImage.classList.remove('d-none');
              placeholderIcon.classList.add('d-none');
          }
          reader.readAsDataURL(file);
      }
  });
});