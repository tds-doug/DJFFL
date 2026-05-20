<html>

<title>Fantasy Football Top 20 Players</title>

<body bgcolor="#EEEEFF" link="#004576" vlink="#004576" alink="#004576">
<font face="Verdana">

<h1><center>Here Be Ye List of Good Players</center></h1>
<p>

<?php
// Connecting to MySQL
$link = mysql_connect('localhost','ffl','foozeball')
  or die('Could not connect to MySQL: ' . mysql_error());

mysql_select_db('ffl_2004') or die('Could not access database');

// Perform sql query
$query = '(select name,nfl_team,position,ffl_team,total_pts from players_QB)'
       . ' union (select name,nfl_team,position,ffl_team,total_pts from players_WR)'
       . ' union (select name,nfl_team,position,ffl_team,total_pts from players_RB)'
       . ' union (select name,nfl_team,position,ffl_team,total_pts from players_TE)'
       . ' union (select name,nfl_team,position,ffl_team,total_pts from players_K)'
       . ' union (select name,nfl_team,position,ffl_team,total_pts from players_DEF)'
       . ' order by total_pts desc limit 20';

$result = mysql_query($query) or die('Could not query table: ' . mysql_error());

//Printing the results
echo "<table border=\"5\" width=\"100%\">\n";
echo "<tr>\n";
echo "  <td><center><b>Player</b></center></td>\n";
echo "  <td><center><b>NFL Name</b></center></td>\n";
echo "  <td><center><b>Position</b></center></td>\n";
echo "  <td><center><b>FFL Team</b></center></td>\n";
echo "  <td><center><b>Points This Season</b></center></td>\n";
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
