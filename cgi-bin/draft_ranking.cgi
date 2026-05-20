#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $ffl_manager = $ENV{'REMOTE_USER'};
my $ffl_team = Foozeball::get_ffl_team($ffl_manager);

print header();
print start_html("Fantasy Football Draft Rankings");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center>Here Be The Players $ffl_team Wants</center></h1>\n";

print "<table align=\"center\" border=\"5\" width=\"40%\">";
print "<tr>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">Ranking</font></b></center></td>\n";
print "<td width=\"50%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">Salary</font></b></center></td>\n";
print "<tr>\n";

my $sql = "select * from ffl_2015.draft_ranking where ffl_team = \'$ffl_team\' and picked_up <> 'Y' order by rank asc;"; 

my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
  print "<td width=\"50%\"><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
  print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";

  my $playerDB = "players_" . $row->[3];
  my $sql2 = "select value from ffl_2015.$playerDB where player = \'$row->[2]\' and nfl_team = \'$row->[4]\';";
  my $sth2 = $dbh->prepare($sql2);
  $sth2->execute();

  while (my $row2 = $sth2->fetchrow_arrayref)
  {
    print "<td width=\"10%\"><center><font color=\"#FFFFDF\">\$$row2->[0]</font></center></td>\n";
  }
  print "<tr>\n";
}

print "</table>\n";
print end_html();
