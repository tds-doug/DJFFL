#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $cgi_script = "\/cgi-bin\/ffl_2015\/zombie.cgi";

#my $week = Foozeball::getweek();
my $week = 14;

print header();
print start_html("Fantasy Football Zombie Kill of the Week");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

#print "<center><img src=\"http://www.djffl.net/images/zombie7_lrg.jpg\"><font size=\"10\" face=\"Verdana\" color=\"#FFFF80\"><b>Zombie Kill of the Week</b></font><img src=\"http://www.djffl.net/images/zombie8_lrg.jpg\"></center>\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Zombie Kills of the Week</font></center></h1>\n";
print "<center><img src=\"http://www.djffl.net/images/zombie7_lrg.jpg\">&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;<img src=\"http://www.djffl.net/images/zombie8_lrg.jpg\"></center>\n";
print "<p>\n";

print "<table align=center border=\"5\" width=\"80%\">";
print "<tr>\n";
print "<td><center><h3><font color=\"#FFFF80\">Week</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">Killer</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">Killee</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">Score</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">Killed By</font></h3></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $i;

my $sql = "select * from zombie_kills where week < $week order by week desc;";

my $sth = $dbh->prepare($sql);
$sth->execute();

while(my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td><center><font color=\"#FFFFDF\"><center>$row->[0]</center></font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[4] pts</font></center></td>\n";
  print "</tr>\n";
}

print "</table>\n";

print "<p>\n";

print "The Zombie Kill of the Week is the score that has the biggest point differential for the week.<p>\n";

print "At the end of the season the manager who appears on this list the most times as the killer will be declared \"Zombie Killer of the Year\".<p>\n";
print "At the end of the season the manager who appears on this list the most times as the killee will be declared \"Zombie Killee of the Year\".<p>\n";

print end_html();
