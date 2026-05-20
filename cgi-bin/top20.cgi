#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

print header();
print start_html("Fantasy Football Top Point Scorers");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">If You Do Not Have Someone On This List Then You Suck</font></center></h1>\n";

print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Top 20 Players</font></center></h3>\n";
print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">Points This Season</font></b></center></td>\n";
print "<tr>\n";

my $sql = "(select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_QB)"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_WR)"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_RB)"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_TE)"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_K)"
        . " order by total_pts desc limit 20;"; 

my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td width=\"20%\"><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
  print "<td width=\"10%\"><center><img src=\"http://www.djffl.net/images/$row->[1]_h.gif\"</center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
  print "<td width=\"25%\"><center><a href=\"./teams.cgi?f_team=$row->[3]&f_order=total_pts\">$row->[3]</a></center></td>\n";
  print "<td width=\"25%\"><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
  print "<tr>\n";
}

print "</table>\n";

print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Top 12 Defenses</font></center></h3>\n";

my $sql_DEF = "select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_DEF order by total_pts desc limit 12;";
my $sth_DEF = $dbh->prepare($sql_DEF);
$sth_DEF->execute();

print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">Points This Season</font></b></center></td>\n";
print "<tr>\n";

while (my $row_DEF = $sth_DEF->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td width=\"20%\"><center><a href=\"./search.cgi?f_player=$row_DEF->[0]\">$row_DEF->[0]</a></center></td>\n";
  print "<td width=\"10%\"><center><img src=\"http://www.djffl.net/images/$row_DEF->[1]_h.gif\"</center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">$row_DEF->[2]</font></center></td>\n";
  print "<td width=\"25%\"><center><a href=\"./teams.cgi?f_team=$row_DEF->[3]&f_order=total_pts\">$row_DEF->[3]</a></center></td>\n";
  print "<td width=\"25%\"><center><font color=\"#FFFFDF\">$row_DEF->[4]</font></center></td>\n";
  print "<tr>\n";
}
print "</table>\n";
print end_html();
