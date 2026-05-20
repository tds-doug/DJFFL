#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

print header();
print start_html("Fantasy Football Managers");

print "<body bgcolor=\"#EEEEFF\" link=\"#004576\" vlink=\"#004576\" alink=\"#004576\">\n";
print "<font face=\"Verdana\">\n";

print "<h1><center>Here Be Ye List of Names</center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"33%\"><center><b>Manager Name</b></center></td>\n";
print "<td width=\"33%\"><center><b>Team Name</b></center></td>\n";
print "<td width=\"33%\"><center><b>Manager Email</b></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $sql = "select * from ffl_2015.managers order by player;";
my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td width=\"33%\">$row->[0]</td>\n";
  print "<td width=\"33%\">$row->[1]</td>\n";
#  print "<td width=\"33%\"><a href=\"mailto:$row->[2]\">$row->[2]</a></td>\n";
  print "<td width=\"33%\"><center>---</center></td>\n";
  print "<tr>\n";
}

print "</table>\n";
print end_html();
