// Search functionality
document.getElementById('searchButton').addEventListener('click', function() {
    performSearch();
});

document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

function performSearch() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.pdf-card');
    let resultsFound = false;
    
    cards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        if (title.includes(searchTerm)) {
            card.style.display = 'block';
            resultsFound = true;
            
            // Make sure the section containing this card is visible
            const section = card.closest('.pdf-section');
            if (section) {
                section.style.display = 'block';
            }
        } else {
            card.style.display = 'none';
        }
    });
    
    // Show message if no results found
    const noResultsMessage = document.getElementById('noResultsMessage');
    if (!resultsFound && searchTerm !== '') {
        if (!noResultsMessage) {
            const message = document.createElement('div');
            message.id = 'noResultsMessage';
            message.textContent = 'No results found for "' + searchTerm + '". Please try a different search term.';
            message.style.padding = '20px';
            message.style.backgroundColor = '#f8d7da';
            message.style.color = '#721c24';
            message.style.borderRadius = '5px';
            message.style.marginBottom = '20px';
            
            const main = document.querySelector('main');
            main.insertBefore(message, main.firstChild);
        }
    } else if (noResultsMessage) {
        noResultsMessage.remove();
    }
}

// Category filtering
document.querySelectorAll('.category-nav a').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Update active state
        document.querySelectorAll('.category-nav a').forEach(a => {
            a.classList.remove('active');
        });
        this.classList.add('active');
        
        const category = this.getAttribute('data-category');
        const sections = document.querySelectorAll('.pdf-section');
        
        // Reset search and display
        document.getElementById('searchInput').value = '';
        const noResultsMessage = document.getElementById('noResultsMessage');
        if (noResultsMessage) {
            noResultsMessage.remove();
        }
        
        // Show all cards
        document.querySelectorAll('.pdf-card').forEach(card => {
            card.style.display = 'block';
        });
        
        if (category === 'all') {
            sections.forEach(section => {
                section.style.display = 'block';
            });
        } else {
            sections.forEach(section => {
                if (section.id === category) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        }
    });
});