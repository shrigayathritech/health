document.getElementById('treatment-form').addEventListener('submit', function(e) {
    e.preventDefault(); 
    const age = document.getElementById('age').value;
    const bloodPressure = document.getElementById('blood_pressure').value;
    const cholesterol = document.getElementById('cholesterol').value;
    const heartRate = document.getElementById('heart_rate').value;
    const treatmentDuration = document.getElementById('treatment_duration').value;

    fetch('/get_treatment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            age: age,
            blood_pressure: bloodPressure,
            cholesterol: cholesterol,
            heart_rate: heartRate,
            treatment_duration: treatmentDuration
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('treatment-output').textContent = data.error;
        } else {
            document.getElementById('treatment-output').textContent = `
                Age: ${data.age}
                Blood Pressure: ${data.blood_pressure}
                Cholesterol: ${data.cholesterol}
                Heart Rate: ${data.heart_rate}
                Treatment Duration: ${data.treatment_duration} days
                KMeans Cluster: ${data.kmeans_cluster}
                GMM Cluster: ${data.gmm_cluster}
                Personalized Treatment: ${data.personalized_treatment}
            `;
        }
        document.getElementById('result').style.display = 'block'; 
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('treatment-output').textContent = "An error occurred. Please try again.";
    });
});
