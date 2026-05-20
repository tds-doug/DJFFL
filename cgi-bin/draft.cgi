#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

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

print header();
print start_html("Fantasy Football Draft Results");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">2015 Draft Results</font></center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"9%\" height=\"38\"></td>\n";

# print the teams across the top of the table
foreach $team (@teams)
{
  print "<td width=\"11%\" height=\"38\"><center><b><a href=\"./teams.cgi?f_team=$team&f_order=total_pts\">$team</a></b></center></td>\n";
}
print "</tr>\n";

for ($round = 1; $round <= 13; $round++)
{
  print "<tr>\n";
  print "  <td width=\"9%\" height=\"19%\"><b><font color=\"#FFFFDF\">Round $round</font></b></td>\n";

  foreach $team (@teams)
  {
    my $sql = "select player,nfl_team from draft where round = $round and ffl_team = '$team';";
    my $sth = $dbh->prepare($sql);
    $sth->execute();

    my $row = $sth->fetchrow_arrayref;

    print "<td width=\"11%\" height=\"19\"><font color=\"#FFFFDF\">$row->[0] - $row->[1]</font></td>\n";
  }
}

print "</tr>\n";
print "</table>\n";

print "<p>\n";
#print "<center>Click <a href=\"http://www.djffl.net/ffl_2015/2013DraftChat.txt\">here</a> for the transcript of the draft day chat</center>\n";

print end_html();
