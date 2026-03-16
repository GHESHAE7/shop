document.getElementById('send_message').addEventListener('click', send_message_to_server)


function send_message_to_server(){
    let fl_name = document.getElementById('fl_name').value
    let email = document.getElementById('email').value
    let subject = document.getElementById('topicSelect').value
    let message = document.getElementById('message').value
    let csrf = document.getElementById('#csrf_t').value
    if(fl_name == '' | subject == '' | email == '' | message == ''){
        console.log('باید پر شود');
    }else{
        $.post('http://127.0.0.1:8000/contact/', {fl_name: fl_name, email: email, subject: subject, message: message, csrfmiddlewaretoken: csrf}, function(res){
            console.log(res);
            document.getElementById('fl_name').value = null;
            document.getElementById('email').value = null;
            document.getElementById('message').value = null;
        })
    }
}