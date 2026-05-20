<html>

<title>Fantasy Football Standings</title>

<body bgcolor="#EEEEFF" link="#004576" vlink="#004576" alink="#004576">
<font face="Verdana">

<h1><center>Here Be Ye Current Standings</center></h1>
<p>

<?php
// Connecting to MySQL
$link = mysql_connect('localhost','ffl','foozeball')
  or die('Could not connect to MySQL: ' . mysql_error());

mysql_select_db('ffl_2004') or die('Could not access database');

// Begin of Northern Conference section

// Perform sql query
$query = "select team,wins,losses,games_back,current_streak,season_points from standings where conference = 'Northern' order by wins desc";
$result = mysql_query($query) or die('Could not query table: ' . mysql_error());

//Printing the results
echo "<h3><center>Northern Conference</center><h3>\n";
echo "<table border=\"5\" align=\"center\" width=\"80%\">\n";
echo "<tr>\n";
echo "  <td><center><b>Team</b></center></td>\n";
echo "  <td><center><b>Wins</b></center></td>\n";
echo "  <td><center><b>Losses</b></center></td>\n";
echo "  <td><center><b>Games Back</b></center></td>\n";
echo "  <td><center><b>Current Streak</b></center></td>\n";
echo "  <td><center><b>Season Points</b></center></td>\n";
echo "</tr>\n";

while ($line = mysql_fetch_array($result, MYSQL_ASSOC)) {
  echo "\t<tr>\n";
  foreach ($line as $col_value) {
    echo "\t\t<td>$col_value</td>\n";
  }
  echo "\t</tr>\n";
}
echo "</table>\n";
echo "<p>\n";

// Free result set
mysql_free_result($result);

// End of Northern Conference section
// Begin of Southern Conference section

// Perform sql query
$query = "select team,wins,losses,games_back,current_streak,season_points from standings where conference = 'Southern' order by wins desc";
$result = mysql_query($query) or die('Could not query table: ' . mysql_error());

//Printing the results
echo "<h3><center>Southern Conference</center><h3>\n";
echo "<table border=\"5\" align=\"center\" width=\"80%\">\n";
echo "<tr>\n";
echo "  <td><center><b>Team</b></center></td>\n";
echo "  <td><center><b>Wins</b></center></td>\n";
echo "  <td><center><b>Losses</b></center></td>\n";
echo "  <td><center><b>Games Back</b></center></td>\n";
echo "  <td><center><b>Current Streak</b></center></td>\n";
echo "  <td><center><b>Season Points</b></center></td>\n";
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

// End of Southern Conference section

// Closing connection
mysql_close($link);

?>

</body>
</html>
