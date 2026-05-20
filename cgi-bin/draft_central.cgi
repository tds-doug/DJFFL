#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

print header();
print start_html("DJFFL Draft Central");

my $ffl_manager = Foozeball::get_ffl_mgr($ENV{'REMOTE_USER'});

my @teams = (
  'Oklahoma Rednecks',
  'Dublin Tundra Wookies',
  'A Dingo Ate My Brady',
  'Mr Rodgers Neighborhood',
  'Death To Armenia',
  'East Bay Gotham Knights',
  'Mantooth Saints',
  'Death Blow',
  'IN DREW BREES WE TRUST',
  'Armenia',
  'Shiva Blast',
  'The Bam Bam Bigaloes'
);

my $round;
my $team;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">2015 Draft Central</font></center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"9%\" height=\"38\"></td>\n";

# print the teams across the top of the table
foreach $team (@teams)
{
  print "  <td width=\"11%\" height=\"38\"><center><b><a href=\"./teams.cgi?f_team=$team&f_order=total_pts\">$team</a></b></center></td>\n";
}
print "</tr>\n";

for ($round = 1; $round <= 10; $round++)
{
  print "<tr>\n";
  print "  <td width=\"9%\" height=\"19%\"><b><font color=\"#FFFFDF\">Round $round</font></b></td>\n";

  foreach $team (@teams)
  {
    my $sql = "select player,nfl_team from draft where round = $round and ffl_team = '$team';";
    my $sth = $dbh->prepare($sql);
    $sth->execute();

    my $row = $sth->fetchrow_arrayref;

    print "  <td width=\"11%\" height=\"19\"><font color=\"#FFFFDF\">$row->[0] - $row->[1]</font></td>\n";
  }
}

print "</tr>\n";

print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><font color=\"#FFFFDF\">Current<br>Salary</font></b></td>\n";

foreach $team (@teams)
{
  my $salary = Foozeball::calc_salary($team);

  my $money_sql = "select salarycap from managers where ffl_team = '$team';";
  my $money_sth = $dbh->prepare($money_sql);
  $money_sth->execute();

  my $row = $money_sth->fetchrow_arrayref;
  my $money_left = $row->[0] - $salary;;

  if ($money_left < 0)
  {
    print "  <td width=\"11%\" height=\"19\"><center><font color=\"#FF0000\">\$$salary<br>(\$$money_left left)</font></center></td>\n";
  }
  else
  {
    print "  <td width=\"11%\" height=\"19\"><center><font color=\"#FFFFDF\">\$$salary<br>(\$$money_left left)</font></center></td>\n";
  }
}

print "</tr>\n";
print "</table>\n";
print "<p>\n";

##########################################################
#
# Begin second part of page
#
##########################################################

# Begin master table
print "<table border=\"0\" width=\"100%\">\n";
print "<tr>\n"; # This should be the only TR for this table

if($ffl_manager eq 'DJ')
{
#  print "<td width=\"66%\">\n"; # Begin TD for draft_ranking table
  print "<td>\n"; # Begin TD for draft_ranking table

  my $rank;
  my $position;
  my $team = 'Death To Armenia';

  # Begin player ranking table section
  print "<table border=\"5\">\n";
  print "  <tr>\n";
  print "    <td width=\"20%\" height=\"38\"><center><b>Position</b></center></td>\n";
  print "    <td width=\"20%\" height=\"38\"><center><b>Rank</b></center></td>\n";
  print "    <td width=\"60%\" height=\"38\"><center><b>Next Pick</b></center></td>\n";
  print "  </tr>\n";

  # begin position ranking
  foreach $position ('QB','WR','RB','TE','K','DEF')
  {
    print "  <tr>\n";
    print "    <td><b><font color=\"#FFFFDF\">$position</font></b></td>\n";

    my $playerDB = "players_" . $position;

    my $sql = "select player,nfl_team,rank from draft_ranking where position = '$position' and picked_up = 'N' order by rank asc;";
    my $sth = $dbh->prepare($sql);
    $sth->execute();

    my $row = $sth->fetchrow_arrayref;

    print "    <td><font color=\"#FFFFDF\">$row->[2]</font></td>\n";
    print "    <td><font color=\"#FFFFDF\">$row->[0] - $row->[1] - $position</font></td>\n";
    print "  </tr>\n";
  }
  # end position
  print "</table>\n";
  # End  player ranking table

  print "</td>\n"; # End TD for draft_ranking table
}

print "<td>\n";

# Begin total positions picked table section
print "<table border=\"5\">\n";
print "  <tr>\n";
print "    <td width=\"50%\" height=\"38\"><center><b>Postion</b></center></td>\n";
print "    <td width=\"50%\" height=\"38\"><center><b>Players Picked Up</b></center></td>\n";
print "  </tr>\n";

# begin position ranking
my $position;

foreach $position ('QB','WR','RB','TE','K','DEF')
{
  print "  <tr>\n";
  print "    <td width=\"50%\" height=\"19%\"><b><font color=\"#FFFFDF\">$position</font></b></td>\n";

  my $playerDB = "players_" . $position;

  my $sql = "select count(*) from $playerDB where ffl_team <> '';";
  my $sth = $dbh->prepare($sql);
  $sth->execute();
  my $row = $sth->fetchrow_arrayref;

  print "    <td width=\"50%\" height=\"19\"><font color=\"#FFFFDF\">$row->[0] players picked up</font></td>\n";
}
# end position
print "  </tr>\n";
print "</table>\n";
# End table

print "</td>\n";


print "</tr>\n";
print "</table>\n";

print end_html();
