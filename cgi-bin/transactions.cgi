#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

print header();
print start_html("Fantasy Football Transactions");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Here Be Ye List of Transactions</font></center></h1>\n";

my $sql_count = "select count(*) from transactions;";
my $sth_count = $dbh->prepare($sql_count);
$sth_count->execute();

while (my $row_count = $sth_count->fetchrow_arrayref)
{
  print "<center><h3>So far there have been a total of $row_count->[0] transactions this season!!!</h3></center>\n";
}

print "<table align=\"center\" border=\"5\" width=\"80%\">";
print "<tr>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">Week</font></b></center></td>\n";
print "<td width=\"30%\"><center><b><font color=\"#FFFFDF\">Team Name</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">Action</font></b></center></td>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<tr>\n";

my $sql = "select * from ffl_2015.transactions order by number desc;";
my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
    print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[0]</font></center></td>\n";
    print "<td width=\"30%\"><center><a href=\"./teams.cgi?f_team=$row->[2]&f_order=total_pts\">$row->[2]</a></center></td>\n";
    print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";
    print "<td width=\"20%\"><center><a href=\"./search.cgi?f_player=$row->[4]\">$row->[4]</a></center></td>\n";
    print "<td width=\"15%\"><center><img src=\"http://www.djffl.net/images/$row->[5]_h.gif\"></center></td>\n";
    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">$row->[6]</font></center></td>\n";
  print "<tr>\n";
}

print "</table>\n";

print "<p>\n";

print end_html();
