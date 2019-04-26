const canvas = document.querySelector('#draw');
const ctx = canvas.getContext('2d');
const slider = document.querySelector('#wSlider');
const output= document.querySelector('#widthVal');
let isDrawing = false;
let lastX = 0;
let lastY = 0;
var gdata;

function initCanvas(){
    canvas.width = 280;
    canvas.height = 280;
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = 'white';
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.lineWidth = 10;
}



function clearme(){
	ctx.clearRect(0,0,canvas.width, canvas.height);
	ctx.fillRect(0,0,canvas.width, canvas.height);
}

function calculate(){
    const canvas = document.querySelector('#draw');
    d=canvas.toDataURL("image/png");
    console.log(d)
   
    d3.json("/predict",{method:'POST', body:d}).then(function(data){
        console.log(data);
        gdata=data;
        document.querySelector('#originalCard').style.display="block";
        document.querySelector('#processedCard').style.display="block";
        document.querySelector('#originalPred').textContent='class: '+data.original;
        document.querySelector('#processedPred').textContent='class: '+data.preprocessed;
        document.querySelector('#originalImg').src=data.originalUrl;
        document.querySelector('#procImg').src=data.processedUrl


    });
}


function draw(e) {
  if (!isDrawing) return; // stop the fn from running when they are not moused down
  //console.log(e);
  ctx.beginPath();
  // start from
  ctx.moveTo(lastX, lastY);
  // go to
  ctx.lineTo(e.offsetX, e.offsetY);
  ctx.stroke();
  [lastX, lastY] = [e.offsetX, e.offsetY];
}

canvas.addEventListener('mousedown', (e) => {
  isDrawing = true;
  [lastX, lastY] = [e.offsetX, e.offsetY];
});


function initPage(){
    document.querySelector('#originalCard').style.display="none";
    document.querySelector('#processedCard').style.display="none";
    
    output.innerText = slider.value;
    
    slider.oninput = function() {
      output.innerText = this.value;
      ctx.lineWidth = this.value;
    }
    
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', () => isDrawing = false);
    canvas.addEventListener('mouseout', () => isDrawing = false);
}

initCanvas();
initPage();