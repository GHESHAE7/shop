(function () {
    'use strict';

    var count = 60;
    var counter = setInterval(timer, 1000); //1000 will run it every 1 second

    function timer() {
        count = count - 1;
        if (count <= 0) {
            clearInterval(counter);
            document.getElementById("resendOTP").innerHTML = '<a class="resendOTP" href="">کد را دوباره ارسال کنید</a>';
        } else {
            document.getElementById("resendOTP").innerHTML = 'صبر کن ' + count + ' ثانیه ';
        }
    }
    
    $(".single-otp-input").keyup(function () {
        if (this.value.length == this.maxLength) {
            var $next = $(this).next('.single-otp-input');
            if ($next.length)
                $(this).next('.single-otp-input').focus();
            else
                $(this).blur();
        }
    });

})();