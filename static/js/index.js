const EnglishBtn = document.getElementById('English');
const ArabicBtn = document.getElementById('Arabic');

EnglishBtn.addEventListener('click', () => {
    EnglishBtn.classList.add('selected_btn');
    ArabicBtn.classList.remove('selected_btn');
});

ArabicBtn.addEventListener('click', () => {
    ArabicBtn.classList.add('selected_btn');
    EnglishBtn.classList.remove('selected_btn');
});


function emailGiftSendRequest() {
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

    let headers = {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
        'X-CSRFToken': csrftoken,
    }

    const userEmail = document.getElementById('email').value
    const emailinput = document.getElementById('email')
    const email = emailinput.value;

    fetch('', {
        method: 'post',
        credentials: 'include',
        headers,
        body: JSON.stringify({
            userEmail
        })

    }).then(response => {


        response.json().then(res => {
            if (res.status === 'errorEmail') {
                const Toast = Swal.mixin({
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 5000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });
                Toast.fire({
                    icon: res.icon,
                    title: res.message
                });
                 email.value = '';
            }

            if (res.status === 'existEmail') {
                const Toast = Swal.mixin({
                    toast: true,
                    position: "top-end",
                    showConfirmButton: false,
                    timer: 5000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.onmouseenter = Swal.stopTimer;
                        toast.onmouseleave = Swal.resumeTimer;
                    }
                });
                Toast.fire({
                    icon: res.icon,
                    title: res.message
                });
                 email.value = '';
            }

            if (res.status === 'success') {
                Swal.fire({
                    icon: "success",
                    title: `your code is ${res.code}`,
                    text: "copy your gift cod it will not show you again!",

                });
                 email.value = '';
            }

        })
    })


}






