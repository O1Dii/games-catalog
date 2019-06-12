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
    if(self.innerHTML.includes("UnMUST")){
        console.log(1);
        self.innerHTML = self.innerHTML.replace("UnMUST", "ReMUST");
        self.style.backgroundColor = "green";
        self.style.borderColor = "green";
    }
    else{
        console.log(2);
        self.innerHTML = self.innerHTML.replace("MUST", "UnMUST");
        console.log(self.innerHTML);
        self.innerHTML = self.innerHTML.replace("Re", "");
        console.log(self.innerHTML);
        self.style.backgroundColor = "red";
        self.style.borderColor = "red";
    }
}