// Toggle answer visibility
function toggleAnswer(card) {
    const answer = card.querySelector('.q-answer');
    const isOpen = card.classList.contains('open');
    
    if (isOpen) {
        card.classList.remove('open');
        answer.style.display = 'none';
    } else {
        card.classList.add('open');
        answer.style.display = 'block';
    }
}

// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });
    
    // Uppercase MPESA input
    const mpesaInput = document.querySelector('[name="mpesa_code"]');
    if (mpesaInput) {
        mpesaInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    }
});
