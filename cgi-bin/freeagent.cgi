#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

print header();
print start_html("Fantasy Football Free Agent Market");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Here Be Ye List of Free Agents Picked Up</font></center></h1>\n";

print "<table align=\"center\" border=\"5\" width=\"80%\">";
print "<tr>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<td width=\"35%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">Salary</font></b></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $sql = "select * from free_agent order by winning_bid desc;";
my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
    print "<td width=\"20%\"><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
    print "<td width=\"15%\"><center><img src=\"http://www.djffl.net/images/$row->[2]_h.gif\"></center></td>\n";
    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
    print "<td width=\"35%\"><center><a href=\"./teams.cgi?f_team=$row->[3]&f_order=total_pts\">$row->[3]</a></center></td>\n";
    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">\$$row->[5]</font></center></td>\n";
  print "<tr>\n";
}

print "</table>\n";

print "<p>\n";
#print "<center>Click <a href=\"http://www.djffl.net/ffl_2015/2013DraftChat.txt\">here</a> for the transcript of the draft day chat</center>\n";
print end_html();
