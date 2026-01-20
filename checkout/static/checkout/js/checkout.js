document.addEventListener('DOMContentLoaded', function() {
    const borrowButtons = document.querySelectorAll('.btn-borrow');

    borrowButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            //Prevent the link from firing immediately
            e.preventDefault();
            const toolName = this.getAttribute('data-tool-name');
            const url = this.getAttribute('href');

            // Confirmation popup
            const confirmBorrow = confirm(
                `Confirm Rental: ${toolName}\n\n` +
                `This tool is a 7-day minimum hire.\n` +
                `You will be redirected to our secure payment gateway.`
            );

            if (confirmBorrow) {
                // Provides immediate feedback/loading state
                this.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Redirecting...';
                this.classList.add('disabled');
                window.location.href = url;
            }
        });
    });
});