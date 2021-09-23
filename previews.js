document.addEventListener('DOMContentLoaded', init, false);


function init(){
  let chicken_run = document.querySelector("#chicken_run");
  let space_invaders = document.querySelector("#space_invaders");
  chicken_run.addEventListener("mouseover", start_cr, false);
  space_invaders.addEventListener("mouseover", start_si, false);
  chicken_run.addEventListener("mouseout", stop_cr, false);
  space_invaders.addEventListener("mouseout", stop_si, false);
}

function start_cr(){
  chicken_run.play();
}
function start_si(){
  space_invaders.play();
}

function stop_cr(){
  chicken_run.load();
}
function stop_si(){
  space_invaders.load();
}
