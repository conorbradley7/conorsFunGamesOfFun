let context;
let canvas;
let width;
let height;
let player;
let enemies = [];
let alien_speed = 1;
let score = 0;
let moveRight = false;
let moveLeft = false;
let intervalId;
let missiles = [];
let shooting = false;
let joey = new Image();
let ship = new Image();
let shot_image = new Image();
let end_link;
let scoreboard;

//document.addEventListener("DOMContentLoaded", start)
document.getElementById("startBtn").addEventListener("click", init, false);
// *****************************************************************************

function init(){
  document.getElementById("startBtn").style.display = "none";
  canvas = document.querySelector('canvas');
  context = canvas.getContext('2d');
  width = canvas.width;
  height = canvas.height;
  player = {
    x: width/2 - 25,
    y: height - 120,
    length: 50,
    width: 10
  };
  context.drawImage(ship, player.x, player.y);
  joey.src = "../media/joey_alien.png";
  ship.src = "../media/space_inv_ship.png"
  shot_image.src = "../media/space_inv_shot.png"
  intervalId = window.setInterval(draw,33);
  window.addEventListener("keydown", activate);
  window.addEventListener("keyup", deactivate);
  create_enemies()
  create_missiles()
 }

// *****************************************************************************

function draw(){
   context.clearRect(0, 0, width, height);
   context.drawImage(ship, player.x, player.y);

   //Draw shots and detect collisions
   for (let shot of missiles) {
      if (shot.status === true){
        if(shot.y <= 0){
          shot.status = false;
        };
        collision(shot)
        context.drawImage(shot_image, shot.x, shot.y);
        shot.y += shot.yChange;
      }
    }

    //Draw Aliens
    for (let alien of enemies){
      context.drawImage(joey, alien.x, alien.y);
      alien.x += alien.xChange;
      alien.y += alien.yChange;
      if ((alien.x <= 0) || (alien.x >= width - 20)){
        alien.xChange *= -1
      }
      if (alien.y+50 >= player.y){
        stop()
      }
   }

   //Drawing Player Movement
   if (moveLeft){
     player.x -= 5;
   }
   if (moveRight){
     player.x += 5;
   }
   if (player.x >= width){
     player.x = -50;
   }
   if (player.x < -50){
     player.x = width;
   }
}

//*****************************************************************************

function create_enemies(){
 for (let i = 0; i < 5; i += 1) {
      let alien = {
          x : getRandomNumber(0, width - 30),
          y : 0,
          width: 50,
          height: 72,
          xChange : getRandomNumber(-3,3),
          yChange : alien_speed
      };
      enemies.push(alien);
    }
}



// *****************************************************************************

function create_missiles(){
 for (let i = 0; i < 15; i += 1) {
      let shot = {
          x : player.x + 45,
          y : player.y,
          size : 10,
          yChange : -20,
          status: false
      };
      missiles.push(shot);
    }
}


// *****************************************************************************

function shoot(){
  for (let shot of missiles){
    if (shot.status === false){
      shot.y = player.y;
      shot.x = player.x + 45;
      shot.status = true;
      break
    }
  }
  shooting = true;
}


// *****************************************************************************

function collision(shot) {
    for (let alien of enemies){
      if (shot.x + shot.size < alien.x ||
        alien.x + alien.width < shot.x ||
        shot.y > alien.y + alien.height ||
        alien.y > shot.y + shot.size) {
        score = score;
      }
      else {
        shot.status = false;
        alien.x = getRandomNumber(0, width - 30);
        alien.y = 0;
        alien.xChange = getRandomNumber(-3,3)
        score += 1;
        scoreboard = document.getElementById("score").innerHTML = `Score: ${score}`;
        if(score % 10 === 0){
          for (let alien of enemies){
            alien.yChange *= 1.25;
            alien.xChange *= 1.25;
          }

          let new_enemy = {
            x : getRandomNumber(0, width - 30),
            y : 0,
            width: 50,
            height: 72,
            xChange : getRandomNumber(-3,3),
            yChange : alien_speed
          };
          enemies.push(new_enemy);
        }
      }
    }
}
// *****************************************************************************

//MOVEMENT AND SHOOTING CONTROLS

// *****************************************************************************

function activate(move){
   let keyCode = move.keyCode;

   if (keyCode === 37){
     moveLeft = true;
     moveRight = false;
   }

   if (keyCode === 39){
     moveRight = true;
     moveLeft = false;
   }

   if ((keyCode === 32) && (shooting === false)){
       shoot()
   }
 }

// *****************************************************************************

function deactivate(move){
   let keyCode = move.keyCode;

   if (keyCode === 37){
     moveLeft = false;
   }
   if (keyCode === 39){
     moveRight = false;
   }
   if (keyCode === 32){
     shooting = false;
   }
}

// *****************************************************************************

function getRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// *****************************************************************************

function stop(){
  end_link = (`../game_over.py?game=space_invaders&score=${score}`);
  window.clearInterval(intervalId)
  window.removeEventListener("keydown", activate)
  window.removeEventListener("keyup", deactivate)
  window.removeEventListener("click", init)
  window.location.assign(end_link);
}

// *****************************************************************************
