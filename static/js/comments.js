function send_comment(product_id){
    let csrf = document.getElementById('#csrf_t');
    let comment = document.getElementById('comments').value;
    let rating = document.getElementById('comment_rating');
    if(rating.value < 0 || rating.value > 5 || rating.value == '' || isFinite(rating.value) || isNaN(parseFloat(rating.value))){
        console.log('نمیتونی بزرگ تر از 5 یا کوچک تر از 0 انتخاب کنی یا خالی وارد کنی');
    }else{
        if (comment == ""){
            console.log('باید متن کامنت پر شود');
        }else{
            $.post('http://127.0.0.1:8000/comment/add', {product_id:product_id, csrfmiddlewaretoken:csrf.value, message:comment, rating:rating.value}, function(res){
                document.getElementById('list_comment').innerHTML = res;
                document.getElementById('comments').value = null;
                document.getElementById('comment_rating').value = null;
                // add alert
            });
        }
    }
}