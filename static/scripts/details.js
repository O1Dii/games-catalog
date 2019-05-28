function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

window.onload = function(){
    let users_rating = document.getElementById("users_rating_value").innerText;
    let users_green = 255 * (users_rating.substr(0, users_rating.indexOf(' ')) / 10 - 0.2);
    let users_red = 255;
    if(users_green < 0){
        users_green = 0;
    }
    else {
        users_red = 255 - users_green;
    }
    document.getElementById("users-rating").style.backgroundColor = rgbToHex(users_red, users_green, 0);

    let critics_rating = document.getElementById("critics_rating_value").innerText;
    let critics_green = 255 * (critics_rating.substr(0, critics_rating.indexOf(' ')) / 10 - 0.2);
    let critics_red = 255;
    if(critics_green < 0){
        critics_green = 0;
    }
    else {
        critics_red = 255 - critics_green;
    }
    document.getElementById("critics-rating").style.backgroundColor = rgbToHex(critics_red, critics_green,0);
};
