const btnCancelList = document.querySelectorAll('.btn-cancel-appointment');

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function cancelAppointment(id){
    let url = '/customer/cancel_appointment/'

    fetch(url, {
        method: 'POST',

        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            'id': id
        })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log("sjflaksd")
        let btn = document.getElementById(id)
        btn.disabled = true
        btn.innerHTML = "Cancelado"
        btn.style.backgroundColor = "#b3cbff" 
    });
}


btnCancelList.forEach(function(currentBtn) {
    currentBtn.addEventListener('click', function() {
        cancelAppointment(this.dataset.appointmentId);
    });
});