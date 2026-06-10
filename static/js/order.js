function remove_order_item(){
    let csrf_token = document.getElementById('#csrf_t');
    let order_item_id = document.getElementById('order_item_id');
    $.post('http://127.0.0.1:8000/order/remove-order-item', {order_item_id: order_item_id.value, csrfmiddlewaretoken: csrf_token.value}, function(res){
        if(res.icon == 'success'){
            
            if (res.icon == 'success'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#00920c',
                }).showToast(); 
            }else if (res.icon == 'info'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#0081cc',
                }).showToast();               
            }else if (res.icon == 'warning'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#ce7e15',
                }).showToast();  
            }else if (res.icon == 'error'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#c50000',
                }).showToast();                 
            }
            setTimeout(function() {
            window.location.reload();
            }, 1000);

        }else{
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
        }
    })
}



function change_count_order_item(input){
    let count_order_item = input;
    let order_item_id = document.getElementById('order_item_id');
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/order/change-count', {change_count: count_order_item.value, order_item_id: order_item_id.value, csrfmiddlewaretoken: csrf_token.value}, function(res){
        if(res.icon == 'info'){
                        if (res.icon == 'success'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#00920c',
                }).showToast(); 
            }else if (res.icon == 'info'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#0081cc',
                }).showToast();               
            }else if (res.icon == 'warning'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#ce7e15',
                }).showToast();  
            }else if (res.icon == 'error'){
                Toastify({
                    text: res.message,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#c50000',
                }).showToast();   

            }
                        setTimeout(function() {
            window.location.reload();
            }, 1000);
        }else{
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
        }
    })
}



function add_product_in_order(){
    let color = document.querySelector('input[name="colorRadio"]:checked') || null;
    let size = document.querySelector('input[name="sizeRadio"]:checked') || null;
    let number_count = document.getElementById('add_order_stock') || 0;
    let csrf = document.getElementById('#csrf_t');
    let product_id = document.getElementById('product_id_for_add_in_order');
    
    if(number_count.value <= 0){
                            Toastify({
                    text: 'تعداد باید بزرگ تر از 0 باشد',
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#0081cc',
                }).showToast();  
    }else{
        if (color != null && size != null){
        $.post('http://127.0.0.1:8000/order/add-product-to-order', {color_name:color.value, size_name:size.value, count: number_count.value, product_id:product_id.value, csrfmiddlewaretoken:csrf.value}, function(res){
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
        }else{
                            Toastify({
                    text: 'حتما باید سایز و رنگ خود را مشخص کنید',
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#ce7e15',
                }).showToast();  
        };
    }
}



function discount_code_send(order_id){
    let csrf = document.getElementById('#csrf_t').value;
    let discount_code = document.getElementById('discount_code').value.trim();
    if (discount_code == ""){
        Toastify({
            text: 'کد تخفیف را وارد کنید',
            duration: 3500,
            gravity: "top",
            position: "right",
            backgroundColor: '#0081cc',
        }).showToast();  
    }else {
        $.post('http://127.0.0.1:8000/order/discount_code', {csrfmiddlewaretoken: csrf, discount_code: discount_code, order_id: order_id}, function(res){
            if (res.icon == 'success'){
                Toastify({
                    text: res.message,
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#00920c',
                }).showToast();  
                setTimeout(function() {
                window.location.reload();
                }, 2000); 
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
        })
    }
    
}



function discount_code_delete(order_id, discount_code){
    let csrf = document.getElementById('#csrf_t').value;
    $.post('http://127.0.0.1:8000/order/discount_code_delete', {csrfmiddlewaretoken: csrf, discount_code: discount_code, order_id: order_id}, function(res){
            if (res.icon == 'success'){
                Toastify({
                    text: res.message,
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#00920c',
                }).showToast(); 
                setTimeout(function() {
                window.location.reload();
                }, 2000);
            }else if (res.icon == 'info'){
                Toastify({
                    text: res.message,
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#0081cc',
                }).showToast();  
                setTimeout(function() {
                window.location.reload();
                }, 2000);             
            }else if (res.icon == 'warning'){
                Toastify({
                    text: res.message,
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#ce7e15',
                }).showToast();  
                setTimeout(function() {
                window.location.reload();
                }, 2000);
            }else if (res.icon == 'error'){
                Toastify({
                    text: res.message,
                    duration: 3500,
                    gravity: "top",
                    position: "right",
                    backgroundColor: '#c50000',
                }).showToast();  
                setTimeout(function() {
                window.location.reload();
                }, 2000);                 
            }
        })
    
}



function payment_request(){
    let csrf_token = document.getElementById('#csrf_t');
    let total_price = document.getElementById('total_price');
    $.post('http://127.0.0.1:8000/order/payment/', {csrfmiddlewaretoken: csrf_token.value, total_price: total_price.innerHTML}, function(res){
        if (res.icon == 'warning'){
            div_warning = document.getElementById('warnings');
            div_warning.classList.remove('d-none');
            div_warning.style.display = 'block';
            div_warning.innerHTML = res.message;
            setTimeout(function() {
            window.location.reload();
            }, 4000);
        }else if(res.url){
            window.location.href = res.url;
        }
    });
}