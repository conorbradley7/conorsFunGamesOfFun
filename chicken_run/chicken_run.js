let game = "chicken_run";
let replay_link = "chicken_run/chicken_run.html";
let context;
let canvas;
let width;
let height;
let player;
let score = 0;
let jmpbtn = false;
let end_link;


let obstacle_interval = 5000;
let obstacle_speed = -5;
let obstacle_image = new Image();;
let obstacles = [];

let chicken_speed = 100;
let chicken = new Image();
let chsrc;

let intervalIdScore;
let intervalIdDraw;
let intervalIdInitialiseObstacle;
let intervalIdWhichChicken;
let intervalIdClouds;


let cloud1 = new Image();
let cloud2 = new Image();
let cloud3 = new Image();
let cloudpic = [cloud1,cloud2,cloud3]
let clouds = [];
let cloud_speed = -7;
let cloud_freq = 3000;

let scoreboard;


document.getElementById("startBtn").addEventListener("click", init, false);
// *****************************************************************************

function init(){
  document.getElementById("startBtn").style.display = "none";
  canvas = document.querySelector('canvas');
  context = canvas.getContext('2d');
  width = canvas.width;
  height = canvas.height;

  player = {
    x: width/5,
    y: 0.69*height,
    yChange: -25,
    width: 60,
    height: 40,
    jumping: false,
    onGround: true
  };


  chicken.src = "../media/chicken_run1.png";
  chsrc  = "../media/chicken_run1.png";
  cloud1.src = "../media/cloud1.png";
  cloud2.src = "../media/cloud2.png";
  cloud3.src = "../media/cloud3.png";
  obstacle_image.src = "../media/obstacle.png";



  intervalIdWhichChicken = window.setInterval(whichChicken, chicken_speed);
  intervalIdDraw = window.setInterval(draw,33);
  intervalIdScore = window.setInterval(score_update,1000);
  intervalIdInitialiseObstacle = window.setInterval(initialise_obstacle, obstacle_interval);
  intervalIdClouds = window.setInterval(initialise_cloud, cloud_freq);

  create_obstacles()
  create_clouds()

  window.addEventListener("keydown", activate);
  window.addEventListener("keyup", deactivate);
}
// *****************************************************************************

function draw(){
  context.clearRect(0, 0, width, height);
  context.drawImage(chicken, player.x, player.y);

  for (let obstacle of obstacles){
    if (obstacle.initialised === true){
      context.drawImage(obstacle_image, obstacle.x, obstacle.y)
      obstacle.x += obstacle.xChange;
    }
    if (obstacle.x <= -50){
      obstacle.initialised = false;
      obstacle.x = width - 50;
    }
  }

  for (let cloud of clouds){
    if (cloud.initialised){
    context.drawImage(cloud.pic, cloud.x, cloud.y);
    cloud.x += cloud.xChange;
    }
    if (cloud.x <= -130){
      cloud.x = width + 130
      cloud.initialised = false;
    }
  }

  if (player.jumping === true){
    jump()
  }

  collision()
}

// *****************************************************************************

function create_obstacles(){
  if (obstacles.length === 0){
    for (let i = 0; i < 20; i += 1) {
         let obstacle_verticalness = 104;
         let obstacle = {
             x : width - 64,
             y : 0.69 * height + 69 - obstacle_verticalness,
             width: (30, 70),
             height: obstacle_verticalness,
             xChange: obstacle_speed,
             index: i,
             initialised: false,
         };
         obstacles.push(obstacle);
     }
   }
}

// *****************************************************************************

function create_clouds(){
  if (clouds.length === 0){
    for (let i = 0; i < 10; i += 1) {
      let cloud = {
          x: width + 50,
          y: "",
          xChange: cloud_speed,
          initialised: false,
          pic: ""
      }
      clouds.push(cloud)
    }
  }
}

// *****************************************************************************

function initialise_obstacle(){
  let rand_obs = getRandomNumber(0,19);
  for (let obstacle of obstacles){
    if (obstacle.index === rand_obs){
      if (obstacle.initialised === false){
        obstacle.initialised = true;
        return
      }
      else{
        initialise_obstacle()
      }
    }
  }
}

// *****************************************************************************

function initialise_cloud(){
  for (let cloud of clouds){
    if (cloud.initialised === false){
      cloud.initialised = true;
      cloud.pic = cloudpic[getRandomNumber(0,2)];
      cloud.y = getRandomNumber(50, 100);
      break
    }
  }
}

// *****************************************************************************

function whichChicken(){
  if (chsrc === "../media/chicken_run1.png"){
    chicken.src = "../media/chicken_run2.png";
    chsrc = "../media/chicken_run2.png";
  }
  else if (chsrc === "../media/chicken_run2.png"){
    chicken.src = "../media/chicken_run1.png";
    chsrc = "../media/chicken_run1.png";
  }
}

// *****************************************************************************

function jump(){
    if (player.jumping && !player.onGround){
      player.y += player.yChange;
      player.yChange += 1;
      chicken.src = "../media/chicken_stand.png"
      chsrc = "../media/chicken_stand"
    }
    if (!jmpbtn && player.yChange <= 0){
      player.yChange = 0;
      jmpbtn = true;
    }
    if (player.y >= 0.69 * height){
      player.y = 0.69 * height;
      player.onGround = true;
    }
    if (player.onGround){
        player.jumping = false;
        player.yChange = -25
        jmpbtn = false;
        chicken.src = "../media/chicken_run2.png";
        chsrc = "../media/chicken_run2.png";
    }
}

// *****************************************************************************


function collision(){
  for (let obstacle of obstacles){
    if (player.x + player.width < obstacle.x ||
      obstacle.x + obstacle.width < player.x ||
      player.y > obstacle.y + obstacle.height ||
      obstacle.y > player.y + player.height) {
      score = score;
    }
    else{
      stop()
    }
  }
}

// *****************************************************************************

function activate(move){
   let keyCode = move.keyCode;

   if (keyCode === 32 && player.jumping === false){
     player.jumping = true;
     player.onGround = false;
     jmpbtn = true;
   }
 }

// *****************************************************************************

function deactivate(move){
   let keyCode = move.keyCode;
   if (keyCode === 32){
     jmpbtn = false;
   }
   if (keyCode === 32 && player.y === 0.69*height) {
     player.jumping = false;
   }
   return
}

// *****************************************************************************

function getRandomNumber(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// *****************************************************************************

function score_update(){
  score += 1;
  if (score % 20 === 0){
    window.clearInterval(intervalIdInitialiseObstacle)
    obstacle_interval *= 0.9;
    intervalIdInitialiseObstacle = window.setInterval(initialise_obstacle, obstacle_interval);
    obstacle_speed *= 2
    obstacle_interval *= 0.8
    cloud_speed *= 1.5
  }
  scoreboard = document.getElementById("score").innerHTML = `Score: ${score}`;
}

// *****************************************************************************

function stop(){
  end_link = (`../game_over.py?game=chicken_run&score=${score}`);
  window.clearInterval(intervalIdDraw)
  window.clearInterval(intervalIdInitialiseObstacle)
  window.clearInterval(intervalIdWhichChicken)
  window.clearInterval(intervalIdScore)
  window.removeEventListener("keydown", activate)
  window.removeEventListener("keyup", deactivate)
  window.removeEventListener("click", init)
  window.location.assign(end_link)
}

// *****************************************************************************
