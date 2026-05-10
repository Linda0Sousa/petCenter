//this is for the landing page forms

window.addEventListener('DOMContentLoaded', function() {
    document.getElementById('signup-btn').addEventListener('click', function(event) {
        event.preventDefault(); 
        document.getElementById('signup-form').style.display = 'block';
        document.getElementById('landing-page').style.display = 'none';
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('verify-number').style.display = 'none';
        document.getElementById('verify-email').style.display = 'none';
    });

});

//this is for the pet creation page

//profile image upload and preview
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("profile-image");
    const previewContainer = document.querySelector(".main-img");
    const uploadArea = document.getElementById("upload-area");
    const selectImageLabel = document.getElementById("select-image");

    uploadArea.addEventListener("click", () => {
        input.click();
    });

    input.addEventListener("change", (event) => {
        const file = event.target.files[0];

        if (file) {
            const imageUrl = URL.createObjectURL(file);

            previewContainer.style.backgroundImage = `url(${imageUrl})`;
            previewContainer.style.backgroundSize = "cover";
            previewContainer.style.backgroundPosition = "center";
            selectImageLabel.style.display = "none";

        }
    });
});

//multi image upload and preview
document.addEventListener("DOMContentLoaded", () => {

    for (let i = 1; i <= 6; i++) {
        const input = document.getElementById(`profile-image-${i}`);
        const label = document.getElementById(`select-image-${i}`);
        const photoDiv = document.getElementById(`photos-div-${i}`);

        if (!input || !label || !photoDiv) continue;

        label.addEventListener("click", () => {
            input.click();
        });

        input.addEventListener("change", (event) => {
            const file = event.target.files[0];

            if (file) {
                const imageUrl = URL.createObjectURL(file);

                photoDiv.style.backgroundImage = `url(${imageUrl})`;
                photoDiv.style.backgroundSize = "cover";
                photoDiv.style.backgroundPosition = "center";

                
                label.style.display = "none";
            }
        });
    }

});