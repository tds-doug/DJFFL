<html>

<title>Fantasy Football Rosters</title>

<body bgcolor="#EEEEFF" link="#004576" vlink="#004576" alink="#004576">
<font face="Verdana">

<h1><center>Here Be Ye Roster</center></h1>
<p>

<?php
// Control loop to see if the form should access MySQL or prompt for a parameter
if($_POST['f_team'])
{

  $team=$_POST['f_team'];

  echo "<center><h3>Roster for $team</h3></center>\n";

  // Connecting to MySQL
  $link = mysql_connect('localhost','ffl','foozeball')
    or die('Could not connect to MySQL: ' . mysql_error());

  mysql_select_db('ffl_2004') or die('Could not access database');

  // Perform sql query
  $query = "(select name,nfl_team,position,contract_end,contract_value,total_pts,value from players_QB where ffl_team = '$team')"
          . " union (select name,nfl_team,position,contract_end,contract_value,total_pts,value from players_WR where ffl_team = '$team')"
          . " union (select name,nfl_team,position,contract_end,contract_value,total_pts,value from players_RB where ffl_team = '$team')"
          . " union (select name,nfl_team,position,contract_end,contract_value,total_pts,value from players_TE where ffl_team = '$team')"
          . " union (select name,nfl_team,position,contract_end,contract_value,total_pts,value from players_K where ffl_team = '$team')"
          . " union (select name,nfl_team,position,contract_end,contract_value,total_pts,value from players_DEF where ffl_team = '$team')"
          . " order by total_pts desc";

  $result = mysql_query($query) or die('Could not query table: ' . mysql_error());

  //Printing the results
  echo "<table border=\"5\" width=\"100%\">\n";
  echo "<tr>\n";
  echo "  <td><center><b>Player</b></center></td>\n";
  echo "  <td><center><b>Team</b></center></td>\n";
  echo "  <td><center><b>Position</b></center></td>\n";
  echo "  <td><center><b>Contracted Thru</b></center></td>\n";
  echo "  <td><center><b>Points This Season</b></center></td>\n";
  echo "  <td><center><b>Fantasy Salary</b></center></td>\n";
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

} // End of first part of if statement
else
{ // Beginning of second part of if statement
  echo "<form action=\"./rosters.php\" method=\"post\">\n";
  echo "<table>\n";

  echo "<tr>\n";
  echo "<td>Team:</td>\n";
  echo "<td><select name=f_team><option selected value=\"\">Select a Team\n";
  echo "  <option value=\"Armenia\">Armenia\n";
  echo "  <option value=\"Death To Armenia\">Death To Armenia\n";
  echo "  <option value=\"East Bay Bottle Rockets\">East Bay Bottle Rockets\n";
  echo "  <option value=\"Here Comes Da Pain\">Here Comes Da Pain\n";
  echo "  <option value=\"Maximus Sparticus\">Maximus Sparticus\n";
  echo "  <option value=\"NorCal Nuggets\">NorCal Nuggets\n";
  echo "  <option value=\"Team Kill\">Team Kill\n";
  echo "  <option value=\"The Maverick Boilermakers\">The Maverick Boilermakers\n";
  echo "  </select></td>\n";
  echo "</tr>\n";

  echo "</table>\n";

  echo "<input type=submit value=\"Submit\">\n";
  echo "</form>\n";
} // End of second part of if statement
?>

</body>
</html>
