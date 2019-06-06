function send_ajax_must(url, val, add){
    console.log(val);
    $.ajax({
        type: 'POST',
        url:url,
        data:{
            game_id:val,
            add:add,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success:function(){
            alert('Game added to MUST!');
        }
    });
}

function hideDiv(self) {
    console.log(self);
    self.parentNode.parentNode.parentNode.parentNode.style.display = "none";
}