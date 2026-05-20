#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

print header();
print start_html("DJFFL Admin League Snapshot");

my $ffl_manager = Foozeball::get_ffl_mgr($ENV{'REMOTE_USER'});
my $week = Foozeball::getweek();

my $team;
my @teams = (
  'Death To Armenia',
  'A Dingo Ate My Brady',
  'Armenia',
  'Death Blow',
  'Dublin Tundra Wookies',
  'East Bay Gotham Knights',
  'IN DREW BREES WE TRUST',
  'Mantooth Saints',
  'Mr Rodgers Neighborhood',
  'Oklahoma Rednecks',
  'Shiva Blast',
  'The Bam Bam Bigaloes'
);

#my $player_count = 0;

my @positions = ('QB','WR','RB','TE','K','DEF');
my $position;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">2015 League Snapshot</font></center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"9%\" height=\"38\"></td>\n";

# Start of - print the teams across the top of the table
foreach $team (@teams)
{
  print "  <td width=\"11%\" height=\"38\"><center><b><a href=\"./teams.cgi?f_team=$team&f_order=total_pts\">$team</a></b></center></td>\n";
}
print "</tr>\n";
# End of - print the teams across the top of the table

# Start of - print the salary for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">Current<br>Salary</font></center></b></td>\n";

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
# End of - print the salary for each team

# Start of - snapshot spacer
print "<tr><td></td>\n";

foreach $team (@teams)
{
  print "<td></td>\n";
}

print "</tr>\n";
# End of - snapshot spacer

# Start of - print the # of QB's for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">QB\'s</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_QB_count = "select count(*) from players_QB where ffl_team = '$team';";
  my $sth_QB_count = $dbh->prepare($sql_QB_count);
  $sth_QB_count->execute();

  my $row_count = $sth_QB_count->fetchrow_arrayref;

  print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_count->[0]</center></font></td>\n";

}
# End of - print the # of QB's for each team

# Start of - print the # of WR's for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">WR\'s</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_WR_count = "select count(*) from players_WR where ffl_team = '$team';";
  my $sth_WR_count = $dbh->prepare($sql_WR_count);
  $sth_WR_count->execute();

  my $row_count = $sth_WR_count->fetchrow_arrayref;

  print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_count->[0]</center></font></td>\n";

}
# End of - print the # of WR's for each team

# Start of - print the # of RB's for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">RB\'s</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_RB_count = "select count(*) from players_RB where ffl_team = '$team';";
  my $sth_RB_count = $dbh->prepare($sql_RB_count);
  $sth_RB_count->execute();

  my $row_count = $sth_RB_count->fetchrow_arrayref;

  print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_count->[0]</center></font></td>\n";

}
# End of - print the # of RB's for each team

# Start of - print the # of TE's for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">TE\'s</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_TE_count = "select count(*) from players_TE where ffl_team = '$team';";
  my $sth_TE_count = $dbh->prepare($sql_TE_count);
  $sth_TE_count->execute();

  my $row_count = $sth_TE_count->fetchrow_arrayref;

  print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_count->[0]</center></font></td>\n";

}
# End of - print the # of TE's for each team

# Start of - print the # of K's for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">K\'s</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_K_count = "select count(*) from players_K where ffl_team = '$team';";
  my $sth_K_count = $dbh->prepare($sql_K_count);
  $sth_K_count->execute();

  my $row_count = $sth_K_count->fetchrow_arrayref;

  print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_count->[0]</center></font></td>\n";

}
# End of - print the # of K's for each team

# Start of - print the # of DEF's for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">DEF\'s</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_DEF_count = "select count(*) from players_DEF where ffl_team = '$team';";
  my $sth_DEF_count = $dbh->prepare($sql_DEF_count);
  $sth_DEF_count->execute();

  my $row_count = $sth_DEF_count->fetchrow_arrayref;

  print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_count->[0]</center></font></td>\n";

}
# End of - print the # of DEF's for each team

# Start of - print the total # of players for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">Total<br>Players</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_QB_count = "select count(*) from players_QB where ffl_team = '$team';";
  my $sth_QB_count = $dbh->prepare($sql_QB_count);
  $sth_QB_count->execute();
  my $row_count = $sth_QB_count->fetchrow_arrayref;
  my $player_count = int($row_count->[0]);

  my $sql_WR_count = "select count(*) from players_WR where ffl_team = '$team';";
  my $sth_WR_count = $dbh->prepare($sql_WR_count);
  $sth_WR_count->execute();
  $row_count = $sth_WR_count->fetchrow_arrayref;
  $player_count = $player_count + int($row_count->[0]);

  my $sql_RB_count = "select count(*) from players_RB where ffl_team = '$team';";
  my $sth_RB_count = $dbh->prepare($sql_RB_count);
  $sth_RB_count->execute();
  $row_count = $sth_RB_count->fetchrow_arrayref;
  $player_count = $player_count + int($row_count->[0]);

  my $sql_TE_count = "select count(*) from players_TE where ffl_team = '$team';";
  my $sth_TE_count = $dbh->prepare($sql_TE_count);
  $sth_TE_count->execute();
  $row_count = $sth_TE_count->fetchrow_arrayref;
  $player_count = $player_count + int($row_count->[0]);

  my $sql_K_count = "select count(*) from players_K where ffl_team = '$team';";
  my $sth_K_count = $dbh->prepare($sql_K_count);
  $sth_K_count->execute();
  $row_count = $sth_K_count->fetchrow_arrayref;
  $player_count = $player_count + int($row_count->[0]);

  my $sql_DEF_count = "select count(*) from players_DEF where ffl_team = '$team';";
  my $sth_DEF_count = $dbh->prepare($sql_DEF_count);
  $sth_DEF_count->execute();
  $row_count = $sth_DEF_count->fetchrow_arrayref;
  $player_count = $player_count + int($row_count->[0]);

  #print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$player_count</center></font></td>\n";
  if ($player_count < 14)
  {
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$player_count</center></font></td>\n";
  }
  else
  {
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$player_count</center></font></td>\n";
  }
}
print "</tr>\n";
# End of - print the total # of players for each team

# Start of - snapshot spacer
print "<tr><td></td>\n";

foreach $team (@teams)
{
  print "<td></td>\n";
}

print "</tr>\n";
# End of - snapshot spacer

# Start of - print the # of lineup players for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">Lineup<br>Players</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_lineup_count = "select count(*) from lineups where week = '$week' and ffl_team = '$team';";
  my $sth_lineup_count = $dbh->prepare($sql_lineup_count);
  $sth_lineup_count->execute();
  my $row_count = $sth_lineup_count->fetchrow_arrayref;
  my $lineup_count = int($row_count->[0]);

  if ($lineup_count != 14)
  {
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$lineup_count</center></font></td>\n";
  }
  else
  {
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$lineup_count</center></font></td>\n";
  }
}
print "</tr>\n";
# End of - print the # of lineup players for each team

# Start of - print the # of lineup starters for each team
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">Lineup<br>Starters</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_lineup_count = "select count(*) from lineups where week = '$week' and ffl_team = '$team' and starter = 'Y';";
  my $sth_lineup_count = $dbh->prepare($sql_lineup_count);
  $sth_lineup_count->execute();
  my $row_count = $sth_lineup_count->fetchrow_arrayref;
  my $lineup_count = int($row_count->[0]);

  if ($lineup_count != 8)
  {
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$lineup_count</center></font></td>\n";
  }
  else
  {
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$lineup_count</center></font></td>\n";
  }
}
print "</tr>\n";
# End of - print the # of lineup starters for each team

# Start of - snapshot spacer
print "<tr><td></td>\n";

foreach $team (@teams)
{
  print "<td></td>\n";
}

print "</tr>\n";
# End of - snapshot spacer

# Start of - print the total # of wrong elimination picks
print "<tr>\n";
print "  <td width=\"9%\" height=\"19%\"><b><center><font color=\"#FFFFDF\">Elim<br>Bad Picks</font></center></b></td>\n";

foreach $team (@teams)
{
  my $sql_elim_count = "select count(*) from elimination where week >= 1 and win = 'N' and ffl_team = '$team';";
    my $sth_elim_count = $dbh->prepare($sql_elim_count);
    $sth_elim_count->execute();

    my $row_count = $sth_elim_count->fetchrow_arrayref;

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
# End of - print the total # of wrong elimination picks


print "</table>\n";

print end_html();
