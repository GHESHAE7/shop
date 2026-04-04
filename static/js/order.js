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