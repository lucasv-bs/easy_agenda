const specialty_list = document.querySelector('#id_specialty');
const doctor_list = document.querySelector('#id_doctor');
const btnRegisterAppointment = document.querySelector('#btn-register-appointment');


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


function getDoctorBySpecialty(specialty) {
    // Clean the doctor list
    doctor_list.textContent = '';
    
    // Check if one specialty was selected
    if (specialty == '' || isNaN(parseInt(specialty))) {
        return;
    }

    // Sends a request to the django
    url = '/appointment/doctor_by_specialty/'
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ 'specialty_id': `${parseInt(specialty)}` })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        if (data['status'] == 'warning' || data['status'] == 'error') {
            return;
        }

        // Insert a default option in the doctor list
        let option = document.createElement('option');
        option.value = "";
        option.textContent = "-----Select an option-----";
        doctor_list.append(option);

        // Fill the list doctor with the django response
        Object.keys(data).map(function(key) {
            let option = document.createElement('option');
            option.value = key;
            option.textContent = data[key];

            doctor_list.append(option);
        });
    });
}


function insertAppointment(appointment_date, appointment_time, customer, specialty, doctor) {
    console.log(appointment_date, appointment_time, customer, specialty, doctor);
    
    const url = '/appointment/employee_appointment/insert/'
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'customer_id': parseInt(customer),
            'specialty_id': parseInt(specialty),
            'doctor_id': parseInt(doctor)
        })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log(data);
    });
}


specialty_list.addEventListener("change", function() {
        getDoctorBySpecialty(this.value);
    }, false
);


btnRegisterAppointment.addEventListener("click", function() {
    const customer = document.querySelector("#id_customer").value;
    const specialty = document.querySelector("#id_specialty").value;
    const doctor = document.querySelector("#id_doctor").value;
    const appointment_date = document.querySelector("#id_appointment_date").value;
    const appointment_time = document.querySelector("#id_appointment_time").value;

    insertAppointment(appointment_date, appointment_time, customer, specialty, doctor);
},);