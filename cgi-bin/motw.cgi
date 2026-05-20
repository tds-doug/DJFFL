#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $cgi_script = "\/cgi-bin\/ffl_2015\/motw.cgi";

my $week = Foozeball::getweek();
#my $week = 17;

print header();
print start_html("Fantasy Football Manager of the Week");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Manager of the Week</font></center></h1>\n";

#print "<center><img src=\"http://www.djffl.net/images/motw7_lrg.jpg\">&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;&nbsp\;<img src=\"http://www.djffl.net/images/motw8_lrg.jpg\"></center>\n";
print "<p>\n";

print "<table align=center border=\"5\" width=\"80%\">";
print "<tr>\n";
print "<td><center><h3><font color=\"#FFFF80\">Week</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">MotW</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">Max Points</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">Actual Points</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFF80\">Spread</font></h3></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $i;

my $sql = "select * from motw where week < $week order by week desc;";

my $sth = $dbh->prepare($sql);
$sth->execute();

while(my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td><center><font color=\"#FFFFDF\"><center>$row->[0]</center></font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[2] pts</font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[3] pts</font></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[4] pts</font></center></td>\n";
  print "</tr>\n";
}

print "</table>\n";

print "<p>\n";

print "The Manager of the Week is the manager whose actual point total is as close to their maximum point total for the week.<p>\n";

#pprint "At the end of the season the manager who appears on this list the most times will be declared \"Manager of the Year\" and awarded a \$10 bonus to next season\'s salary cap.<p>\n";
print "There is no \$ associated with the Manager of the Week anymore.  This is merely a smack talking contest now.<p>\n";


print end_html();
