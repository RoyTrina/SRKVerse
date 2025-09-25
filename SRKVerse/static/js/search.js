document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('input[name="q"]');
    searchInput.addEventListener('input', () => {
        // Add AJAX call to API for live suggestions
        console.log('Searching for:', searchInput.value);
    });
});