<!DOCTYPE html>
<html>
 <head>
<title>PHP</title>
</head>
<body>
<?php
$x=12;
//$s="This is a sample string";
//echo $x ." ".$s;
function f($x){
echo $x;
}
f(10)
string fucntions
echo strlen($s);
echo str_word_count($s);
echo str_replace("world","3100","Heallo world");
//int function
echo is_int(12);
var_dump(is_int(12.12));
var_dump(is_flaot(12.12));
//math function
echo min(12,11,13,124,11.11,14);
echo max(12,11,13,124,14);
sqrt,abs,floor,round,rand,pow
//if else elseif
//switch
if(10>12){
echo "impossible";
}
else{
echo "possible"
}
//for loop,while,do while
$arr=array(1,3,2,5,4);
for ($i=0;$i<count($arr);i++){
echo $arr[$i] . "<br>";
}

foreach($arr as $val){
echo $val ."<br>";
}
$file=fopen("file.txt","r")
 or die("Unable to open the file");
echo fread($file,filesize("file.txt"));
fclose($file);
$file=fopen("file.txt","w")
 or die("Unable to open the file");
fwrite($file,"first line \n");
fclose($file);
$file=fopen("file.txt","a")
 or die("Unable to open the file");
fwrite($file,"first line \n");
fclose($file);
?>
</body>
</html>