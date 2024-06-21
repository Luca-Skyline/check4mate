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
    // Function to get the CSRF token from the cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Get access to the camera
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            var video = document.getElementById('video');
            video.srcObject = stream;
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
        var imageData = canvas.toDataURL('image/png');

        // Get CSRF token
        var csrftoken = getCookie('csrftoken');

        // Send the image data to the server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/save_image/', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                var response = JSON.parse(xhr.responseText);
                alert(response.message);
            }
        };
        xhr.send('image_data=' + encodeURIComponent(imageData));
    });
});