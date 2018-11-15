var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;

var x = "black",
    y = 10;

var image = new Image();

function predict(){
	
	//var image1 = ctx.getImageData(0,0,400,400);
	//image1.width = "28px";
	//image1.height = "28px";
	//ctx2.putImageData(image1,0,0,0,0,400,400);
	
	image.src = canvas.toDataURL("image/png");
	
	//image.width = 28;
	//image.height = 28;
	
	  image.addEventListener('load', function () {
    		ctx2.drawImage(this, 0, 0, 400, 400, 0, 0, 28, 28);
  		});
	
	//ctx2.drawImage(image,0,0);
	
	//alert(image);
	
	
	
	
	$.ajax({
		type: "POST",
		url: "../cgi-bin/php/predict_mnist.php",
		async: false,
		datatype: 'json',
		data: {
			imgBase64: image.src
		},
		success: function(response){
			try {
				digit_id.innerHTML = "Error";
				probability_id.innerHTML = "Error";
				console.log(response);
				//var obj = JSON.parse(response);
				//console.log(obj.benign);
				//console.log(obj.malignant);
				//pneumonia_id.innerHTML = (parseFloat(obj.benign)*100).toFixed(1) + "%";
				//non_pneumonia_id.innerHTML = (parseFloat(obj.malignant)*100).toFixed(1) + "%";
			}
			catch(err){
			/*	console.log(response);
				pneumonia_id.innerHTML = "Error";
				non_pneumonia_id.innerHTML = "Error";*/
			}

		},
		error: function(response){
			/*console.log(response);
			pneumonia_id.innerHTML = "Error";
			non_pneumonia_id.innerHTML = "Error";*/
		}
	})
	
}

function draw() {
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = x;
    ctx.lineWidth = y;
    ctx.stroke();
    ctx.closePath();
}

function erase() {
    //var m = confirm("Want to clear");
    //if (m) {
        ctx.clearRect(0, 0, w, h);
		ctx2.clearRect(0, 0, w, h);
        //document.getElementById("canvasimg").style.display = "none";
    //}
}

function save() {
    document.getElementById("canvasimg").style.border = "2px solid";
    var dataURL = canvas.toDataURL();
    document.getElementById("canvasimg").src = dataURL;
    document.getElementById("canvasimg").style.display = "inline";
}

function findxy(res, e) {
    if (res == 'down') {
        prevX = currX;
        prevY = currY;
        //currX = e.clientX - canvas.offsetLeft;
        //currY = e.clientY - canvas.offsetTop;
		currX = e.clientX - offsetleft;
        currY = e.clientY - offsettop;

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = x;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (res == 'up' || res == "out") {
        flag = false;
    }
    if (res == 'move') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            //currX = e.clientX - canvas.offsetLeft;
            //currY = e.clientY - canvas.offsetTop;
			currX = e.clientX - offsetleft;
        	currY = e.clientY - offsettop;
            draw();
        }
    }
}


function page_load(){
		//get prediction span ids
	digit_id = document.getElementById("digit");
	probability_id = document.getElementById("probability");
	
	canvas = document.getElementById('canvas');
	canvas2 = document.getElementById('canvas2');
	ctx2 = canvas2.getContext("2d");
	//canvas.style.width = "28px";
	

	var offsets = canvas.getBoundingClientRect();
	offsetleft = offsets.left;
	offsettop = offsets.top;
	//alert(offsets.top);
	//alert(offsets.left);
	
    ctx = canvas.getContext("2d");
    w = canvas.width;
    h = canvas.height;

    canvas.addEventListener("mousemove", function (e) {
        findxy('move', e)
    }, false);
    canvas.addEventListener("mousedown", function (e) {
        findxy('down', e)
    }, false);
    canvas.addEventListener("mouseup", function (e) {
        findxy('up', e)
    }, false);
    canvas.addEventListener("mouseout", function (e) {
        findxy('out', e)
    }, false);
}