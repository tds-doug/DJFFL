#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my @QB = (
  'Peyton Manning',
  'Alex Smith',
  'Drew Brees'
);

my $rank;
my $position;
my $team = 'Death To Armenia';

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

print header();
print start_html("DJ Draft Strategy");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">DJ\'s 2012 Draft Strategy</font></center></h1>\n";

# Begin total positions picked table section
print "<table border=\"5\" width=\"20%\">";
print "<tr>\n";
print "<td width=\"50%\" height=\"38\"><center><b>Postion</b></center></td>\n";
print "<td width=\"50%\" height=\"38\"><center><b>Total Picks</b></center></td>\n";
print "</tr>\n";

# begin position ranking
foreach $position ('QB','WR','RB','TE','K','DEF')
{
  print "<tr>\n";
  print "  <td width=\"50%\" height=\"19%\"><b><font color=\"#FFFFDF\">$position</font></b></td>\n";

  my $playerDB = "players_" . $position;

  my $sql = "select count(*) from $playerDB where ffl_team <> '';";
  my $sth = $dbh->prepare($sql);
  $sth->execute();
  my $row = $sth->fetchrow_arrayref;

  print "<td width=\"50%\" height=\"19\"><font color=\"#FFFFDF\">$row->[0] total picks</font></td>\n";
}
# end position
print "</tr>\n";
print "</table>\n";
# End table

# Begin player ranking table section
print "<table border=\"5\" width=\"33%\">";
print "<tr>\n";
print "<td width=\"20%\" height=\"38\"><center><b>Postion</b></center></td>\n";
print "<td width=\"80%\" height=\"38\"><center><b>Next Pick</b></center></td>\n";
print "</tr>\n";

# begin position ranking
foreach $position ('QB','WR','RB','TE','K','DEF')
{
  print "<tr>\n";
  print "  <td width=\"20%\" height=\"19%\"><b><font color=\"#FFFFDF\">$position</font></b></td>\n";

  my $playerDB = "players_" . $position;

  my $sql = "select player,nfl_team from dj_draft where position = '$position' and ffl_team = '' order by rank asc;";
  my $sth = $dbh->prepare($sql);
  $sth->execute();

  my $row = $sth->fetchrow_arrayref;

  print "<td width=\"80%\" height=\"19\"><font color=\"#FFFFDF\">$row->[0] - $row->[1] - $position</font></td>\n";
}
# end position
print "</tr>\n";
print "</table>\n";
# End  player ranking table

print "<p>\n";

#Begin money section
my $salary = Foozeball::calc_salary($team);

my $money_sql = "select salarycap from managers where ffl_team = '$team';";
my $money_sth = $dbh->prepare($money_sql);
$money_sth->execute();
my $row = $money_sth->fetchrow_arrayref;
my $money_left = $row->[0] - $salary;;

print "<font color=\"#FFFFDF\">Salary Cap: \$$row->[0]</font></b><br>\n";
print "<font color=\"#FFFFDF\">Current Salary: \$$salary</font></b></br>\n";
print "<font color=\"#FFFFDF\">Money Left: \$$money_left</font></b></br>\n";
#End money section

print end_html();
