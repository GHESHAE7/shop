function delete_product_to_likes(id_like_product){
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/likes/delete', {like_product_id:id_like_product, csrfmiddlewaretoken:csrf_token.value}, function(res){
                    if (res.icon == 'success'){
                Toastify({
                    text: res.message,
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#00920c',
                }).showToast(); 
            }else if (res.icon == 'info'){
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
            setTimeout(function() {
            window.location.reload();
            }, 1000);
    });
}

function add_product_to_likes(id_product){
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/likes/', {product_id:id_product, csrfmiddlewaretoken:csrf_token.value}, function(res){
            if (res.icon == 'success'){
                Toastify({
                    text: res.message,
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#00920c',
                }).showToast(); 
            }else if (res.icon == 'info'){
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
    });
}