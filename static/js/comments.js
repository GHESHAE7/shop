function send_comment(){
    let csrf = document.getElementById('#csrf_t');
    let comment = document.getElementById('comments').value;
    let rating = document.getElementById('comment_rating');
    let product_id = document.getElementById('product_id_send_comment');
    if(parseInt(rating.value) < 0 || parseInt(rating.value) > 5 || parseInt(rating.value) == '' || isNaN((rating.value))){
        Swal.fire({
        icon: 'warning',
        title: 'امتیاز محصول باید بین 1 تا 5 باشد',
        timer: 3500,
        timerProgressBar: true,
        //position:'top-left'
        });
    }else{
        if (comment == ""){
            Swal.fire({
            icon: 'warning',
            title: 'متن کامنت باید حتما پر شود',
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            });
        }else{
            $.post('http://127.0.0.1:8000/comment/add', {product_id:parseInt(product_id.value), csrfmiddlewaretoken:csrf.value, message:comment, rating:rating.value}, function(res){
                if(res.icon == 'warning' || res.icon == 'error' || res.icon == 'info'){
                        Swal.fire({
                            icon: res.icon,
                            title: res.message,
                            timer: 3500,
                            timerProgressBar: true,
                            //position:'top-left'
                        });
                }else{
                    document.getElementById('list_comment').innerHTML = res;
                    document.getElementById('comments').value = null;
                    document.getElementById('comment_rating').value = null;
                    Swal.fire({
                        icon: 'success',
                        title: 'کامنت شما با موفقیت ثبت شد و پس از بررسی نمایش داده می شود',
                        timer: 3500,
                        timerProgressBar: true,
                        //position:'top-left'
                    });
                }
            });
        }
    }
}