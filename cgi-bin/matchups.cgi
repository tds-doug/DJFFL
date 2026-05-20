#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $cgi_script = "\/cgi-bin\/ffl_2015\/matchups.cgi";
print header();
print start_html("Fantasy Football Matchups");

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
  my $column = "week" . $week . "_pts";

  print "<center><h1><font color=\"#FFFF80\" face=\"Verdana\">Matchups for Week $week</font></h1></center>\n";
  print "<hr>\n";

  my $sql_matchup = "select ffl_team,opponent from schedule3 where week = '$week' and home_status = 'H';";
  my $sth_matchup = $dbh->prepare($sql_matchup);
  $sth_matchup->execute();

  while (my $row_matchup = $sth_matchup->fetchrow_arrayref)
  {

# Begin week table
    my $home_points = 0;
    my $away_points = 0;
    my $home_team = $row_matchup->[0];
    my $away_team = $row_matchup->[1];
    my $home_mgr;
    my $away_mgr;

    my $sql_home_mgr = "select name from managers where ffl_team = '$home_team';";
    my $sth_home_mgr = $dbh->prepare($sql_home_mgr);
    $sth_home_mgr->execute();
    while (my $row_home_mgr = $sth_home_mgr->fetchrow_arrayref)
    {
      $home_mgr = $row_home_mgr->[0];
    }

    my $sql_away_mgr = "select name from managers where ffl_team = '$away_team';";
    my $sth_away_mgr = $dbh->prepare($sql_away_mgr);
    $sth_away_mgr->execute();
    while (my $row_away_mgr = $sth_away_mgr->fetchrow_arrayref)
    {
      $away_mgr = $row_away_mgr->[0];
    }


    print "<table border=\"0\" align=\"center\" width=\"90%\">\n";
    print "<tr>\n";
    print "<td><center><h3><font color=\"#FFFFDF\">$home_team - $home_mgr</font></h3></center></td>\n";
    print "<td><center><h3><font color=\"#FFFFDF\">$away_team - $away_mgr</font></h3></center></td>\n";
    print "</tr>\n";
    print "<td>\n";

# Begin home team table
    print "  <table border=\"1\" align=\"center\" width=\"100%\">\n";
    print "    <tr>\n";
    print "      <td width=\"20%\"><center><b><font color=\"#FFFFDF\">Postion</font></b></center></td>\n";
    print "      <td width=\"40%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
    print "      <td width=\"20%\"><center><b><font color=\"#FFFFDF\">Team</font></b></center></td>\n";
    print "      <td width=\"20%\"><center><b><font color=\"#FFFFDF\">Points</font></b></center></td>\n";
    print "    </tr>\n";

    $home_points = $home_points + Foozeball::get_player_stats($home_team, 'QB', $week);
    $home_points = $home_points + Foozeball::get_player_stats($home_team, 'WR', $week);
    $home_points = $home_points + Foozeball::get_player_stats($home_team, 'RB', $week);
    $home_points = $home_points + Foozeball::get_player_stats($home_team, 'TE', $week);
    $home_points = $home_points + Foozeball::get_player_stats($home_team, 'K', $week);
    $home_points = $home_points + Foozeball::get_player_stats($home_team, 'DEF', $week);

    print "  </table>\n";
    # End home team table

    print "</td>\n";
    print "<td>\n";

    # Begin away team table
    print "  <table border=\"1\" align=\"center\" width=\"100%\">\n";
    print "    <tr>\n";
    print "      <td width=\"20%\"><center><b><font color=\"#FFFFDF\">Postion</font></b></center></td>\n";
    print "      <td width=\"40%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
    print "      <td width=\"20%\"><center><b><font color=\"#FFFFDF\">Team</font></b></center></td>\n";
    print "      <td width=\"20%\"><center><b><font color=\"#FFFFDF\">Points</font></b></center></td>\n";
    print "    </tr>\n";

    $away_points = $away_points + Foozeball::get_player_stats($away_team, 'QB', $week);
    $away_points = $away_points + Foozeball::get_player_stats($away_team, 'WR', $week);
    $away_points = $away_points + Foozeball::get_player_stats($away_team, 'RB', $week);
    $away_points = $away_points + Foozeball::get_player_stats($away_team, 'TE', $week);
    $away_points = $away_points + Foozeball::get_player_stats($away_team, 'K', $week);
    $away_points = $away_points + Foozeball::get_player_stats($away_team, 'DEF', $week);

    print "  </table>\n";
   # End away team table

    print "</td>\n";
    print "</tr>\n";

    print "<tr>\n";
    print "<td><center><h3><font color=\"#FFFFDF\">Total Points: $home_points</font></h3></center></td>\n";
    print "<td><center><h3><font color=\"#FFFFDF\">Total Points: $away_points</font></h3></center></td>\n";
    print "</tr>\n";

    print "</table>\n";
    # End week table  

    print "<hr>\n";
  }
}
else
{
  print "<h1><center><font color=\"#FFFF80\" face=\"Verdana\">Choose Ye Matchups</font></center></h1>\n";
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
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();

