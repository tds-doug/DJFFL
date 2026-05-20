#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $admin_week = Foozeball::admin_getweek();
my $week = Foozeball::getweek();

print header();
print start_html("FFL Admin - Update Points for a Player");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center>This has better be Doug using this tool.</center></h1>\n";

print "<p>\n";

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_upd_points.cgi";

my $ffl_manager = $ENV{'REMOTE_USER'};

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'root';
my $password = 'yoda';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

if(param( 'f_position'))
{
  my $position = param( 'f_position' );
  my $playerDB = "players_" . $position;
  my $week = param( 'f_week' );
  my $pts_week = "week" . $week . "_pts";

  print  "Position is $position<br>\n";
  print  "PlayerDB is $playerDB<br>\n";
  print  "Week is $week<br>\n";
  print  "Points Week is $pts_week<br>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
  print "<td><select name=f_player_query><option selected value=\"\">Select a Player\n";

  my $sql_get_players = "select player,nfl_team,$pts_week from ffl_2015.$playerDB order by player asc;";
  my $sth_get_players = $dbh->prepare($sql_get_players);
  $sth_get_players->execute();

 while (my $row = $sth_get_players->fetchrow_arrayref)
  {
    my $player_query = "$row->[0], $row->[1], $row->[2]";
    print "  <option value=\"$player_query\">$player_query\n";
  }

  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=hidden name=f_playerDB value=\"$playerDB\">\n";
  print "<input type=hidden name=f_pts_week value=\"$pts_week\">\n";

  print "<input type=submit value=\"Submit\">\n";

}

elsif(param( 'f_player_query' ))
{

  my $player_query = param('f_player_query');
  my $playerDB = param('f_playerDB');
  my $pts_week = param( 'f_pts_week' );

  my $player;
  my $nfl_team;
  my $old_points;

  if($player_query=~m/([A-Za-z \-\.]+), ([A-Za-z]+), ([0-9]+)/)
  {
    $player = Foozeball::db_escape($1);
    $nfl_team = $2;
    $old_points = $3;
  }

  print "Player query is $player_query<br>\n";
  print "PlayerDB is $playerDB<br>\n";
  print "Points Week is $pts_week<br>\n";
  print "Player is $player<br>\n";
  print "NFL Team is $nfl_team<br>\n";
  print "Old Points is $old_points<br>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">New Points:</font></td>\n";
  print "<td><input type=text size = 3 name=f_new_points value=\"$old_points\"></td>\n";
  print "</tr>\n";

  print "</table>\n"; 

  print "<input type=hidden name=f_playerDB value=\"$playerDB\">\n";
  print "<input type=hidden name=f_player value=\"$player\">\n";
  print "<input type=hidden name=f_nfl_team value=\"$nfl_team\">\n";
  print "<input type=hidden name=f_pts_week value=\"$pts_week\">\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
elsif(param( 'f_new_points' ))
{

  my $player = param('f_player');
  my $playerDB = param('f_playerDB');
  my $pts_week = param( 'f_pts_week' );
  my $nfl_team = param('f_nfl_team');
  my $new_points = param( 'f_new_points' );

  print "Player is $player<br>\n";
  print "PlayerDB is $playerDB<br>\n";
  print "Points Week is $pts_week<br>\n";
  print "NFL Team is $nfl_team<br>\n";
  print "New Points is $new_points<p>\n";

  my $sql_upd_points = "update $playerDB set $pts_week = $new_points where player = '$player' and nfl_team = '$nfl_team';";
  my $sth_upd_points = $dbh->prepare($sql_upd_points);
  $sth_upd_points->execute();

  print "Points Update SQL is: $sql_upd_points<br>\n";
}
else # Nothing selected or first time page is loaded
{
  my $ffl_team = Foozeball::get_ffl_team($ffl_manager);
 
  print "The current week is <b><font color=\"#FF0000\">$week</font></b>.\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Position:</font></td>\n";
  print "<td><select name=f_position><option selected value=\"\">Select a position\n";
  print "  <option value=\"QB\">Quarterbacks\n";
  print "  <option value=\"WR\">Wide Recievers\n";
  print "  <option value=\"RB\">Running Backs\n";
  print "  <option value=\"TE\">Tight Ends\n";
  print "  <option value=\"K\">Kickers\n";
  print "  <option value=\"DEF\">Defense\n";
  print "  </select></td>\n";
  print "</tr>\n";

#  print "</table>\n";

#  print "<table>\n";

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
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";

}
print end_html();
