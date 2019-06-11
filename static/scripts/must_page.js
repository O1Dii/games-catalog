function send_ajax_must(url, val, add){
    console.log(val);
    $.ajax({
        type: 'POST',
        url:url,
        data:{
            game_id:val,
            add:add,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        }
    });
}

function changeDiv(self) {
    console.log(self, self.innerHTML);
    if(self.innerHTML[0] == "U"){
        self.innerHTML = "ReMUST";
        self.style.backgroundColor = "green";
        self.style.borderColor = "green";
    }
    else{
        self.innerHTML = "UnMUST";
        self.style.backgroundColor = "red";
        self.style.borderColor = "red";
    }
}