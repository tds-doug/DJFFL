#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_pbp.cgi";
print header();
print start_html("Fantasy Football Players");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center>Here Be Ye List of Players</center></h1>\n";
print "<p>\n";

if(param( 'f_team' ))
{

  my $team = param( 'f_team' );
  my $playerDB = param( 'f_playerDB');

  print "<table border=\"5\" width=\"100%\">";
  print "<tr>\n";
  print "<td width=\"25%\"><center><h3><font color=\"#FFFFDF\">Player</font></h3></center></td>\n";
  print "<td width=\"25%\"><center><h3><font color=\"#FFFFDF\">Team</font></h3></center></td>\n";
  print "<td width=\"25%\"><center><h3><font color=\"#FFFFDF\">Points This Season</font></h3></center></td>\n";
  print "<td width=\"25%\"><center><h3><font color=\"#FFFFDF\">Fantasy Salary</font></h3></center></td>\n";
  print "<tr>\n";

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
  my $sql;

  if($team eq 'all_players')
  {
    $sql = "select player,ffl_team,total_pts,value from ffl_2015.$playerDB order by value desc;";
  }
  elsif($team eq 'all_teams')
  {
    $sql = "select player,ffl_team,total_pts,value from ffl_2015.$playerDB where ffl_team <> '' order by value desc;";
  } 
  else
  {
    $sql = "select player,ffl_team,total_pts,value from ffl_2015.$playerDB where ffl_team = '$team' order by value desc;";
  }

  my $sth = $dbh->prepare($sql);
  $sth->execute();

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<tr>\n";
    print "<td width=\"25%\"><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
    print "  <td><center><a href=\"./teams.cgi?f_team=$row->[1]\">$row->[1]</a></center></td>\n";
    print "<td width=\"25%\"><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
    print "<td width=\"25%\"><center><font color=\"#FFFFDF\">\$$row->[3]</font></center></td>\n";
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

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Team:</font></td>\n";
  print "<td><select name=f_team><option selected value=\"\">Select a Team\n";
  print "  <option value=\"all_players\">All NFL Players\n";
  print "  <option value=\"all_teams\">All FFL Teams\n";
  print "  <option value=\"Armenia\">Armenia\n";
  print "  <option value=\"Oklahoma Rednecks\">Oklahoma Rednecks\n";
  print "  <option value=\"Death Blow\">Death Blow\n";
  print "  <option value=\"Death To Armenia\">Death To Armenia\n";
  print "  <option value=\"East Bay Gotham Knights\">East Bay Gotham Knights\n";
  print "  <option value=\"Mr Rodgers Neighborhood\">Mr Rodgers Neighborhood\n";
  print "  <option value=\"Mantooth Saints\">Mantooth Saints\n";
  print "  <option value=\"The Bam Bam Bigaloes\">The Bam Bam Bigaloes\n";
  print "  <option value=\"IN DREW BREES WE TRUST\">IN DREW BREES WE TRUST\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();
