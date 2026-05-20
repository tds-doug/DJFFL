#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $week = 1;

my @teams = (
  'A Dingo Ate My Brady',
  'Armenia',
  'Death Blow',
  'Death To Armenia',
  'Dublin Tundra Wookies',
  'East Bay Gotham Knights',
  'Mr Rodgers Neighborhood',
  'IN DREW BREES WE TRUST',
  'Shiva Blast',
  'Mantooth Saints',
  'Oklahoma Rednecks',
  'The Bam Bam Bigaloes'
);

my $i;
my $team;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $ffl_team;
my $ffl_manager = $ENV{'REMOTE_USER'};
my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_elimination.cgi";

print header();
print start_html("FFL Admin - Elimination Challeng");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">2012 Elimination Challenge</font></center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"12%\" height=\"38\"></td>\n";

# print the teams across the top of the table
foreach $team (@teams)
{
  print "<td width=\"11%\"><center><b><a href=\"./teams.cgi?f_team=$team&f_order=total_pts\">$team</a></b></center></td>\n";
}
print "</tr>\n";

# Get the total wrong picks
print "<tr>\n";
print "  <td><font color=\"#FFFFDF\"><center>Tally</center></font></b></td>\n";

foreach $team (@teams)
{
  my $sql_count = "select count(*) from elimination where week >= 1 and win = 'N' and ffl_team = '$team';";
    my $sth_count = $dbh->prepare($sql_count);
    $sth_count->execute();

    my $row_count = $sth_count->fetchrow_arrayref;

    if ($row_count->[0] < 5)
    {
      print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_count->[0]</center></font></td>\n";
    }
    else
    {
      print "<td><center><img src=\"http://www.djffl.net/images/Crying.gif\"></center></td>\n";
    }
}

print "</tr>\n";


print "</table>\n";

print end_html();
