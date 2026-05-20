#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

# Create subroutine to get total season points
sub season_points{

  my $season_pts = 0;

  my $sql_pts = "select * from lineups where ffl_team = '$_[0]' and starter = 'Y';";
  my $sth_pts = $dbh->prepare($sql_pts);
  $sth_pts->execute();

  while (my $row = $sth_pts->fetchrow_arrayref)
  {
    $season_pts = $season_pts + int($row->[6]);
  }

  print "  <td width=\"16%\"><center><font color=\"#FFFFDF\">$season_pts</font></center></td>\n";
  print "<tr>\n";

}

# End subroutine season_points

# Create subroutine to get team standings
sub standings{

  #my $sql_teams = "select ffl_team, conference, wins, losses, percentage, current_streak, conf_wins, conf_losses, conf_percentage, morale from standings where conference = '$_[0]' order by standing asc;";
  my $sql_teams = "select ffl_team, conference, wins, losses, percentage, current_streak, conf_wins, conf_losses, conf_percentage, morale from standings where conference = '$_[0]' order by standing,percentage desc;";

  my $sth_teams = $dbh->prepare($sql_teams);

  $sth_teams->execute();

  while (my $row = $sth_teams->fetchrow_arrayref)
  {
    print "<tr>\n";

# Print the team name
    print "  <td width=\"26%\"><a href=\"./teams.cgi?f_team=$row->[0]&f_order=total_pts\">$row->[0]</a></td>\n";

# Print the League Record
    print "  <td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[2] - $row->[3]</font></center></td>\n";

# Print the Team Morale
    print "  <td width=\"6%\"><center><img src=\"http://www.djffl.net/images/$row->[9].gif\"></center></td>\n";

#    my $percentage = int($row->[4]) / 1000;
#    print "  <td width=\"10%\"><center><font color=\"#FFFFDF\">$percentage</font></center></td>\n";
    print "  <td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";

    print "  <td width=\"14%\"><center><font color=\"#FFFFDF\">$row->[6] - $row->[7]</font></center></td>\n";

    print "  <td width=\"14%\"><center><font color=\"#FFFFDF\">$row->[5]</font></center></td>\n";

    season_points($row->[0]);
  }

}
# End soubroutine to get team standings

print header();
print start_html("Fantasy Football Standings");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">DJFFL Standings</font></center></h1>\n";

# Begin Northern Conference
print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Northern Conference</font></center></h3>\n";

print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";
print "  <td width=\"26%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">League Record</font></b></center></td>\n";
print "  <td width=\"6%\"><center><b><font color=\"#FFFFDF\">Team Morale</font></b></center></td>\n";
print "  <td width=\"10%\"><center><b><font color=\"#FFFFDF\">Winning %</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Conference Record</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Current Streak</font></b></center></td>\n";
print "  <td width=\"16%\"><center><b><font color=\"#FFFFDF\">Season Points</font></b></center></td>\n";
print "<tr>\n";

standings('Northern');

print "</table>\n";
# End Northern Conference

print "<p>\n";
 
# Begin Western Conference
print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Western Conference</font></center></h3>\n";

print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";
print "  <td width=\"26%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">League Record</font></b></center></td>\n";
print "  <td width=\"6%\"><center><b><font color=\"#FFFFDF\">Team Morale</font></b></center></td>\n";
print "  <td width=\"10%\"><center><b><font color=\"#FFFFDF\">Winning %</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Conference Record</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Current Streak</font></b></center></td>\n";
print "  <td width=\"16%\"><center><b><font color=\"#FFFFDF\">Season Points</font></b></center></td>\n";
print "<tr>\n";

standings('Western');

print "</table>\n";
# End Western Conference

# Begin Eastern Conference
print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Eastern Conference</font></center></h3>\n";

print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";
print "  <td width=\"26%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">League Record</font></b></center></td>\n";
print "  <td width=\"6%\"><center><b><font color=\"#FFFFDF\">Team Morale</font></b></center></td>\n";
print "  <td width=\"10%\"><center><b><font color=\"#FFFFDF\">Winning %</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Conference Record</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Current Streak</font></b></center></td>\n";
print "  <td width=\"16%\"><center><b><font color=\"#FFFFDF\">Season Points</font></b></center></td>\n";
print "<tr>\n";

standings('Eastern');

print "</table>\n";
# End Eastern Conference

print "<p>\n";

# Begin Southern Conference 
print "<h3><center><font face=\"Verdana\" color=\"#FFFF80\">Southern Conference</font></center></h3>\n";

print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";
print "  <td width=\"26%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">League Record</font></b></center></td>\n";
print "  <td width=\"6%\"><center><b><font color=\"#FFFFDF\">Team Morale</font></b></center></td>\n";
print "  <td width=\"10%\"><center><b><font color=\"#FFFFDF\">Winning %</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Conference Record</font></b></center></td>\n";
print "  <td width=\"14%\"><center><b><font color=\"#FFFFDF\">Current Streak</font></b></center></td>\n";
print "  <td width=\"16%\"><center><b><font color=\"#FFFFDF\">Season Points</font></b></center></td>\n";
print "<tr>\n";

standings('Southern');

print "</table>\n";
# End Southern Conference

print "<p>\n";
print "<center>A <img src=\"http://www.djffl.net/images/Cool.gif\"> indicates conference winner</center>\n";
print "<center>A <img src=\"http://www.djffl.net/images/BigSmile.gif\"> indicates clinched playoff spot</center>\n";
print "<center>A <img src=\"http://www.djffl.net/images/Happy.gif\"> indicates still in the hunt</center>\n";
print "<center>A <img src=\"http://www.djffl.net/images/Scared.gif\"> indicates fear of elimination</center>\n";
print "<center>A <img src=\"http://www.djffl.net/images/Crying.gif\"> indicates eliminated from the playoffs</center>\n";

print end_html();
