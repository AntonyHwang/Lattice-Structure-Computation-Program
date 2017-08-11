<!DOCTYPE html>

<?php
	require("includes/config.php");
    include_once "includes/header.php";
?>

<script type="text/javascript">
    // $(document).ready(function(){
    //     $('#submit').click(function(){
    //         $('row').css("filter","blur(5px)");
    //         $('#loader').removeAttr("hidden");
    //     });
    function load() {
        if ($('#x').val() === "" && $('#y').val() === "" && $('#z').val() === "") {

        } else {
            $('#loader').removeAttr("hidden");
            $('row').css("filter","blur(5px)");
            $("form :input").prop('readonly', true);
            document.getElementById("submit").style.display = "none";
            document.getElementById("shape").style.display = "none";
        }
	}
</script>  

<html>
<body>
    <row>
        <div class ="login">  
            <form action="index.php" method="post" enctype="multipart/form-data"> 
                <h1>Lattice Generator</h1>
                <h5>Shape:</h5>
                <select name="shape" class="form-control" id="shape" required>
                    <option value="45" selected>45</option>
                    <option value="90">90</option>
                </select>
                <h5>Dimension:</h5>
                <div class="row">
                    <div class="col-md-4"><input name = "x" type="number" min="1" step="1" placeholder="x" required/></div>
                    <div class="col-md-4"><input name = "y" type="number" min="1" step="1" placeholder="y"required/></div>
                    <div class="col-md-4"><input name = "z" type="number" min="1" step="1" placeholder="z" required/></div>
                </div>
                <h5> </h5>
                <input type="submit" class="btn btn-block btn-large" value="Generate" id="submit" onclick="load()">
            </form>
        </div> 
    </row>
    <div id='loader' hidden="true"</div> 
</body>
</html>

<?php
    if (!empty($_POST)) {
        $shape = $_POST["shape"];
        $x = $_POST['x'];
        $y = $_POST['y'];
        $z = $_POST['z'];
        set_time_limit(150);
        $call_python = $py_path." py/app.py 2>&1".$shape." ".$x." ".$y." ".$z;
        $result = shell_exec($call_python);
        header('Location: x3d_viewer.php?filename='.$shape."_".$x."_".$y."_".$z);
    }
?>