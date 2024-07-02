document.addEventListener('DOMContentLoaded', function () {
  let emotionDetected = localStorage.getItem('detectedEmotion') || null;
  let list_music = localStorage.getItem('list_music') || null;
  let path_music = localStorage.getItem('path_song') || null;
  let videoElement = document.getElementById('video');
  let canvasElement = document.getElementById('canvas');
  let cameraModal = document.getElementById('cameraModal');
  let closeCameraModalBtn = document.getElementById('closeCameraModal');
  let startEmotionsBtn = document.getElementById('startEmotionsBtn');

  let stream = null;
  let sendingFrames = false; // Bandera para controlar el envío de cuadros al servidor
  let intervalId = null; // Identificador del intervalo para el envío de cuadros

  // Mostrar modal de la cámara al hacer clic en el botón de inicio de emociones
  startEmotionsBtn.addEventListener('click', function () {
    if (emotionDetected) {
      console.log('Ya se detectó una emoción previamente:', emotionDetected);
      clearSession(); // Limpiar sesión y reiniciar el proceso
    }

    openCameraModal();
    startCamera();
  });

  // Cerrar modal de la cámara al hacer clic en el botón de cierre
  closeCameraModalBtn.addEventListener('click', function () {
    closeCameraModal();
    stopSendingFrames();
  });

  // Función para abrir el modal de la cámara
  function openCameraModal() {
    cameraModal.classList.remove('hidden');
    document.body.classList.add('overflow-hidden');
  }

  // Función para cerrar el modal de la cámara
  function closeCameraModal() {
    cameraModal.classList.add('hidden');
    document.body.classList.remove('overflow-hidden');
  }

  // Función para iniciar la captura de la cámara
  function startCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (mediaStream) {
        videoElement.srcObject = mediaStream;
        stream = mediaStream;
        sendingFrames = true; // Habilitar el envío de cuadros
        sendFramesToServer(); // Iniciar el envío de cuadros al servidor
      })
      .catch(function (err) {
        console.error('Error accessing the camera: ', err);
      });
  }

  // Función para detener la captura de la cámara
  function stopCamera() {
    if (stream) {
      let tracks = stream.getTracks();
      tracks.forEach(function (track) {
        track.stop();
      });
      videoElement.srcObject = null;
      stream = null; // Liberar la referencia al stream
    }
  }

  // Función para enviar los cuadros del video al servidor
  function sendFramesToServer() {
    const FPS = 30; // Cuadros por segundo
    const INTERVAL = 1000 / FPS; // Intervalo en milisegundos entre cuadros

    intervalId = setInterval(function () {
      // Verificar si ya se detuvo el envío de cuadros
      if (!sendingFrames || emotionDetected) {
        stopSendingFrames(); // Detener el envío de cuadros
        return;
      }

      // Captura el cuadro actual del video en el canvas
      canvasElement.getContext('2d').drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
      let imageData = canvasElement.toDataURL('image/jpeg'); // Convertir el cuadro a base64

      // Verificar si la imageData está vacía ('data:,')
      if (imageData === 'data:,') {
        console.log('No hay datos de imagen, deteniendo el envío de cuadros.');
        stopSendingFrames(); // Detener el envío de cuadros
        return;
      }

      // Envía el cuadro al servidor usando fetch API
      fetch('/detect_emotion', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken') // Obtener el token CSRF de las cookies
        },
        body: JSON.stringify({ image: imageData })
      })
        .then(response => response.json())
        .then(data => {
          // Manejar la respuesta del servidor
          console.log('Respuesta del servidor:', data);

          // Verificar si se detectó una emoción y almacenarla en localStorage
          if (data.emotions && data.emotions.length > 0) {
            console.log('Emoción detectada:', data.emotions[0].emotion);
            emotionDetected = data.emotions[0].emotion; // Almacenar la emoción detectada
            localStorage.setItem('detectedEmotion', emotionDetected); // Persistir en localStorage
            localStorage.setItem('list_music', JSON.stringify(data.songs)); // Persistir en localStorage
            localStorage.setItem('path_song', data.song_path)
            location.reload(); // Recargar la página para mostrar la nueva detección
          }
        })
        .catch(error => {
          console.error('Error al enviar cuadro al servidor:', error);
          stopSendingFrames(); // Detener el envío de cuadros en caso de error
        });
    }, INTERVAL);
  }

  // Función para detener el envío de cuadros
  function stopSendingFrames() {
    sendingFrames = false; // Marcar que no se enviarán más cuadros
    clearInterval(intervalId); // Detener el intervalo
    stopCamera(); // Detener la captura de la cámara
  }

  // Función para limpiar la sesión y reiniciar el proceso
  function clearSession() {
    localStorage.removeItem('detectedEmotion'); // Eliminar la emoción detectada del almacenamiento local
    localStorage.removeItem('list_music'); // Eliminar el array de canciones del almacenamiento local
    localStorage.removeItem('path_song'); // Eliminar la ruta de la canción del almacenamiento local
    emotionDetected = null;
    path_music = null;
    list_music = null;
    console.log('Sesión y valor de emoción eliminados. Reiniciando proceso.');
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
