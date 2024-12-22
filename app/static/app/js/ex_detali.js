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
  const editRateModal = document.getElementById('editRateModal')
  
  editRateModal.addEventListener('show.bs.modal', function(event) {
      const button = event.relatedTarget
      console.log('Data from card:', button.dataset) // Добавим для отладки
      
      const pairId = button.dataset.pairId
      const giveRate = button.dataset.giveRate
      const getRate = button.dataset.getRate

      const modalForm = this.querySelector('form')
      modalForm.querySelector('#pairId').value = pairId
      modalForm.querySelector('#giveRate').value = giveRate
      modalForm.querySelector('#getRate').value = getRate
  })
})




document.addEventListener('DOMContentLoaded', function() {
  const editRateModal = document.getElementById('editRateModal')
  
  editRateModal.addEventListener('show.bs.modal', function(event) {
      const button = event.relatedTarget
      const pairId = button.dataset.pairId
      const giveRate = button.dataset.giveRate
      const getRate = button.dataset.getRate

      this.querySelector('#pairId').value = pairId
      this.querySelector('#giveRate').value = giveRate
      this.querySelector('#getRate').value = getRate
  })
})
