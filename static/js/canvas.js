const canvas = document.querySelector('#draw');
const ctx = canvas.getContext('2d');
canvas.width = 280;
canvas.height = 280;
ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.strokeStyle = 'white';
ctx.lineJoin = 'round';
ctx.lineCap = 'round';
ctx.lineWidth = 15;

let isDrawing = false;
let lastX = 0;
let lastY = 0;



function clearme(){
	const context = canvas.getContext('2d');
	context.clearRect(0, 0, canvas.width, canvas.height);
}

function calculate(){
    const canvas = document.querySelector('#draw');
    d=canvas.toDataURL("image/png");
    
    /* for debugging only */
    w=window.open('about:blank','image from canvas');
    w.document.write("<img src='"+d+"' alt='from canvas'/>");
    w.document.body.style.background = 'blue';
    /***********************/
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


canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', () => isDrawing = false);
canvas.addEventListener('mouseout', () => isDrawing = false);