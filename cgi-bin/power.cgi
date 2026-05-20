#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $cgi_script = "\/cgi-bin\/ffl_2015\/power.cgi";
print header();
print start_html("Fantasy Football Power Matchups");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

if(param( 'f_week' ))
{

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';
  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  my $week = param( 'f_week');
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

  my $team;

  print "<center><h1><font color=\"#FFFF80\" face=\"Verdana\">Here Be Ye Power Scores</font></h1></center>\n";

  print "<table border=\"5\" width=\"100%\">";
  print "<tr>\n";
  print "<td width=\"12%\" height=\"38\"></td>\n";

  # print the teams across the top of the table
  foreach $team (@teams)
  {
    print "<td width=\"11%\" height=\"38\"><center><b><a href=\"./teams.cgi?f_team=$team&f_order=total_pts\">$team</a></b></center></td>\n";
  }
  print "</tr>\n";

  # Begin section to print out values for regular formation
  print "<tr>\n";
  print "  <td width=\"12%\" height=\"19%\"><b><font color=\"#FFFFDF\">Regular</font></b></td>\n";

  foreach $team (@teams)
  {
    my $formation_pts = 0;

    $formation_pts = $formation_pts + get_points($team, 'QB', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'WR', $week, 2);
    $formation_pts = $formation_pts + get_points($team, 'RB', $week, 2);
    $formation_pts = $formation_pts + get_points($team, 'TE', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'K', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'DEF', $week, 1);

    print "<td width=\"11%\" height=\"19\"><center><font color=\"#FFFFDF\">$formation_pts</font></center></td>\n";

 }

  print "</tr>\n";

  # Begin section to print out values for red gun formation
  print "<tr>\n";
  print "  <td width=\"12%\" height=\"19%\"><b><font color=\"#FFFFDF\">Red Gun</font></b></td>\n";

  foreach $team (@teams)
  {
    my $formation_pts = 0;

    $formation_pts = $formation_pts + get_points($team, 'QB', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'WR', $week, 3);
    $formation_pts = $formation_pts + get_points($team, 'RB', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'TE', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'K', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'DEF', $week, 1);

    print "<td width=\"11%\" height=\"19\"><center><font color=\"#FFFFDF\">$formation_pts</font></center></td>\n";

 }

  print "</tr>\n";

  # Begin section to print out values for run and shoot formation
  print "<tr>\n";
  print "  <td width=\"12%\" height=\"19%\"><b><font color=\"#FFFFDF\">Run and Shoot</font></b></td>\n";

  foreach $team (@teams)
  {
    my $formation_pts = 0;

    $formation_pts = $formation_pts + get_points($team, 'QB', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'WR', $week, 4);
    $formation_pts = $formation_pts + get_points($team, 'RB', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'K', $week, 1);
    $formation_pts = $formation_pts + get_points($team, 'DEF', $week, 1);

    print "<td width=\"11%\" height=\"19\"><center><font color=\"#FFFFDF\">$formation_pts</font></center></td>\n";

 }

  print "</tr>\n";
  # End run and shoot section

  # Begin section to get the actual points that a team got for the week
  print "<tr>\n";
  print "  <td width=\"12%\" height=\"19%\"><b><font color=\"#FFFFDF\">Actual Points Scored</font></b></td>\n";
  
  foreach $team (@teams)
  {
    my $sql_actual = "select sum(points) from lineups where week = $week and ffl_team = '$team' and starter = 'Y';";

    my $sth_actual = $dbh->prepare($sql_actual);
    $sth_actual->execute();

    while(my $row_actual = $sth_actual->fetchrow_arrayref)
    {
      print "<td width=\"11%\" height=\"19\"><center><font color=\"#FFFFDF\">$row_actual->[0]</font></center></td>\n";
    }
  } 

  # End section to get actual points

  print "</table><p>\n";

  print "A power score is the score you would recieve had you played your best lineup.  This allows you to see just how badly you screwed up for a given week, and to let people see just who is really dominating as opposed to just getting lucky.\n";
}
else
{
  print "<h1><center><font color=\"#FFFF80\" face=\"Verdana\">Choose A Week</font></center></h1>\n";
  print "<p>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Week:</font></td>\n";
  print "<td><select name=f_week><option selected value=\"\">Select a week\n";
  print "  <option value=\"1\">Week 1\n";
  print "  <option value=\"2\">Week 2\n";
  print "  <option value=\"3\">Week 3\n";
  print "  <option value=\"4\">Week 4\n";
  print "  <option value=\"5\">Week 5\n";
  print "  <option value=\"6\">Week 6\n";
  print "  <option value=\"7\">Week 7\n";
  print "  <option value=\"8\">Week 8\n";
  print "  <option value=\"9\">Week 9\n";
  print "  <option value=\"10\">Week 10\n";
  print "  <option value=\"11\">Week 11\n";
  print "  <option value=\"12\">Week 12\n";
  print "  <option value=\"13\">Week 13\n";
  print "  <option value=\"14\">Week 14\n";
  print "  <option value=\"15\">Week 15\n";
  print "  <option value=\"16\">Week 16\n";
  print "  <option value=\"17\">Week 17\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";
  
  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
} 

print end_html();

sub get_points{

  my $ffl_team = $_[0];
  my $position = $_[1];
  my $week = $_[2]; 
  my $num_players = $_[3];
    
  my $points = 0;

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';
  my $dbh_points = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  my $sql_points = "select points from lineups where week = $week and ffl_team = '$ffl_team' and position = '$position' order by points desc limit $num_players;";
  my $sth_points = $dbh_points->prepare($sql_points);
  $sth_points->execute();

  while(my $row_points = $sth_points->fetchrow_arrayref)
  {
    $points = $points + int($row_points->[0]);
  }
  return($points);
}
