#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $week;

print header();
print start_html("NFL Bye Weeks");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Bye Weeks for the NFL Teams</font></center></h1>\n";

print "<table border=\"5\" align=\"center\" width=\"80%\">";
print "<tr>\n";

print "<tr>\n";

for ($week = 4; $week <= 11; $week++)
{
  my $column = "week" . $week;

  my $sql = "select nfl_team from nfl_schedule where $column = '';";
  my $sth = $dbh->prepare($sql);
  $sth->execute();

  print "<tr>\n";
  print "<td width=\"10%\"><center>Week $week</center></td>\n";

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<td><center><img src=\"http://www.djffl.net/images/$row->[0].gif\"</center></td>\n";
  }
  print "<tr>\n";
}

print "</table>\n";

print end_html();
