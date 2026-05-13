function intcomma(value) {
  const num = typeof value === "string" ? Number(value) : value;
  if (!Number.isFinite(num)) return "";

  return new Intl.NumberFormat("en-US").format(num);
}



function get_stock(product_id){
    let color = document.querySelector('input[name="colorRadio"]:checked') || null;
    let size = document.querySelector('input[name="sizeRadio"]:checked') || null;
    let csrf = document.getElementById('#csrf_t');
    
    if (color != null && size != null){
        $.post('http://127.0.0.1:8000/products/stock_by_color_size', {color_name:color.value, size_name:size.value, product_id:product_id, csrfmiddlewaretoken:csrf.value}, function(res){
            if(res.message){
                document.getElementById('all_stock_product_').innerHTML = 'این رنگ و سایز برای این کفش وجود ندارد';
                document.getElementById('price_product').innerHTML = null;
            }else{
                document.getElementById('all_stock_product_').innerHTML = 'موجودی رنگ' + ' ' + res.color + ' ' + 'سایز' + ' ' + res.size + ' :' + ' ' + res.stock;
                if(res.discount > 0){
                    document.getElementById('price_product').innerHTML = 'قیمت با ' + res.discount + '%' + ' تخفیف: ' + intcomma(res.price);
                }else{
                    document.getElementById('price_product').innerHTML = 'قیمت: ' + intcomma(res.price);
                }
            }
        });
    }else{
        Toastify({
            text: 'سایز و رنگ کفش انتخاب باید کنید تا موجودی نمایش داده شود',
            duration: 3500,
            gravity: "top",
            position: "right",
            backgroundColor: '#0081cc',
        }).showToast();   
    };
}