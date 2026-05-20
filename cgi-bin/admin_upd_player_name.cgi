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

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_upd_player_name.cgi";
print header();
print start_html("FFL Admin - Update Player NFL Team");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Player Name Update Page</font></center></h1>\n";

if(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  my $player_new_name = param( 'f_player_new_name' );

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
else  
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
  print "<td><select name=f_player><option selected value=\"\">Select a Player\n";

  my $sql_player = "(select player,position,nfl_team from ffl_2015.players_QB)"
        . " union (select player,position,nfl_team from players_WR)"
        . " union (select player,position,nfl_team from players_RB)"
        . " union (select player,position,nfl_team from players_TE)"
        . " union (select player,position,nfl_team from players_K)"
        . " union (select player,position,nfl_team from players_DEF)"
        . " order by player asc;";

  my $sth_player = $dbh->prepare($sql_player);
  $sth_player->execute();

  while (my $row = $sth_player->fetchrow_arrayref)
  {
    my $result = "$row->[0], $row->[1], $row->[2]";
    print "  <option value=\"$result\">$result\n";
  }

  print "  </select></td>\n";
  print "</tr>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">New NFL Team:</font></td>\n";
  print "<td><select name=f_nfl_new_team><option selected value=\"\">Select a Team\n";
  print "  <option value=\"Ari\">Arizona\n";
  print "  <option value=\"Atl\">Atlanta\n";
  print "  <option value=\"Bal\">Baltimore\n";
  print "  <option value=\"Buf\">Buffalo\n";
  print "  <option value=\"Car\">Carolina\n";
  print "  <option value=\"Chi\">Chicago\n";
  print "  <option value=\"Cin\">Cincinnati\n";
  print "  <option value=\"Cle\">Cleveland\n";
  print "  <option value=\"Dal\">Dallas\n";
  print "  <option value=\"Den\">Denver\n";
  print "  <option value=\"Det\">Detroit\n";
  print "  <option value=\"GB\">Green Bay\n";
  print "  <option value=\"Hou\">Houston\n";
  print "  <option value=\"Ind\">Indianapolis\n";
  print "  <option value=\"Jac\">Jacksonville\n";
  print "  <option value=\"KC\">Kansas City\n";
  print "  <option value=\"Mia\">Miami\n";
  print "  <option value=\"Min\">Minnesota\n";
  print "  <option value=\"NE\">New England\n";
  print "  <option value=\"NO\">New Orleans\n";
  print "  <option value=\"NYG\">New York Giants\n";
  print "  <option value=\"NYJ\">New York Jets\n";
  print "  <option value=\"Oak\">Oakland\n";
  print "  <option value=\"Phi\">Philadelphia\n";
  print "  <option value=\"Pit\">Pittsburgh\n";
  print "  <option value=\"SD\">San Diego\n";
  print "  <option value=\"SF\">San Francisco\n";
  print "  <option value=\"Sea\">Seattle\n";
  print "  <option value=\"StL\">St. Louis\n";
  print "  <option value=\"TB\">Tampa Bay\n";
  print "  <option value=\"Ten\">Tennessee\n";
  print "  <option value=\"Was\">Washington\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}

print end_html();
