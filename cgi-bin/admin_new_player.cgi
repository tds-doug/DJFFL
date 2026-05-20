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

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_new_player.cgi";
print header();
print start_html("FFL Admin - Add Player");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Add a Player Control Page</font></center></h1>\n";

if(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  my $position = param( 'f_position' );
  my $nfl_team = param( 'f_nfl_team' );
  my $value = param( 'f_value' );

  if($player=~m/([A-Za-z \-\.\']+)/)
  {
    my $name = Foozeball::db_escape($1);
    $player = $name;
  }

  chomp($player);
  chomp($position);
  chomp($nfl_team);
  chomp($value);


  my $playerDB = "players_" . $position;

  print "Player is $player<br>\n";
  print "Position is $position<br>\n";
  print "NFL Team is $nfl_team<br>\n"; 
  print "Value is $value <br>\n";

  my $sql_insert_player = "insert into $playerDB values (\'$player\',\'$nfl_team\',\'\',0,0,0,0,\'$position\',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,$value,'N',0);";
  my $sth_insert_player = $dbh->prepare($sql_insert_player);
  $sth_insert_player->execute();

  print "Player insert sql is $sql_insert_player<p>\n";
}
else  
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
  print "<td><input type=text size = 64 name=f_player value=\"Enter name here\"></td>\n";
  print "</tr>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Position:</font></td>\n";
  print "<td><select name=f_position><option selected value=\"\">Select a Position\n";
  print "  <option value=\"QB\">Quarterback\n";
  print "  <option value=\"WR\">Wide Receiver\n";
  print "  <option value=\"RB\">Running Back\n";
  print "  <option value=\"TE\">Tight End\n";
  print "  <option value=\"K\">Kicker\n";
  print "  <option value=\"DEF\">Defence\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">NFL Team:</font></td>\n";
  print "<td><select name=f_nfl_team><option selected value=\"\">Select a Team\n";
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

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Value:</font></td>\n";
  print "<td><input type=text size = 5 name=f_value value=\"0\"></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}

print end_html();
