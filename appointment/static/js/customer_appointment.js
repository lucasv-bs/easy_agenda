const appointmentDate = document.querySelector('#id_appointment_date');
const specialtyList = document.querySelector('#id_specialty');
const doctorList = document.querySelector('#id_doctor');
const divAvailabilityInformation = document.querySelector('.right-panel');
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


function clearAvailabilityInformation() {
    divAvailabilityInformation.textContent = '';
}


function getAppointmentsAvailable(specialty, appointmentDate) {
    
    // Check if one specialty was selected
    if (specialty == '' || isNaN(parseInt(specialty))) {
        divAvailabilityInformation.textContent = '';
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
        clearAvailabilityInformation();

        const pSelectedDayResults = document.createElement('p');
        pSelectedDayResults.setAttribute('id', 'selected-day-results');

        // get the selected date to fill in the day results message
        let selectedDate = document.querySelector('#id_appointment_date').value;
        if (selectedDate == "") {
            selectedDate = formatDate(new Date(), true);
        }
        else {            
            // replace '-' for '/' on the string date
            let regexp = /-/gi;
            selectedDate = selectedDate.replace(regexp, '/');            
            selectedDate = formatDate(new Date(selectedDate), true);
        }
        if ( data['doctors'] == undefined || !Array.isArray(data['doctors']) ) {
            pSelectedDayResults.textContent = `Não há disponibilidade para as opções selecionadas`;
            divAvailabilityInformation.insertAdjacentElement('beforeend', pSelectedDayResults);
            
            return;
        }
        pSelectedDayResults.textContent = `Resultados para o dia ${selectedDate}`;
        divAvailabilityInformation.insertAdjacentElement('beforeend', pSelectedDayResults);

        const specialtyId = data['specialty_id'];
        const specialtyName = data['specialty_name'];

        // generate the panel with the availability data
        for (const doctor of data['doctors']) {
            let doctorId = doctor['doctor_id'];
            let doctorName = doctor['doctor_name'];
            let doctorGender = doctor['doctor_gender'];
            let doctorCrm = doctor['doctor_crm'];
            let doctorState = doctor['doctor_state'];

            // generate the HTML elements of the panel
            const divDoctorAvailable = document.createElement('div');
            divDoctorAvailable.setAttribute('id', `doctor-id-${doctorId}`);
            divDoctorAvailable.setAttribute('class', 'doctor');
            divDoctorAvailable.setAttribute('data-doctor-id', doctorId);

            const pDoctorName = document.createElement('p');
            pDoctorName.textContent = doctorGender == 'm' ? `Dr. ${doctorName}` : `Dra. ${doctorName}`;
            pDoctorName.setAttribute('class', 'doctor-name');

            const pDoctorSpecialty = document.createElement('p');
            pDoctorSpecialty.textContent = `${specialtyName} - CRM: ${doctorCrm}`;
            pDoctorSpecialty.setAttribute('class', 'doctor-specialty');

            const ulDoctorAvailableList = document.createElement('ul');
            ulDoctorAvailableList.setAttribute('class', 'doctor-time-list');

            // generate the available time list
            for (const time of doctor['available_times']) {
                const liAvailableTime = document.createElement('li');
                liAvailableTime.setAttribute('class', 'doctor-time-available');
                liAvailableTime.setAttribute('data-time-selected', 'false');                
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
            btnRegister.setAttribute('class', 'btn-register-appointment');
            btnRegister.textContent = 'Agendar';
            
            btnRegister.addEventListener('click', function() {
                if (!validateFields(this)) {
                    return;
                }

                // get the filled values
                const customer = -1;
                const specialty = document.querySelector("#id_specialty").value;
                const appointment_date = document.querySelector('#id_appointment_date').value 
                    ? document.querySelector('#id_appointment_date').value 
                    : formatDate(new Date());
                const appointment_return = 'false';

                const doctor = this.parentElement.dataset.doctorId;
                const appointment_time = this.previousSibling.querySelector('[data-time-selected="true"]').textContent;

                insertAppointment(appointment_date, appointment_time, customer, specialty, doctor, appointment_return);
            });

            divDoctorAvailable.insertAdjacentElement('beforeend', pDoctorName);
            divDoctorAvailable.insertAdjacentElement('beforeend', pDoctorSpecialty);
            divDoctorAvailable.insertAdjacentElement('beforeend', ulDoctorAvailableList);
            divDoctorAvailable.insertAdjacentElement('beforeend', btnRegister);

            divAvailabilityInformation.insertAdjacentElement('beforeend', divDoctorAvailable);
        }
        
    });
}


function validateFields(registerButtonClicked) {
    const specialty = document.querySelector("#id_specialty").value;
    
    const doctor = registerButtonClicked.parentElement.dataset.doctorId;
    const appointmentTime = registerButtonClicked.previousSibling.querySelector('[data-time-selected="true"]');

    if (specialty == undefined || specialty == null || specialty == "") {
        alert("Por favor, selecione uma especialidade");
        return false;
    }
    if (doctor == undefined || doctor == null || doctor == "") {
        alert("Por favor, informe selecione um médico");
        return false;
    }
    if (appointmentTime == undefined || appointmentTime == null || appointmentTime == "") {
        alert("Por favor, selecione um horário disponível");
        return false;
    }

    return true;
}


function insertAppointment(appointment_date, appointment_time, customer, specialty, doctor, 
        appointment_return) {

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
            'customer_id': customer,
            'specialty_id': parseInt(specialty),
            'doctor_id': parseInt(doctor),
            'appointment_return': (appointment_return === 'true')
        })
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        if (data['status'] == 'success') {
            alert('Agendamento registrado com sucesso!');
        }
        if (data['status'] == 'error' && data['error-code-text'] == 'duplicate') {
            alert('Atenção: Você já fez um agendamento dessa especialidade para a data selecionada');
        }
    });
}


function formatDate(date, formatForView = false) {
    const year = Intl.DateTimeFormat('pt-br', { year: 'numeric' }).format(date);
    const month = Intl.DateTimeFormat('pt-br', { month: '2-digit' }).format(date);
    const day = Intl.DateTimeFormat('pt-br', { day: '2-digit' }).format(date);

    if (formatForView) {
        return `${day}/${month}/${year}`;
    }
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