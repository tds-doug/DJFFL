#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

print header();
print start_html("Fantasy Football History");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Fantasy Football History</font></center></h1>\n";

print "<table border=\"0\" cellpadding=\"0\" style=\"border-collapse: collapse\" align=\"center\" border=\"5\" width=\"90%\">";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $sql = "select * from history order by number desc;";
my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{

  my $history = $row->[2] . $row->[3] . $row->[4];

  print "<tr>\n";
    print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
    print "<td width=\"90%\"><font color=\"#FFFFDF\">$history</font></td>\n";
  print "</tr>\n";
  print "<tr><td>&nbsp\;</td><td>&nbsp\;</td></tr>\n";
}

print "</table>\n";

print end_html();
