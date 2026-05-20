<html>

<title>Fantasy Football Managers</title>

<body bgcolor="#EEEEFF" link="#004576" vlink="#004576" alink="#004576">
<font face="Verdana">

<h1><center>Here Be Ye List of Managers</center></h1>
<p>

<?php
// Connecting to MySQL
$link = mysql_connect('localhost','ffl','foozeball')
  or die('Could not connect to MySQL: ' . mysql_error());

mysql_select_db('ffl_2004') or die('Could not access database');

// Perform sql query
$query = 'select * from managers order by name';
$result = mysql_query($query) or die('Could not query table: ' . mysql_error());

//Printing the results
echo "<table border=\"5\" width=\"100%\">\n";
echo "<tr>\n";
echo "  <td><center><b>Manager Name</b></center></td>\n";
echo "  <td><center><b>Team Name</b></center></td>\n";
echo "  <td><center><b>Manager Email</b></center></td>\n";
echo "</tr>\n";

while ($line = mysql_fetch_array($result, MYSQL_ASSOC)) {
  echo "\t<tr>\n";
  foreach ($line as $col_value) {
    echo "\t\t<td>$col_value</td>\n";
  }
  echo "\t</tr>\n";
}
echo "</table>\n";

// Free result set
mysql_free_result($result);

// Closing connection
mysql_close($link);

?>

</body>
</html>
