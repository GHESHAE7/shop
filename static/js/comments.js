function send_comment(product_id){
    let csrf = document.getElementById('#csrf_t')
    let comment = document.getElementById('comments').value
    if (comment == ""){
        console.log('باید متن کامنت پر شود');
    }else{
        $.post('http://127.0.0.1:8000/comment/add', {product_id:product_id, csrfmiddlewaretoken:csrf.value, message:comment}, function(res){
            document.getElementById('list_comment').innerHTML = res;
            document.getElementById('comments').value = null;
            // add alert
        });
    }
}