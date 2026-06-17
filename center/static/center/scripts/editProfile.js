const edit = document.getElementById('edit');
const inputs = document.querySelectorAll('.input');
const info = document.querySelectorAll('.info');
const save = document.getElementById('save');
const cancel = document.getElementById('close');
const errors = document.querySelectorAll(".error");

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

    //hiding and showing the inputs and the info
    toggleInputs(true);

});

//canceling the edit mode
cancel.addEventListener('click', function() {
    errors.forEach(element => {
        element.style.display = 'none';
    });

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
            
            document.getElementById("email-error").textContent = "";
            document.getElementById("phone-error").textContent = "";

             if (data.errors.email) {
                document.getElementById("email-error").textContent = data.errors.email[0];
                document.getElementById("email-error").style.display = "block"

            }

            if (data.errors.phone_number) {
                document.getElementById("phone-error").textContent = data.errors.phone_number[0];
                document.getElementById("phone-error").style.display = "block"
            }

            return;
        }
        
        console.log("Sucesso:", data);

        toggleInputs(false);
        errors.forEach(element => {
            element.style.display = 'none';
        });
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
