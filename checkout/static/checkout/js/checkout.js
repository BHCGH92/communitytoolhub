document.addEventListener('DOMContentLoaded', function() {
    const checkoutForm = document.getElementById('checkout-form');

    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function(e) {
            // Stop the browser from submitting immediately
            e.preventDefault();

            // Confirmation popup
            const confirmBorrow = confirm(
                "This tool is a 7-day minimum hire.\n" +
                "You will be redirected to our secure payment gateway."
            );

            if (confirmBorrow) {
                const submitBtn = this.querySelector('button[type="submit"]');
                
                // Visual feedback
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Redirecting...';
                submitBtn.style.pointerEvents = 'none'; // Prevent double-clicks
                
                // Submit the form manually
                this.submit();
            }
        });
    }
});