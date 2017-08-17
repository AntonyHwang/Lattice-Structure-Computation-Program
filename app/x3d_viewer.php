<!DOCTYPE html>
<html>
	<?php
		require ("includes/config.php");
		include_once "includes/header.php";
	?>

	<head>
		<script type='text/javascript' src='http://www.x3dom.org/download/x3dom.js'> </script> 
		<link rel='stylesheet' type='text/css' href='http://www.x3dom.org/download/x3dom.css'></link>
	  	<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.0.min.js" ></script>

	  	<script>	
		  	function center(event)
		  	{
		  		document.getElementById('the_element').runtime.fitAll();
		  	}

	  	</script>
		<style>
			#the_element {
				width: 50%;
				height: 50%;
				border: none;  // remove the default 1px border
				position: relative;
			}
			#toggler {
				position: absolute;
				float: left;
				z-index: 1;
				top: 0px;
				left: 0px;
				width: 10em;
				height: 2em;
				border: none;
				background-color: #202021;
				color: #ccc;
			}
		</style>
	</head>


	<body>
			<br>
			<br>
			<br>
			<x3d id="the_element" style = "width:98%; height:80%; margin-left:1%; margin-right:1%; margin-bottom:1%;">
				<button id="toggler" onclick="center(event)">Center</button>   
				<scene>
					<inline id="x3d_object" url="x3d_output/<?php echo $_GET["filename"];?>.x3d" onload="center();"></inline> 
				</scene> 
			</x3d>   
	</body>
</html>