const edit = document.getElementById('edit');
const inputs = document.querySelectorAll('.input');
const info = document.querySelectorAll('.info');
const save = document.getElementById('save');
const cancel = document.getElementById('close');

edit.addEventListener('click', function() {
    console.log('Edit button clicked');

    //hiding and showing the inputs and the info
    inputs.forEach(function(input) {
        input.style.display = 'block';
    });

    info.forEach(function(paragraph) {
        paragraph.style.display = 'none';
    });

    //hiding the edit button and showing the save button
    edit.style.display = 'none';
    save.style.display = 'block';
    cancel.style.display = 'block';

    //canceling the edit mode
    cancel.addEventListener('click', function() {
        console.log('Cancel button clicked');

        //hiding the inputs and showing the info
        inputs.forEach(function(input) {
            input.style.display = 'none';
        });

        info.forEach(function(paragraph) {
            paragraph.style.display = 'block';
        });

        //hiding the save and cancel buttons and showing the edit button
        save.style.display = 'none';
        cancel.style.display = 'none';
        edit.style.display = 'block';
    });


    //saving the changes
    save.addEventListener('click', function() {

    const email = document.getElementById("input-email").value;
    const phone = document.getElementById("input-phone").value;

    const csrftoken = document.cookie.match(/csrftoken=([^;]+)/)?.[1];

    fetch("/profile/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ email, phone })
    })
    .then(async response => {

        const data = await response.json();

        if (!response.ok) {
            console.log("Erro:", data.errors);
            return;
        }

        console.log("Sucesso:", data);

    })
    .catch(error => {
        console.error("Erro de rede:", error);
    });
});

});