//const video = document.getElementById('video');
//const button = document.getElementById('cambutton');
//
//// Use navigator.mediaDevices.getUserMedia to access the webcam
//navigator.mediaDevices.getUserMedia({ video: {facingMode: "environment"} })
//    .then(stream => {
//        video.srcObject = stream;
//    })
//    .catch(err => {
//        console.error('Error accessing webcam:', err);
//    });
//
document.addEventListener('DOMContentLoaded', function() {

    // Get access to the camera
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }})
        .then(function (stream) {
            var video = document.getElementById('video');
            video.srcObject = stream;
            video.playsInline = true;
            video.play();
        })
        .catch(function (error) {
            console.error("Error accessing the camera: ", error);
        });

    document.getElementById('captureButton').addEventListener('click', function () {
        var video = document.getElementById('video');
        var canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
          canvas.toBlob(function(blob) {
            const formData = new FormData();
            formData.append('image', blob, 'capture.png');

            fetch('/save_image/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken') // Ensure CSRF token is sent
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/analysis/';
                } else {
                    console.error('Image save failed:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }, 'image/png');
    });

     function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
     }
});