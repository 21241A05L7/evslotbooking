// static/myapp/location.js

// CSRF token function
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
const csrftoken = getCookie('csrftoken');

// Function to get location and send it to the backend
function getLocationAndSend() {
    // Check if Geolocation is supported
    if (navigator.geolocation) {
        // Request the user's location
        navigator.geolocation.getCurrentPosition(function(position) {
            // Extract latitude and longitude from the position object
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            console.log(`Latitude: ${lat}, Longitude: ${lon}`); // Debugging message

            // Send the coordinates to the backend
            fetch('/save_user_location/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({latitude: lat, longitude: lon})
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                alert('Location saved successfully.');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving location.');
            });
        }, function(error) {
            console.error('Error occurred while retrieving location:', error);
            alert('Unable to retrieve your location.');
        });
    } else {
        alert('Geolocation is not supported by your browser.');
    }
}

// Attach event listener to the button
document.getElementById('getLocationBtn').addEventListener('click', getLocationAndSend);
