function send_ajax_must(url, val){
    console.log(val);
    $.ajax({
        type: 'POST',
        url:url,
        data:{
            game_id:val,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
            alert('Game added to MUST!');
        }
    });
}
