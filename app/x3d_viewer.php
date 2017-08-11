<!DOCTYPE html>
<html>
	<head>
		<script type='text/javascript' src='http://www.x3dom.org/download/x3dom.js'> </script> 
		<link rel='stylesheet' type='text/css' href='http://www.x3dom.org/download/x3dom.css'></link>
	  	<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>
		<?php
			require ("includes/config.php");
			include_once "includes/header.php";
		?>



		<script>
			var unselectable = [];

			function mouse_unhighlight(event){
				anchorColor = '0 0.75 0.75';
		  		pressureColor = '0.5 1 0.5';
		  		defaultColor = '0.65 0.65 0.65';

				val = parseInt(event.target._x3domNode._objectID);
				var face = val - 2;

				if (unselectable.includes(face) || isSelected(pressureColor, val) || isSelected(anchorColor, val)) 
		  		{
		  			return;
		  		}

		  		setFaceColor(defaultColor, val);
			}

			function mouse_highlight(event){
				anchorColor = '0 0.75 0.75';
		  		pressureColor = '0.5 1 0.5';
		  		defaultColor = '0.65 0.65 0.65';
				
				val = parseInt(event.target._x3domNode._objectID);
				var face = val - 2;

				if (unselectable.includes(face) || isSelected(pressureColor, val) || isSelected(anchorColor, val)) 
		  		{
		  			return;
		  		}

		  		setFaceColor('0.529412 0.807843 0.980392', val); //light blue
			}



		  	function displayCoordinates(event)
		  	{
		  		var coordinates = event.hitPnt;

		  		//alert(Object.keys(event.target._x3domNode));
		  		// alert(event.target._x3domNode._objectID);

		  		val = parseInt(event.target._x3domNode._objectID);
		  		var face = val - 2;
		  		if (unselectable.includes(face)) 
		  		{
		  			return;
		  		}

		  		anchorColor = '0 0.75 0.75';
		  		pressureColor = '0.5 1 0.5';
		  		defaultColor = '0.65 0.65 0.65';

		  		if (event.button == 1) { // for aface
		  			// $('#marker').attr('translation', event.hitPnt);

		  			var aface = document.getElementById('aface');
		  			
		  			if (isSelected(anchorColor, val)) { //unselect this face
		  				setFaceColor(defaultColor, val);
			   			aface.value = aface.defaultValue;
		  			} else {	//select this face
		  				setFaceColor(anchorColor, val);
				   		// if another face was previously selected, change its color back
				   		if(aface.value != aface.defaultValue){
				   			var myval = parseInt(aface.value) + 2;
				   			setFaceColor(defaultColor, myval);
				   		}
				   		aface.value = face;

				   		var pface = document.getElementById('pface');  //unset pface values if the same
				   		if(pface.value == face){
				   			pface.value = pface.defaultValue;
				   		}
			   	}

		  		} else if (event.button == 2) { //for pface
		  			// $('#marker2').attr('translation', event.hitPnt)z

		  			var pface = document.getElementById('pface');

				   	if (isSelected(pressureColor, val)) {	//unselect this face
		  				setFaceColor(defaultColor, val);
		  				
			   			pface.value = pface.defaultValue;
		  			} else {	//select this face
		  				setFaceColor(pressureColor, val);

				   		// if another face was previously selected, change its color back
				   		if(pface.value != pface.defaultValue){
				   			var myval = parseInt(pface.value) + 2;
				   			setFaceColor(defaultColor, myval);
				   		}
				   		pface.value = face;

				   		var aface = document.getElementById('aface');   //unset aface values if the same
				   		if(aface.value == face){
				   			aface.value = aface.defaultValue;
				   		}
			   		}	
		  		}

		  	}

		  	function setFaceColor(color, value)
		  	{
		  		document.getElementById('Object__Shape_Mat_'.concat(String(value - 2))).setAttribute('diffuseColor', color);
		  	}

		  	function isSelected(color, value)
		  	{
		  		if (document.getElementById('Object__Shape_Mat_'.concat(String(value - 2))).getAttribute('diffuseColor') == color) {
		  			return true;
		  		} else {
		  			return false;
		  		}
		  	}

		  	function changeCameraAngle(event)
		  	{
		  		document.getElementById('x3d_element').runtime.nextView();
		  	
			}
			
		  	function center(event)
		  	{
		  		document.getElementById('x3d_element').runtime.fitAll();
		  	}

		  	function getDimensions() {
		  		var x3dnode = document.getElementById("x3d_object");        
			    var totalVol = x3dnode._x3domNode.getVolume();
			    var min = new x3dom.fields.SFVec3f();
			    var max = new x3dom.fields.SFVec3f();
			    totalVol.getBounds(min, max);
			    var vol = max.subtract(min);
			    $('#x_size').append(Math.round(vol.x * 100)/100);
			    $('#y_size').append(Math.round(vol.y*100)/100);
			    $('#z_size').append(Math.round(vol.z*100)/100);

			    var minValue = Math.min.apply(Math, [vol.x, vol.y, vol.z]);
			    var maxElementSize = minValue / 5;
			    var minElementSize = maxElementSize / 4;
			    $('#maxElementSize').attr('value', Math.round(maxElementSize * 100) /100);
			    $('#minElementSize').attr('value', Math.round(minElementSize* 100) / 100);
		  	}

		  	function displayMesh() {
		  		var meshButton = "<form target='_blank' action='view_mesh.php' method='post'><input id='id' name='id' type='hidden' value='<?php echo $_GET['job_id'];?>'><button style='width=auto; height=auto;color:black;' type='submit'>View Mesh</button></form>";
		  		$('#x3d_elements').append(meshButton);
		  	}

		  	function checkModel() {
		  		if ($('#sel1').val() === "") {
		  			alert("Granularity must be filled to submit!");
		  			return false;
		  		} else {

			  		$('#check').attr("hidden", "hidden");
			  		$('#animation').removeAttr("hidden");
			  		$('.row').css("filter","blur(5px)");
			  		
			  		$.ajax({
	                    type: 'POST',
	                    url:'mesh_check.php',
	                    dataType: 'json',
	                    data: {
	                    	job_id: $('#id').val(), 
		                    element_size: $('#sel1').val(),
		                    max_element_size: $('#maxElementSize').val(),
		                    min_element_size: $('#minElementSize').val()
		                },
	                    success: function (data){
	                    	$('#animation').attr("hidden", "hidden");
	                    	$('.row').css("filter","blur(0px)");

	                    	if (data.conversion === "success") {
	                    		$('#submit').removeAttr("hidden");
	                    		alert("Succesfully meshed your model.");
	                    		displayMesh();
	                    	} else {
	                    		alert("Sorry, this file cannot be meshed due to unconnected nodes. Please upload another file.")
	                    	}
	                    }
	                });
			  	}
		  	}

		  	function validateForm() {
		  		if (parseInt($('#anchorTotal').val()) < $('#removedAnchor').val().split(",").length -1 && parseInt($('#pressureTotal').val()) < $('#removedPressure').val().split(",").length -1){
		  			alert("Please select an anchor and a pressure face.");
		  		} else if (parseInt($('#anchorTotal').val()) < $('#removedAnchor').val().split(",").length -1) {
		  			alert("Please select an anchor face.");
		  		} else if (parseInt($('#pressureTotal').val()) < $('#removedPressure').val().split(",").length -1) {
		  			alert("Please select a pressure face.");
		  		} else {
		  			$('.row').css("filter","blur(5px)");
		  			$('#animation').removeAttr("hidden");
		  			return true;
		  		}
		  		return false;
		  	}

		  	

		  	$(document).ready(function(){

		  		$('#bbox').on({
		  			"shown.bs.dropdown": function() { this.closable = false; },
				    "click":             function() { this.closable = true; },
				    "hide.bs.dropdown":  function() { return this.closable; }
		  		});



			    $("#material").on("keydown", function(event) {
			    	// based on ASCII values, allows space, backspace, and delete
			    	var arr = [8,9,16,17,20,32,35,36,37,38,39,40,45,46]; 
					// Allow letters
					for(var i = 65; i <= 90; i++){
						arr.push(i);
					}
					// Prevent default if not in array
					if(jQuery.inArray(event.which, arr) === -1){
						event.preventDefault();
					}
			    });

			    // prevents user from copying and pasting in invalid values
			    $("#material").on("input", function(){
			    	// allow spaces by adding a " " after the Z
					var allowedChars = /[^a-zA-Z]/g;
					if($(this).val().match(allowedChars)){
						$(this).val( $(this).val().replace(allowedChars,'') );
					}
				});


		  		$('.dropdown-item').click(function() {
		  			var input = $(this).closest('.input-group').find('input.element_size');
    				input.val($(this).text());
		  		});

				countP = 0;
				countA = 0;
				$('#pressureT').on('click', '.addBtn', function() {
					if ($.trim($('#pface').val()) === "" || $.trim($('#pvalue').val()) === "") {	return false; }
					$('#pressureT tbody').append('<tr><td><input type="hidden" name="pface'+ countP +'"value=' +$('#pface').val()+'><input type="hidden" name="pvalue'+ countP +'"value=' +$('#pvalue').val()+'><h5> Face:'+$('#pface').val()+', Pressure:'+$('#pvalue').val()+'</h5></td><td><input type="button" value="X" class="delBtn" onclick="attachListener()"></td></tr>');

					$('#pressureTotal').val(countP++);

					unselectable.push(parseInt($('#pface').val()));
					$('#pface').val('');
					$('#pvalue').val('');
					return false; 
				});

				$('#anchorT').on('click', '.addBtn', function() {
					if ($.trim($('#aface').val()) === "") { return false; }
					$('#anchorT tbody').append('<tr><td><input type="hidden" name="aface'+ countA +'"value=' +$('#aface').val()+'><h5> Face:'+$('#aface').val()+'</h5></input></td><td><input type="button" value="X" class="delBtn" onclick="attachListener()"></td></tr>');

					$('#anchorTotal').val(countA++);

					unselectable.push(parseInt($('#aface').val()));
					$('#aface').val('');
					return false; 
				});

				$("table").on('click', '.delBtn', function() {
					face = $(this).parent().parent().find('input[type=hidden]').val();
					var temp = $(this).parent().parent().find('input[type=hidden]').attr('name').substr(5);
					var type = $(this).parent().parent().find('input[type=hidden]').attr('name').substr(0, 1);

					$(this).parent().parent().remove();

					if (type == 'a') {
						$('#removedAnchor').val($('#removedAnchor').val() + temp + ",");

					} else {
						$('#removedPressure').val($('#removedPressure').val() + temp + ",");
					}
					

					setFaceColor('0.65 0.65 0.65', parseInt(face)+2);

					var index = unselectable.indexOf(parseInt(face));
			  		if (index > -1) {
			  			unselectable.splice(index, 1);
			  		}
				});
			})

		  </script>
	  </head>


    <body> 
		<div class="container" align='center'>
			<h1>Lattice Mesh</h1>
			<x3d id='x3d_element' class="x3d_element" align='center' > 
				<div id="instructions">
					<button type="button" onclick="center(event)" class="btn btn-secondary">Center</button>
				</div>
				<scene>
					<inline id="x3d_object" onload="center(); getDimensions();" nameSpaceName="Object" mapDEFToID="true" url="x3d_output/<?php echo $_GET["filename"];?>.x3d" onmouseover="mouse_highlight(event)" onmouseout="mouse_unhighlight(event)" onclick="displayCoordinates(event)"></inline> 
				</scene> 
			</x3d>   				
		</div>
    </body>
</html>