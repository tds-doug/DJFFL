#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $cgi_script = "\/cgi-bin\/ffl_2015\/lineup.cgi";

print header();
print start_html("Fantasy Football Lineup");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Here Be Ye Lineup</font></center></h1>\n";
print "<p>\n";

if(param( 'f_team' ))
{


  my $team = param( 'f_team' );
  my $week = param( 'f_week');
  my $column = "week" . $week . "_pts";
  my $starter_points = 0;
  my $bench_points = 0;

  print "<center><h2>Starters for $team for Week $week</h2></center>\n";

  print "<table border=\"5\" align=\"center\" width=\"80%\">";
  print "<tr>\n";
  print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">Postion</font></b></center></td>\n";
  print "<td width=\"40%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
  print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
  print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">NFL Opponent</font></b></center></td>\n";
  print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">Points</font></b></center></td>\n";
  print "<tr>\n";

  $starter_points = $starter_points + get_players($team, 'QB', $week, 'Y');
  $starter_points = $starter_points + get_players($team, 'WR', $week, 'Y');
  $starter_points = $starter_points + get_players($team, 'RB', $week, 'Y');
  $starter_points = $starter_points + get_players($team, 'TE', $week, 'Y');
  $starter_points = $starter_points + get_players($team, 'K', $week, 'Y');
  $starter_points = $starter_points + get_players($team, 'DEF', $week, 'Y');

  print "</table>\n";

  print "<center><h3>Total Points: $starter_points</h3></center>\n";

  print "<p>\n";

  print "<center><h2>Bench for $team for Week $week</h2></center>\n";

  print "<table border=\"5\" align=\"center\" width=\"80%\">";
  print "<tr>\n";
  print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">Postion</font></b></center></td>\n";
  print "<td width=\"40%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
  print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
  print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">NFL Opponent</font></b></center></td>\n";
  print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">Points</font></b></center></td>\n";
  print "<tr>\n";

  $bench_points = $bench_points + get_players($team, 'QB', $week, 'N');
  $bench_points = $bench_points + get_players($team, 'WR', $week, 'N');
  $bench_points = $bench_points + get_players($team, 'RB', $week, 'N');
  $bench_points = $bench_points + get_players($team, 'TE', $week, 'N');
  $bench_points = $bench_points + get_players($team, 'K', $week, 'N');
  $bench_points = $bench_points + get_players($team, 'DEF', $week, 'N');

  print "</table>\n";

  print "<center><h3>Total Bench Points: $bench_points</h3></center>\n";
}
else
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Week:</font></td>\n";
  print "<td><select name=f_week><option selected value=\"\">Select a week\n";
  print "  <option value=\"1\">Week 1\n";
  print "  <option value=\"2\">Week 2\n";
  print "  <option value=\"3\">Week 3\n";
  print "  <option value=\"4\">Week 4\n";
  print "  <option value=\"5\">Week 5\n";
  print "  <option value=\"6\">Week 6\n";
  print "  <option value=\"7\">Week 7\n";
  print "  <option value=\"8\">Week 8\n";
  print "  <option value=\"9\">Week 9\n";
  print "  <option value=\"10\">Week 10\n";
  print "  <option value=\"11\">Week 11\n";
  print "  <option value=\"12\">Week 12\n";
  print "  <option value=\"13\">Week 13\n";
  print "  <option value=\"14\">Week 14\n";
  print "  <option value=\"15\">Week 15\n";
  print "  <option value=\"16\">Week 16\n";
  print "  <option value=\"17\">Week 17\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Team:</font></td>\n";
  print "<td><select name=f_team><option selected value=\"\">Select a Team\n";
  print "  <option value=\"A Dingo Ate My Brady\">A Dingo Ate My Brady\n";
  print "  <option value=\"Armenia\">Armenia\n";
  print "  <option value=\"Oklahoma Rednecks\">Oklahoma Rednecks\n";
  print "  <option value=\"Death Blow\">Death Blow\n";
  print "  <option value=\"Death To Armenia\">Death To Armenia\n";
  print "  <option value=\"Dublin Tundra Wookies\">Dublin Tundra Wookies\n";
  print "  <option value=\"IN DREW BREES WE TRUST\">IN DREW BREES WE TRUST\n";
  print "  <option value=\"East Bay Gotham Knights\">East Bay Gotham Knights\n";
  print "  <option value=\"Mr Rodgers Neighborhood\">Mr Rodgers Neighborhood\n";
  print "  <option value=\"Shiva Blast\">Shiva Blast\n";
  print "  <option value=\"Mantooth Saints\">Mantooth Saints\n";
  print "  <option value=\"The Bam Bam Bigaloes\">The Bam Bam Bigaloes\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();

sub get_players{
  # The team name, week, and position should be passed to this subroutine
  my $ffl_team = $_[0];
  my $position = $_[1];
  my $week = $_[2];
  my $starter = $_[3];

  my $column = "week" . $week . "_pts";
  my $points = 0;

  my $sql_player = "select position,player,nfl_team,points from lineups where week = '$week' and ffl_team = '$ffl_team' and position = '$position' and starter = '$starter' order by player;";

    my $sth_player = $dbh->prepare($sql_player);
    $sth_player->execute();

    while (my $row = $sth_player->fetchrow_arrayref)
    {
      print "    <tr>\n";
      print "      <td width=\"25%\"><center><font color=\"#FFFFDF\">$row->[0]</font></center></td>\n";
      print "      <td width=\"40%\"><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
      print "      <td width=\"10%\"><center><img src=\"http://www.djffl.net/images/$row->[2]_h.gif\"></center></td>\n";


# SQL that takes the NFL Team from the previous SQL and find the opponent for this week in the nfl_schedule table
      my $column2 = "week" . $week;
      my $sql_opponent = "select $column2 from nfl_schedule where nfl_team = '$row->[2]';";
      my $sth_opponent = $dbh->prepare($sql_opponent);
      $sth_opponent->execute();
 
## Comment out the following when the NFL schedule is not yet updated to remove
## NFL Opponent from the weekly lineup

      # There should only ever be 1 row that is returned for the previous sql
      while (my $row_opponent = $sth_opponent->fetchrow_arrayref)
      {
        print "      <td width=\"10%\"><center><img src=\"http://www.djffl.net/images/$row_opponent->[0]_l.gif\"</center></td>\n";
      } 

## End section to comment out

# SQL that takes the name from the previous SQL and find the pts for this week in the player_position table
      my $playerDB = "players_" . $position;

      my $player = Foozeball::db_escape($row->[1]);
      my $sql_player_pts = "select $column from $playerDB where player = '$player' and nfl_team = '$row->[2]';";
      my $sth_player_pts = $dbh->prepare($sql_player_pts);
      $sth_player_pts->execute();

# There may be more then 1 row that is returned for the previous SQL
      while (my $row_pts = $sth_player_pts->fetchrow_arrayref)
      {
        print "      <td width=\"15%\"><center><font color=\"#FFFFDF\">$row_pts->[0]</font></center></td>\n";
        $points = $points + $row_pts->[0];
      }

      print "    </tr>\n";

    }
    return($points);
} # End get_players subroutine
