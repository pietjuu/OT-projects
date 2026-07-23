function update(){

fetch("/status/")
.then(r=>r.json())
.then(data=>{

document.getElementById("level").innerHTML=data.niveau+" %";

document.getElementById("valve").innerHTML=data.klep_hoek+" °";

document.getElementById("pump").innerHTML=data.pomp_aan ? "ON":"OFF";

});

}

setInterval(update,500);

update();

function pumpOn(){

fetch("/pump/on/",{

method:"POST",

headers:{

'X-CSRFToken':getCookie('csrftoken')

}

});

}

function pumpOff(){

fetch("/pump/off/",{

method:"POST",

headers:{

'X-CSRFToken':getCookie('csrftoken')

}

});

}

function moveValve(v){

fetch("/valve/"+v+"/",{

method:"POST",

headers:{

'X-CSRFToken':getCookie('csrftoken')

}

});

}

function getCookie(name){

let cookieValue = null;

if(document.cookie){

const cookies = document.cookie.split(';');

for(let cookie of cookies){

cookie=cookie.trim();

if(cookie.startsWith(name+'=')){

cookieValue=decodeURIComponent(cookie.substring(name.length+1));

break;

}

}

}

return cookieValue;

}