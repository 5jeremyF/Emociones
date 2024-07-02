document.addEventListener('DOMContentLoaded', function () {
    fetch('/histories/')
        .then(response => response.json())
        .then(histories => {
            const historyContainer = document.getElementById('historyContainer');


            histories.forEach(history => {
                const historyCard = document.createElement('div');
                historyCard.classList.add('rounded-lg', 'border', 'bg-card', 'text-card-foreground', 'shadow-sm', 'p-4');

                historyCard.innerHTML = `
                    <img src="${history.album_cover}" alt="Album Cover" width="200" height="200" class="rounded-lg mb-4" style="aspect-ratio: 200 / 200; object-fit: cover" />
                    <h3 class="text-lg font-bold mb-2">${history.music_title}</h3>
                    <p class="text-gray-500 mb-2">${history.artist_name}</p>
                    <p class="text-gray-500 mb-2">Listened on: ${new Date(history.listened_date).toLocaleString()}</p>
                    <div class="flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5 text-green-500">
                            <circle cx="12" cy="12" r="10"></circle>
                            <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                            <line x1="9" x2="9.01" y1="9" y2="9"></line>
                            <line x1="15" x2="15.01" y1="9" y2="9"></line>
                        </svg>
                        <span class="text-sm text-green-500">${history.emotion}</span>
                    </div>
                `;

                historyContainer.appendChild(historyCard);
            });
        })
        .catch(error => console.error('Error fetching history:', error));
});
