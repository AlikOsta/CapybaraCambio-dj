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
