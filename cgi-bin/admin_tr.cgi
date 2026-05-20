#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

print header();
print start_html("Fantasy Football History");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Fantasy Football Transaction Requests</font></center></h1>\n";

my $week = Foozeball::getweek();
#my $week = Foozeball::admin_getweek();

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $sql = "select week,ffl_team,action,player,nfl_team,position,timestamp from transaction_request where week = $week order by number desc;";
my $sth = $dbh->prepare($sql);
$sth->execute();

print "<table border=\"5\" align=\"center\"  width=\"80%\">";
print "<tr>\n";
print "<td><center><b><font color=\"#FFFFDF\">Week</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Action</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Timestamp</font></b></center></td>\n";
print "<tr>\n";

while (my $row = $sth->fetchrow_arrayref)
{

  print "<tr>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[0]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[5]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[6]</font></center></td>\n";
  print "</tr>\n";
}

print "</table>\n";

print end_html();
