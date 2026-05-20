#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'root';
my $password = 'yoda';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_upd_lineup_pts.cgi";
print header();
print start_html("FFL Admin - Update Lineups Points");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Player Weekly Pts Update Page</font></center></h1>\n";

if(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  my $nfl_new_team = param( 'f_nfl_new_team' );

  my $position;
  my $name;
  my $nfl_old_team;

  if($player=~m/([A-Za-z \-\.\']+), ([A-Z]+), ([A-Za-z]+)/)
  {
    $name = Foozeball::db_escape($1);
    $position = $2;
    $nfl_old_team = $3;
  }

  chomp($name);
  chomp($position);
  chomp($nfl_old_team);

  my $playerDB = "players_" . $position;

  print "Player is $name<br>\n";
  print "Position is $position<br>\n";
  print "Old NFL Team is $nfl_old_team<br>\n"; 
  print "New NFL Team is $nfl_new_team<br>\n"; 
  print "<p>\n";

  my $sql_upd_players = "update $playerDB set nfl_team = '$nfl_new_team' where player = '$name' and position = '$position' and nfl_team = '$nfl_old_team';";
  my $sth_upd_players = $dbh->prepare($sql_upd_players);
  $sth_upd_players->execute();

  my $sql_upd_lineups = "update lineups set nfl_team = '$nfl_new_team' where player = '$name' and position = '$position' and nfl_team = '$nfl_old_team';";
  my $sth_upd_lineups = $dbh->prepare($sql_upd_lineups);
  $sth_upd_lineups->execute();

  print "Player Update sql is $sql_upd_players<p>\n";
  print "Lineup sql is $sql_upd_lineups<p>\n";
}
if(param( 'f_team' ))
{
  my $team = param( 'f_team' );
  my $week = param( 'f_week');

  print "The following players are on $ffl_team for week $week<p>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
  print "<td><select name=f_player><option selected value=\"\">Select a Player\n";

  my $sql_get_players = "select * from lineups where week = '$week' and where ffl_team = '$ffl_team' order by position asc;";

  my $sth_get_players = $dbh->prepare($sql_get_players);
  $sth_get_players->execute();

  while (my $row = $sth_get_players->fetchrow_arrayref)
  {
    print "  <option value=\"$result\">$result\n";
  }

  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=hidden name=f_ffl_team value=\"$ffl_team\">\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";

)
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
  print "  <option value=\"Death Blow\">Death Blow\n";
  print "  <option value=\"Death To Armenia\">Death To Armenia\n";
  print "  <option value=\"Dublin Tundra Wookies\">Dublin Tundra Wookies\n";
  print "  <option value=\"IN DREW BREES WE TRUST\">IN DREW BREES WE TRUST\n";
  print "  <option value=\"East Bay Gotham Knights\">East Bay Gotham Knights\n";
  print "  <option value=\"Mr Rodgers Neighborhood\">Mr Rodgers Neighborhood\n";
  print "  <option value=\"Shiva Blast\">Shiva Blast\n";
  print "  <option value=\"Mantooth Saints\">Mantooth Saints\n";
  print "  <option value=\"Oklahoma Rednecks\">Oklahoma Rednecks\n";
  print "  <option value=\"The Bam Bam Bigaloes\">The Bam Bam Bigaloes\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}

print end_html();
