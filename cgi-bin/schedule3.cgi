#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $cgi_script = "\/cgi-bin\/ffl_2015\/schedule3.cgi";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $ffl_manager = $ENV{'REMOTE_USER'};
my $ffl_team = Foozeball::get_ffl_team($ffl_manager);;
my $week = 1;
my $wins = 0;
my $losses = 0;

print header();
print start_html("Fantasy Football Schedule");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">2014 Schedule For $ffl_team</font></center></h1>\n";
print "<p>\n";

print "<table align=center border=\"5\" width=\"80%\">";
print "<tr>\n";
print "<td><center><h3><font color=\"#FFFFDF\">Week</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFFDF\">Your Team</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFFDF\">Your Score</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFFDF\">Opponent</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFFDF\">Opponent Score</font></h3></center></td>\n";
print "<td><center><h3><font color=\"#FFFFDF\">Win or Loss</font></h3></center></td>\n";
print "<tr>\n";


for($week; $week<=17; $week++)
{

  my $sql = "select * from schedule3 where week = $week and ffl_team = '$ffl_team';";
  my $sth = $dbh->prepare($sql);
  $sth->execute();

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<tr>\n";
    print "<td><center><font color=\"#FFFFDF\"><center>$week</center></font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[5]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[7]</font></center></td>\n";
    print "</tr>\n";

    if ($row->[7] eq 'W')
    {
      $wins++;
    }
    elsif ($row->[7] eq 'L')
    {
      $losses++;
    }
  }
}

print "</table>\n";
print "<p>\n";
print "<center>You have $wins wins and $losses losses.</center>\n";
print end_html();
