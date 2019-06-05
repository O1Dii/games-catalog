function send_ajax_must(val){
    console.log(val);
    $.ajax({
        type: 'POST',
        url:'/',
        data:{
            game_id:val,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
            alert('Game added to MUST!');
        }
    });
}
