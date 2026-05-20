#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

print header();
print start_html("Fantasy Football Franchise Players");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Players We Are In Love With</font></center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "<td width=\"25%\"><center><b><font color=\"#FFFFDF\">Points This Season</font></b></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $sql = "(select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_QB where franchise_player = 'Y')"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_WR where franchise_player = 'Y')"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_RB where franchise_player = 'Y')"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_TE where franchise_player = 'Y')"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_K where franchise_player = 'Y')"
        . " union (select player,nfl_team,position,ffl_team,total_pts from ffl_2015.players_DEF where franchise_player = 'Y')"
        . " order by total_pts desc;"; 

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
print end_html();
