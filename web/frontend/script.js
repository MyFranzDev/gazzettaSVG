// Global utility functions

// Smooth scroll to top on step change
window.addEventListener('load', function() {
    window.scrollTo({top: 0, behavior: 'smooth'});
});

// Form validation helper
function validateStep(stepNumber) {
    const form = document.querySelector('form');
    if (!form) return true;

    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (field.type === 'radio') {
            const radioGroup = form.querySelectorAll(`[name="${field.name}"]`);
            const isChecked = Array.from(radioGroup).some(r => r.checked);
            if (!isChecked) {
                isValid = false;
                field.closest('.form-group').style.border = '2px solid #f44336';
            }
        } else if (field.type === 'checkbox') {
            const checkboxGroup = form.querySelectorAll(`[name="${field.name}"]`);
            const isChecked = Array.from(checkboxGroup).some(c => c.checked);
            if (!isChecked) {
                isValid = false;
            }
        } else if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#f44336';
        }
    });

    if (!isValid) {
        alert('Per favore compila tutti i campi obbligatori');
    }

    return isValid;
}

// Auto-save to localStorage (optional, for better UX)
function autoSave() {
    const wizardData = {};
    document.querySelectorAll('[name^="data["]').forEach(input => {
        const name = input.name.match(/data\[(.*?)\]/)[1];
        if (input.type === 'checkbox') {
            wizardData[name] = wizardData[name] || [];
            if (input.checked) {
                wizardData[name].push(input.value);
            }
        } else if (input.type === 'radio') {
            if (input.checked) {
                wizardData[name] = input.value;
            }
        } else {
            wizardData[name] = input.value;
        }
    });
    localStorage.setItem('wizardData', JSON.stringify(wizardData));
}

// Set interval for auto-save (every 30 seconds)
if (document.querySelector('form')) {
    setInterval(autoSave, 30000);
}

console.log('🏆 Gazzetta Multi-Banner Generator - Frontend Ready!');
