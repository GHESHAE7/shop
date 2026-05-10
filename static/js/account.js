document.addEventListener("DOMContentLoaded", function() {
    let elem = document.getElementById('id_captcha_1');
    elem.className = 'form-control';
    elem.placeholder = 'کپچا اینا وارد شود'
    })


$(function () {
    $('#refresh-captcha').on('click', function (e) {
        e.preventDefault();

        $.get('/captcha/refresh/', function (data) {

            $('.captcha').attr('src', data.image_url);

            $('input[name="captcha_0"]').val(data.key);

            $('input[name="captcha_1"]').val('');
        });
    });
});