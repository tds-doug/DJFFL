#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;


my $cgi_script = "\/cgi-bin\/ffl_2015\/free_players.cgi";
my $week = Foozeball::admin_getweek();

print header();
print start_html("Fantasy Football Players");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Nobody Loves These Guys</font></center></h1>\n";
print "<p>\n";

if(param( 'f_playerDB' ))
{

  my $playerDB = param( 'f_playerDB');
  my $order = 'total_pts';
  my $t_order = param( 'f_order');
  my $asc_desc = 'desc';

  if ( ($t_order eq "total_pts") or ($t_order eq "value") )
  {
    $order = $t_order;
    $asc_desc = 'desc';
  }

  if ( ($t_order eq "name") or ($t_order eq 'nfl_team') )
  {
    $order = $t_order;
  }


  print "<table border=\"5\" width=\"100%\">";
  print "<tr>\n";
  print "<td width=\"40%\"><center><a href=\"./free_players.cgi?f_playerDB=$playerDB&f_order=name\"><h3>Player</font></h3></center></td>\n";
  print "<td width=\"15%\"><center><a href=\"./free_players.cgi?f_playerDB=$playerDB&f_order=nfl_team\"><h3>Team</font></h3></center></td>\n";
  print "<td width=\"15%\"><center><a href=\"./free_players.cgi?f_playerDB=$playerDB&f_order=total_pts\"><h3>Points This Season</font></h3></center></td>\n";
  print "<td width=\"15%\"><center><a href=\"./free_players.cgi?f_playerDB=$playerDB&f_order=value\"><h3>CPV</font></h3></center></td>\n";
  print "<td width=\"15%\"><center><h3><font color=\"#FFFF80\">Week $week Opponent</font></h3></center></td>\n";

  print "<tr>\n";

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
  my $sql;

  $sql = "select player,nfl_team,total_pts,value from ffl_2015.$playerDB where ffl_team = '' order by $order $asc_desc;";
  my $sth = $dbh->prepare($sql);
  $sth->execute();

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<tr>\n";
    print "<td width=\"40%\"><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
    print "<td width=\"15%\"><center><img src=\"http://www.djffl.net/images/$row->[1]_h.gif\"></center></td>\n";
    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";

    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">\$$row->[3]</font></center></td>\n";

# SQL that takes the NFL Team from the previous SQL and find the opponent for this week in the nfl_schedule table
      my $column2 = "week" . $week;
      my $sql_opponent = "select $column2 from nfl_schedule where nfl_team = '$row->[1]';";
      my $sth_opponent = $dbh->prepare($sql_opponent);
      $sth_opponent->execute();

## Comment out the following when the NFL schedule is not yet updated to remove
## NFL Opponent from the weekly lineup

      # There should only ever be 1 row that is returned for the previous sql
      while (my $row_opponent = $sth_opponent->fetchrow_arrayref)
      {
        print "      <td width=\"15%\"><center><img src=\"http://www.djffl.net/images/$row_opponent->[0]_l.gif\"</center></td>\n";
      }

## End section to comment out





    print "</tr>\n";
  }

  print "</table>\n";
}
else
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Position:</font></td>\n";
  print "<td><select name=f_playerDB><option selected value=\"\">Select a position\n";
  print "  <option value=\"players_QB\">Quarterbacks\n";
  print "  <option value=\"players_WR\">Wide Recievers\n";
  print "  <option value=\"players_RB\">Running Backs\n";
  print "  <option value=\"players_TE\">Tight Ends\n";
  print "  <option value=\"players_K\">Kickers\n";
  print "  <option value=\"players_DEF\">Defense\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();
