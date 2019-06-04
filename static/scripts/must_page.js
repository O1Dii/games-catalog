$(document).on('submit', '.must_send_form', function (e) {
    e.preventDefault();
    console.log(e);
    $.ajax({
        type: 'POST',
        url:'/main_page',
        data:{
            game_id:1,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
            alert('Game added to MUST!');
        }
    });
});
