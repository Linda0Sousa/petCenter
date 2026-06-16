const edit = document.getElementById('edit');
const inputs = document.querySelectorAll('.input');
const info = document.querySelectorAll('.info');
const save = document.getElementById('save');
const cancel = document.getElementById('close');

const toggleInputs = function(editing) {

    inputs.forEach(input => {
        input.style.display = editing ? 'block' : 'none';
    });

    info.forEach(paragraph => {
        paragraph.style.display = editing ? 'none' : 'block';
    });

    edit.style.display = editing ? 'none' : 'block';
    save.style.display = editing ? 'block' : 'none';
    cancel.style.display = editing ? 'block' : 'none';
}


edit.addEventListener('click', function() {
    console.log('Edit button clicked');

    //hiding and showing the inputs and the info
    toggleInputs(true);

});

//canceling the edit mode
cancel.addEventListener('click', function() {
    console.log('Cancel button clicked');

    toggleInputs(false);
});


//saving the changes
save.addEventListener('click', function() {

    const email = document.getElementById("input-email").value;
    const phone = document.getElementById("input-phone").value;

    const csrftoken = document.cookie.match(/csrftoken=([^;]+)/)?.[1];

    save.disabled = true;

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

        toggleInputs(false);
        //change the info displayed with the new values
        document.getElementById("email-info").textContent = email;
        document.getElementById("phone-info").textContent = phone;

    })
    .catch(error => {
        console.error("Erro de rede:", error);
    })
    .finally(() => {
        save.disabled = false;
    });
        

});
