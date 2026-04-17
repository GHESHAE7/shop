function remove_order_item(){
    let csrf_token = document.getElementById('#csrf_t');
    let order_item_id = document.getElementById('order_item_id');
    $.post('http://127.0.0.1:8000/order/remove-order-item', {order_item_id: order_item_id.value, csrfmiddlewaretoken: csrf_token.value}, function(res){
        if(res.icon == 'success'){
            Swal.fire({
            icon: res.icon,
            title: res.message,
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            }).then(() => {
                location.reload();
            });
        }else{
            Swal.fire({
            icon: res.icon,
            title: res.message,
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            }); 
        }
    })
}



function change_count_order_item(input){
    let count_order_item = input;
    let order_item_id = document.getElementById('order_item_id');
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/order/change-count', {change_count: count_order_item.value, order_item_id: order_item_id.value, csrfmiddlewaretoken: csrf_token.value}, function(res){
        if(res.icon == 'info'){
            Swal.fire({
            icon: res.icon,
            title: res.message,
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            }).then(() => {
                location.reload();
            });
        }else{
            Swal.fire({
            icon: res.icon,
            title: res.message,
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            }); 
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
            Swal.fire({
            icon: 'info',
            title: 'تعداد باید بزرگ تر از 0 باشد',
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            });
    }else{
        if (color != null && size != null){
        $.post('http://127.0.0.1:8000/order/add-product-to-order', {color_name:color.value, size_name:size.value, count: number_count.value, product_id:product_id.value, csrfmiddlewaretoken:csrf.value}, function(res){
            Swal.fire({
            icon: res.icon,
            title: res.message,
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            });
        });
        }else{
            Swal.fire({
            icon: 'warning',
            title: 'حتما باید سایز و رنگ خود را مشخص کنید',
            timer: 3500,
            timerProgressBar: true,
            //position:'top-left'
            });
        };
    }
}