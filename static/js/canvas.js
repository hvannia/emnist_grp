const canvas = document.querySelector('#draw');
const ctx = canvas.getContext('2d');
canvas.width = 280;
canvas.height = 280;
ctx.fillStyle = "black";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.strokeStyle = 'white';
ctx.lineJoin = 'round';
ctx.lineCap = 'round';
ctx.lineWidth = 27;

let isDrawing = false;
let lastX = 0;
let lastY = 0;


function clearme(){
	//const context = canvas.getContext('2d');
	//context.clearRect(0, 0, canvas.width, canvas.height);
	ctx.clearRect(0,0,canvas.width, canvas.height);
	//ctx.fillStyle="black";
	ctx.fillRect(0,0,canvas.width, canvas.height);
	
}

function calculate(){
    const canvas = document.querySelector('#draw');
    d=canvas.toDataURL("image/png");
	var blob = new Blob([d], {type:'image/png'});
    console.log(d)
    var url= '/mark'
	var xhr = new XMLHttpRequest();
	xhr.open("POST",url, true);
	xhr.onreadystatechange = function() { // Call a function when the state changes.
	if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        result=document.getElementById('result');
			// Request finished. Do processing here.
        console.log(this.responseText);
        result.innerHTML=this.responseText;
		}
	}
    xhr.send(blob); 
    /* for debugging only 
    w=window.open('about:blank','image from canvas');
    w.document.write("<img src='"+d+"' alt='from canvas'/>");
    w.document.body.style.background = 'blue';
    ***********************/
}
function process_result(){
   /* d3.json("/mark").then(function(metadata){
        var level="";
    });*/
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