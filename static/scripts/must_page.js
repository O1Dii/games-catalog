function send_ajax_must(url, val, add){
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
    if(self.innerHTML.includes("UnMUST")){
        self.innerHTML = self.innerHTML.replace("UnMUST", "ReMUST");
        self.style.backgroundColor = "green";
        self.style.borderColor = "green";
    }
    else{
        self.innerHTML = self.innerHTML.replace("MUST", "UnMUST");
        self.innerHTML = self.innerHTML.replace("Re", "");
        self.style.backgroundColor = "red";
        self.style.borderColor = "red";
    }
}

function changeAdded(self, game_id) {
    let element = document.getElementById("added_" + game_id);
    let split = element.innerHTML.split(' ');
    if(self.innerHTML.includes("UnMUST")){
        split.push(Number(split.pop()) + 1);
        element.innerHTML = split.join(' ');
    }
    else{
        split.push(Number(split.pop()) - 1);
        element.innerHTML = split.join(' ');
    }
}