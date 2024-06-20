        const video = document.getElementById('video');

    // Use navigator.mediaDevices.getUserMedia to access the webcam
    navigator.mediaDevices.getUserMedia({ video: {facingMode: "environment"} })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            console.error('Error accessing webcam:', err);
        });