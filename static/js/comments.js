function send_comment(){
    let csrf = document.getElementById('#csrf_t');
    let comment = document.getElementById('comments').value;
    let rating = document.getElementById('comment_rating');
    let product_id = document.getElementById('product_id_send_comment');
    if(parseInt(rating.value) < 0 || parseInt(rating.value) > 5 || parseInt(rating.value) == '' || isNaN((rating.value))){
            Toastify({
              text: 'امتیاز محصول باید بین 1 تا 5 باشد',
              duration: 3500,
              gravity: "top",
              position: "right",
              backgroundColor: '#ce7e15',
          }).showToast();
    }else{
        if (comment == ""){
            Toastify({
              text: 'متن کامنت باید حتما پر شود',
              duration: 3500,
              gravity: "top",
              position: "right",
              backgroundColor: '#ce7e15',
          }).showToast();
        }else{
            $.post('http://127.0.0.1:8000/comment/add', {product_id:parseInt(product_id.value), csrfmiddlewaretoken:csrf.value, message:comment, rating:rating.value}, function(res){
                if(res.icon == 'warning' || res.icon == 'error' || res.icon == 'info'){
                    if (res.icon == 'info'){
                        Toastify({
                            text: res.message,
                            duration: 3500,
                            gravity: "top",
                            position: "right",
                            backgroundColor: '#0081cc',
                        }).showToast();               
                    }else if (res.icon == 'warning'){
                        Toastify({
                            text: res.message,
                            duration: 3500,
                            gravity: "top",
                            position: "right",
                            backgroundColor: '#ce7e15',
                        }).showToast();  
                    }else if (res.icon == 'error'){
                        Toastify({
                            text: res.message,
                            duration: 3500,
                            gravity: "top",
                            position: "right",
                            backgroundColor: '#c50000',
                        }).showToast();                 
                    }
                }else{
                    document.getElementById('list_comment').innerHTML = res;
                    document.getElementById('comments').value = null;
                    document.getElementById('comment_rating').value = null;
                    Toastify({
                            text: 'کامنت شما با موفقیت ثبت شد و پس از بررسی نمایش داده می شود',
                            duration: 3500,
                            gravity: "top",
                            position: "right",
                            backgroundColor: '#00920c',
                    }).showToast();
                }
            });
        }
    }
}