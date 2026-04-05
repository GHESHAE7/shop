// document.addEventListener('DOMContentLoaded', stock);


// function stock(){
//     colors = document.getElementsByName('colorRadio');
//     sizes = document.getElementsByName('sizeRadio');

//     for(let i=0; i < colors.length; i++){
//         colors[i].addEventListener('click', get_stock);
//     }

//     for(let j=0; j < sizes.length; j++){
//         sizes[j].addEventListener('click', get_stock);
//     }
// }


function get_stock(product_id){
    let color = document.querySelector('input[name="colorRadio"]:checked') || null;
    let size = document.querySelector('input[name="sizeRadio"]:checked') || null;
    let csrf = document.getElementById('#csrf_t');
    
    if (color != null && size != null){
        $.post('http://127.0.0.1:8000/products/stock_by_color_size', {color_name:color.value, size_name:size.value, product_id:product_id, csrfmiddlewaretoken:csrf.value}, function(res){
            if(res.message){
                document.getElementById('stock_product').innerHTML = 'این رنگ و سایز برای این کفش وجود ندارد'
            }else{
                document.getElementById('stock_product').innerHTML = 'موجودی رنگ' + ' ' + res.color + ' ' + 'سایز' + ' ' + res.size + ' :' + ' ' + res.stock
            }
        });
    }else{
        console.log('NONOONONNONO');
    };
}