document.addEventListener('DOMContentLoaded', filtering)

function filtering(){
    const checkbox_brand = document.querySelectorAll("input[name='check_brand']");
    const checkbox_category = document.querySelectorAll("input[name='check_category']");
    // console.log(checkbox_category);
    
    // console.log(checkbox_brand);
    for(var i =0; i < checkbox_brand.length; i++){
        checkbox_brand[i].addEventListener('change', filter_brand);
    };
    for(var i =0; i < checkbox_category.length; i++){
        checkbox_category[i].addEventListener('change', filter_category);
    };
};

function filter_brand(){
    const checked_brands = document.querySelectorAll('input[name="check_brand"]:checked');
    const search_params = new URLSearchParams(window.location.search);
    search_params.delete('brand');
    for (var i =0; i < checked_brands.length; i++){
        search_params.append('brand', checked_brands[i].value)
    };
    window.location.href = '?' + search_params.toString();
};


function filter_category(){
    const checked_categories = document.querySelectorAll('input[name="check_category"]:checked');
    console.log(checked_categories);
    
    const search_params = new URLSearchParams(window.location.search);
    search_params.delete('category');
    for (var i =0; i < checked_categories.length; i++){
        search_params.append('category', checked_categories[i].value)
    };
    window.location.href = '?' + search_params.toString();
};


const submit_price_filter = document.getElementById('submit_price_filter');
submit_price_filter.addEventListener('click', filter_by_price)

function filter_by_price(){
    const min_price = document.getElementById('min_price_filter').value;
    const max_price = document.getElementById('max_price_filter').value;
    const search_params = new URLSearchParams(window.location.search);
    search_params.delete('max_price');
    search_params.delete('min_price');
    search_params.append('min_price', min_price);
    search_params.append('max_price', max_price);
    window.location.href = '?' + search_params.toString();
}


const delete_price_filter = document.getElementById('delete_price_filter');
delete_price_filter.addEventListener('click', delete_filter_by_price)

function delete_filter_by_price(){
    const search_params = new URLSearchParams(window.location.search);
    search_params.delete('max_price');
    search_params.delete('min_price');
    window.location.href = '?' + search_params.toString();
}


const discounted_checkbox = document.getElementById('discounted');
discounted_checkbox.addEventListener('change', filter_discount)

function filter_discount(){
    const checked_discounted = document.getElementById('discounted');
    const search_params = new URLSearchParams(window.location.search);
    if (checked_discounted.checked == true){
        search_params.delete('discounted');
        search_params.append('discounted', 'on');
        window.location.href = '?' + search_params.toString();
    }else{
        search_params.delete('discounted');
        window.location.href = '?' + search_params.toString();
    }
};


function add_product_to_likes(id_product){
    let csrf_token = document.getElementById('#csrf_t');
    $.post('http://127.0.0.1:8000/likes/', {product_id:id_product, csrfmiddlewaretoken:csrf_token.value}, function(res){console.log(res);
    });
    
}