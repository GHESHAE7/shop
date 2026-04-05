function remove_order_item(order_item_id){
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/order/', {order_item_id: order_item_id, csrfmiddlewaretoken: csrf_token.value}, function(res){
        if(res.delete == true){
            location.reload();
        }else{
            console.log(res);
        }
    })
}


function change_count_order_item(order_item_id, input){
    let count_order_item = input;
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/order/', {change_count: count_order_item.value, order_item_id: order_item_id, csrfmiddlewaretoken: csrf_token.value}, function(res){
        console.log(res);
    })
}


function add_product_in_order(product_id){
    let color = document.querySelector('input[name="colorRadio"]:checked') || null;
    let size = document.querySelector('input[name="sizeRadio"]:checked') || null;
    let number_count = document.getElementById('add_order_stock') || 0;
    let csrf = document.getElementById('#csrf_t');
    
    if(number_count.value <= 0){
        console.log('تعداد باید بزرگ از تر 0 باشد');
    }else{
        if (color != null && size != null){
        $.post('http://127.0.0.1:8000/order/', {color_name:color.value, size_name:size.value, count: number_count.value, product_id:product_id, csrfmiddlewaretoken:csrf.value}, function(res){
            console.log(res);
        });
        }else{
        console.log('NONOONONNONO');
        };
    }
}