#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

print header();
print start_html("Fantasy Football Waiver Priority");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">If You Are On This List You Won A Player Who Probably Didn\'t Work Out For You</font></center></h1>\n";

print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Waiver Pickups</font></center></h3>\n";
print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";
print "<td><center><b><font color=\"#FFFFDF\">Week</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Winning Team</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFFDF\">Other Interested Teams</font></b></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $sql = "select * from ffl_2015.waivers order by week desc;"; 

my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[0]</font></center></td>\n";
  print "<td><center><a href=\"./search.cgi?f_player=$row->[1]\">$row->[1]</a></center></td>\n";
  print "<td><center><img src=\"http://www.djffl.net/images/$row->[2]_h.gif\"</center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";
  print "<td><center><a href=\"./teams.cgi?f_team=$row->[4]&f_order=total_pts\">$row->[4]</a></center></td>\n";
  print "<td><center><font color=\"#FFFFDF\">$row->[5]</font></center></td>\n";
  print "<tr>\n";
}

print "</table>\n";

print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Current Waiver Priority List</font></center></h3>\n";

print "<table align=\"center\" border=\"5\" width=\"60%\">";
print "<tr>\n";
print "  <td width=\"20%\"><center><b><font color=\"#FFFFDF\">Waiver Priority</font></b></center></td>\n";
print "  <td width=\"80%\"><center><b><font color=\"#FFFFDF\">Team Name</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">1</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">The Bam Bam Bigaloes</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">2</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">IN DREW BREES WE TRUST</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">3</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Mr Rodgers Neighborhood</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">4</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">A Dingo Ate My Brady</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">5</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Oklahoma Rednecks</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">6</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Mantooth Saints</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">7</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">East Bay Gotham Knights</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">8</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Death Blow</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">9</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Armenia</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">10</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Death To Armenia</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">11</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Dublin Tundra Wookies</font></b></center></td>\n";
print "</tr>\n";
print "<tr>\n";
print "  <td width=\"20%\"><center><font color=\"#FFFFDF\">12</font></center></td>\n";
print "  <td width=\"80%\"><center><font color=\"#FFFFDF\">Shiva Blast</font></b></center></td>\n";
print "</tr>\n";

print "</table>\n";

print end_html();
