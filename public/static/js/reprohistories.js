document.addEventListener('DOMContentLoaded', () => {
    const playIcons = document.querySelectorAll('.play-icon');
  
    playIcons.forEach(icon => {
      icon.addEventListener('click', () => {
        const songPath = icon.getAttribute('data-song-path');
        const audioPlayer = document.getElementById('audioPlayer'); // Suponiendo que tu elemento de audio tiene este ID
        audioPlayer.src = songPath;
        audioPlayer.play();
      });
    });
  });
  