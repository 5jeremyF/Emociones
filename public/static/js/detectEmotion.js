document.addEventListener('DOMContentLoaded', function () {
    let path_music = localStorage.getItem('path_song') || null;
    let emotionDetected = localStorage.getItem('detectedEmotion') || null;
    let list_music = JSON.parse(localStorage.getItem('list_music')) || null;
    let audioPlayer = document.getElementById('audioPlayer');
    let playPauseBtn = document.getElementById('playPauseBtn');
    let playIcon = document.getElementById('playIcon');
    let pauseIcon = document.getElementById('pauseIcon');
    const guardarBoton = document.getElementById('save');
    const saveFavoritiesButton = document.getElementById('save_favorities');

    let musicData = null; // Variable para almacenar los datos de la música seleccionada

    // Función para reproducir la música seleccionada
    function playSelectedMusic(songPath) {
        if (songPath) {
            audioPlayer.src = songPath;
            audioPlayer.load();
            audioPlayer.play();
            playIcon.style.display = 'none';
            pauseIcon.style.display = 'block';

            // Guardar la canción seleccionada en localStorage
            localStorage.setItem('path_song', songPath);
            // Actualizar path_music con la nueva canción
            path_music = songPath;
            console.log(path_music);
            // Llamar a la API para obtener datos adicionales de la canción
            fetch(`/deezer_search/?query=${encodeURIComponent(extractSongName(songPath))}`)
                .then(deezerResponse => deezerResponse.json())
                .then(deezerData => {
                    if (deezerData.data && deezerData.data.length > 0) {
                        const track = deezerData.data[0];
                        console.log(track);
                        document.getElementById('artistName').textContent = ' emocion: ' + emotionDetected;
                        document.getElementById('albumCover').src = track.album.cover;
                        document.getElementById('songTitle').textContent = track.title + ' - ' + track.artist.name;
                        document.getElementById('imgMusic').src = track.album.cover;
                        // Guardar los datos en la base de datos
                        saveMusicData(track);
                        musicData = track; // Guardar datos de la música seleccionada
                    } else {
                        console.error('No se encontraron resultados en Deezer.');
                    }
                })
                .catch(error => console.error('Error buscando en Deezer:', error));
        }
    }

    // Función para guardar los datos de la música en la base de datos
    function saveMusicData(trackData) {
        // Preparar los datos para enviar a tu servidor
        console.log(path_music);
        const musicInfo = {
            title: trackData.title,
            artist: trackData.artist.name,
            song_path: path_music,
            emotion: emotionDetected,
            genre: trackData.genre || 'Unknown',
            link: trackData.link,
            preview: trackData.preview,
            duration: trackData.duration,
            image: trackData.album.cover
        };
        console.log(musicInfo);

        // Realizar una solicitud POST a tu API para guardar los datos
        fetch('/savemusic', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(musicInfo)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al guardar los datos de la música.');
            }
            console.log('Datos de música guardados exitosamente.');

            // Guardar el historial de la música
            saveHistory(trackData);
        })
        .catch(error => console.error('Error al guardar los datos de la música:', error));
    }

    // Función para guardar el historial de la música
    function saveHistory(trackData) {
        const historyData = {
            music_id: trackData.title
        };

        // Realizar una solicitud POST para guardar el historial
        fetch('/saveHistories', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(historyData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al guardar el historial de la música.');
            }
            console.log('Historial de música guardado exitosamente.');
        })
        .catch(error => console.error('Error al guardar el historial de la música:', error));
    }

    // Función para guardar la música en favoritos
    function saveFavorities(trackData) {
        const favoritiesData = {
            music_id: trackData.title
        };
        console.log(
                favoritiesData
            )

        // Realizar una solicitud POST para guardar en favoritos
        fetch('/add_to_favorites', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(favoritiesData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al guardar en favoritos.');
            }
            console.log(response);
        })
        .catch(error => console.error('Error al guardar la música a favoritos:', error));
    }

    // Mostrar la lista de canciones en el template
    if (list_music) {
        const musicListElement = document.getElementById('musicList');
        musicListElement.innerHTML = '';

        list_music.forEach((songPath, index) => {
            const songName = extractSongName(songPath);

            const songRow = document.createElement('tr');
            songRow.classList.add('border-b', 'transition-colors', 'hover:bg-gray-200', 'cursor-pointer', 'data-[state=selected]:bg-muted');
            songRow.addEventListener('click', () => {
                playSelectedMusic(songPath);
                document.getElementById('titleMusic').textContent = 'Reproduciendo... ' + songName;
            });

            const numberCell = document.createElement('td');
            numberCell.classList.add('p-4', 'align-middle', '[&:has([role=checkbox])]:pr-0');
            numberCell.textContent = index + 1;

            const descriptionCell = document.createElement('td');
            descriptionCell.classList.add('p-4', 'align-middle', '[&:has([role=checkbox])]:pr-0');
            descriptionCell.textContent = songName;

            songRow.appendChild(numberCell);
            songRow.appendChild(descriptionCell);
            musicListElement.appendChild(songRow);
        });

        const titleEmotion = document.getElementById('titleEmotion');
        titleEmotion.innerHTML = '';
        titleEmotion.innerHTML = 'lista de musica para tu emocion - ' + emotionDetected;
    }
    if (emotionDetected) {
        document.getElementById('titleOne').textContent = 'Su Ultima emocion detectada es: ' + emotionDetected;
    }

    playPauseBtn.addEventListener('click', function () {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playIcon.style.display = 'none';
            pauseIcon.style.display = 'block';
        } else {
            audioPlayer.pause();
            playIcon.style.display = 'block';
            pauseIcon.style.display = 'none';
        }
    });

    // Agregar evento de clic al botón de favoritos
    saveFavoritiesButton.addEventListener('click', function () {
        if (musicData) {

            saveFavorities(musicData);
        } else {
            console.error('No hay datos de música seleccionada para guardar en favoritos.');
        }
    });

    // Función para extraer el nombre de la canción desde su ruta
    function extractSongName(songPath) {
        const parts = songPath.split('/');
        const fileName = parts[parts.length - 1];
        const nameWithoutExtension = fileName.replace(/\.[^/.]+$/, "");
        return nameWithoutExtension.replace(/-/g, ' ').trim();
    }

    // Función para obtener el valor del token CSRF de las cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Buscar el token CSRF
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
