const appointmentDate = document.querySelector('#id_appointment_date');
const specialtyList = document.querySelector('#id_specialty');
const doctorList = document.querySelector('#id_doctor');
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


function getAppointmentsAvailable(specialty, appointmentDate) {
    
    // Check if one specialty was selected
    if (specialty == '' || isNaN(parseInt(specialty))) {
        return;
    }
    // Check if one appointment date was selected
    if (appointmentDate == '' || appointmentDate == undefined) {
        return;
    }

    // Sends a request to the django
    const url = '/appointment/appointments_available/';
    fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ 
            'specialty_id': `${parseInt(specialty)}`,
            'appointment_date': `${appointmentDate}`
        })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        if (data['status'] == 'warning' || data['status'] == 'error') {
            return;
        }
        const divAvailabilityInformation = document.querySelector('.right-panel');
        divAvailabilityInformation.textContent = '';

        const specialtyId = data['specialty_id'];
        const specialtyName = data['specialty_name'];

        for (const doctor of data['doctors']) {
            let doctorId = doctor['doctor_id'];
            let doctorName = doctor['doctor_name'];
            let doctorGender = doctor['doctor_gender'];
            let doctorCrm = doctor['doctor_crm'];
            let doctorState = doctor['doctor_state'];
            let selectedDate = doctor['selected_date'];

            const divDoctorAvailable = document.createElement('div');
            divDoctorAvailable.setAttribute('id', `doctor-id-${doctorId}`);
            divDoctorAvailable.setAttribute('data-doctor-id', doctorId);

            const pDoctorName = document.createElement('p');
            pDoctorName.textContent = doctorGender == 'm' ? `Dr. ${doctorName}` : `Dra. ${doctorName}`;
            pDoctorName.style.fontWeight = 700;

            const pDoctorSpecialty = document.createElement('p');
            pDoctorSpecialty.textContent = `${specialtyName} - CRM: ${doctorCrm}`;

            const ulDoctorAvailableList = document.createElement('ul');

            for (const time of doctor['available_times']) {
                const liAvailableTime = document.createElement('li');
                liAvailableTime.setAttribute('data-time-selected', 'false');
                liAvailableTime.style.padding = '10px';
                liAvailableTime.textContent = time;
                
                liAvailableTime.addEventListener('click', function() {
                    // Deselect another item if it exists
                    const selectedTime = this.parentElement.querySelector('[data-time-selected="true"]');
                    if (selectedTime != null || selectedTime != undefined) {
                        selectedTime.setAttribute('data-time-selected', 'false');
                    }
                    this.setAttribute('data-time-selected', 'true');
                });
                
                ulDoctorAvailableList.insertAdjacentElement('beforeend', liAvailableTime);
            }

            const btnRegister = document.createElement('button');
            btnRegister.setAttribute('type', 'button');
            btnRegister.setAttribute('id', `btn-doctor-id-${doctorId}`);
            btnRegister.textContent = 'Agendar';
            btnRegister.addEventListener('click', function() {
                const customer = document.querySelector("#id_customer").value;
                const specialty = document.querySelector("#id_specialty").value;
                const appointment_date = document.querySelector('#id_appointment_date').value 
                    ? document.querySelector('#id_appointment_date').value 
                    : formatDate(new Date());

                const doctor = this.parentElement.dataset.doctorId;
                const appointment_time = this.previousSibling.querySelector('[data-time-selected="true"]').textContent;
                console.log('Appointment time: ', appointment_time);

                insertAppointment(appointment_date, appointment_time, customer, specialty, doctor);
            });

            divDoctorAvailable.insertAdjacentElement('beforeend', pDoctorName);
            divDoctorAvailable.insertAdjacentElement('beforeend', pDoctorSpecialty);
            divDoctorAvailable.insertAdjacentElement('beforeend', ulDoctorAvailableList);
            divDoctorAvailable.insertAdjacentElement('beforeend', btnRegister);

            divAvailabilityInformation.insertAdjacentElement('beforeend', divDoctorAvailable);
        }
        
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


function formatDate(date) {
    const year = Intl.DateTimeFormat('pt-br', { year: 'numeric' }).format(date);
    const month = Intl.DateTimeFormat('pt-br', { month: '2-digit' }).format(date);
    const day = Intl.DateTimeFormat('pt-br', { day: '2-digit' }).format(date);

    return `${year}-${month}-${day}`;
}


specialtyList.addEventListener("change", function() {
        const selectedDate = appointmentDate.value ? appointmentDate.value : formatDate(new Date());
        
        getAppointmentsAvailable(this.value, selectedDate);
    }, false
);

appointmentDate.addEventListener("change", function() {
    const selectedSpecialty = specialtyList.value;

    if (selectedSpecialty == '' || selectedSpecialty == undefined) {
        return;
    }
    getAppointmentsAvailable(selectedSpecialty, this.value);
});