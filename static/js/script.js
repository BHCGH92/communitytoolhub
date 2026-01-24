/* JS Validation for Tool Borrowing on tool_detail.html */
document.addEventListener("DOMContentLoaded", function() {
    const dateInput = document.getElementById('borrow_date');
    const errorDiv = document.getElementById('date-error');
    const helpDiv = document.getElementById('date-help');
    const submitBtn = document.querySelector('.btn-borrow');

    if (dateInput) {
        const today = new Date();
        const maxDate = new Date();
        maxDate.setDate(today.getDate() + 5);

        const todayStr = today.toISOString().split('T')[0];
        const maxStr = maxDate.toISOString().split('T')[0];

        dateInput.min = todayStr;
        dateInput.max = maxStr;

        dateInput.addEventListener('change', function() {
            const val = this.value;

            if (val && (val < todayStr || val > maxStr)) {
                dateInput.classList.add('border-danger', 'text-danger');
                errorDiv.classList.remove('d-none');
                helpDiv.classList.add('d-none');
                submitBtn.disabled = true;
            } else {
                dateInput.classList.remove('border-danger', 'text-danger');
                errorDiv.classList.add('d-none');
                helpDiv.classList.remove('d-none');
                submitBtn.disabled = false;
            }
        });
    }
});