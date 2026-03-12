function delete_product_to_likes(id_like_product){
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/likes/delete', {like_product_id:id_like_product, csrfmiddlewaretoken:csrf_token.value}, function(res){
        console.log(res);
        window.location.reload();
    });
}

function add_product_to_likes(id_product){
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/likes/', {product_id:id_product, csrfmiddlewaretoken:csrf_token.value}, function(res){console.log(res);
    });
    
}