function send_comment(){
    let csrf = document.getElementById('#csrf_t');
    let comment = document.getElementById('comments').value;
    let rating = document.getElementById('comment_rating');
    let product_id = document.getElementById('product_id_send_comment');
    if(parseInt(rating.value) < 0 || parseInt(rating.value) > 5 || parseInt(rating.value) == '' || isNaN((rating.value))){
        console.log('نمیتونی بزرگ تر از 5 یا کوچک تر از 0 انتخاب کنی یا خالی وارد کنی');
    }else{
        if (comment == ""){
            console.log('باید متن کامنت پر شود');
        }else{
            $.post('http://127.0.0.1:8000/comment/add', {product_id:parseInt(product_id.value), csrfmiddlewaretoken:csrf.value, message:comment, rating:rating.value}, function(res){
                if(res.status == 400 || res.status == 401 || res.status == 404){
                    console.log(res);
                }else{
                    document.getElementById('list_comment').innerHTML = res;
                    document.getElementById('comments').value = null;
                    document.getElementById('comment_rating').value = null;
                    // add alert
                }
            });
        }
    }
}