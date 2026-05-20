#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $cgi_script = "\/cgi-bin\/ffl_2015\/2012rosters.cgi";

print header();
print start_html("Fantasy Football Rosters");

print "<body bgcolor=\"#EEEEFF\" link=\"#004576\" vlink=\"#004576\" alink=\"#004576\">\n";
print "<font face=\"Verdana\">\n";

print "<h1><center>Here Be Ye Rosters</center></h1>\n";
print "<p>\n";

if(param( 'f_team' ))
{

  my $team = param( 'f_team' );

  print "<center><h3>Roster for $team</h3></center>\n";

  print "<table border=\"5\" width=\"100%\">";
  print "<tr>\n";
  print "<td width=\"20%\"><center><h3>Player</h3></center></td>\n";
  print "<td width=\"15%\"><center><h3>Team</h3></center></td>\n";
  print "<td width=\"15%\"><center><h3>Position</h3></center></td>\n";
  print "<td width=\"20%\"><center><h3>Contracted Thru</h3></center></td>\n";
  print "<td width=\"15%\"><center><h3>Points This Season</h3></center></td>\n";
  print "<td width=\"15%\"><center><h3>Fantasy Salary</h3></center></td>\n";
  print "<tr>\n";

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  my $sql = "(select player,nfl_team,position,contract_end,contract_value,total_pts,value from ffl_2015.players_QB where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value from ffl_2015.players_WR where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value from ffl_2015.players_RB where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value from ffl_2015.players_TE where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value from ffl_2015.players_K where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value from ffl_2015.players_DEF where ffl_team = '$team')"
          . " order by total_pts desc;";

  my $sth = $dbh->prepare($sql);
  $sth->execute();

  my $salary = 0;
  my $count = 0;

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<tr>\n";
    print "<td width=\"20%\"><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
    print "<td width=\"15%\"><center><img src=\"http://www.djffl.net/images/$row->[1]_h.gif\"></center></td>\n";
    print "<td width=\"15%\"><center>$row->[2]</center></td>\n";

    if($row->[3] eq '0')
    {
      print "<td width=\"20%\"><center>Not Under Contract</center></td>\n";
    }
    else
    {
      print "<td width=\"20%\"><center>$row->[3]</center></td>\n";
    }

    print "<td width=\"15%\"><center>$row->[5]</center></td>\n";

    if($row->[4] eq '0')
    {
      print "<td width=\"15%\"><center>\$$row->[6]</center></td>\n";
      $salary = $salary + int($row->[6]);
    }
    else
    {
      print "<td width=\"15%\"><center>\$$row->[4]</center></td>\n";
      $salary = $salary + int($row->[4]);
    }

    $count++;

    print "</tr>\n";

  }

  print "</table>\n";

  print "<p>\n";

  print "$team currently has $count players on the active roster\n";
  print "$team is also being fined by the league for dropping the following players under contract: \n";
  print "<br>\n";

  my $penalty = 0;

  my $sql2 = "select player_name, position, nfl_team, current_penalty from ffl_2015.salary_penalty where ffl_team = '$team';";
  my $sth2 = $dbh->prepare($sql2);
  $sth2->execute();

  while (my $row2 = $sth2->fetchrow_arrayref)
  {

    $penalty = $penalty + int($row2->[3]);

    print "$row2->[0] ($row2->[1] - $row2->[2]) for a penatly of \$$row2->[3]<br>\n";

#    $salary = $salary + $penalty;

#    print "<center>This brings the total salary for $team to $salary</center>\n";
  }
  print "<center><h3>Player Salary for $team: \$$salary</h3></center>\n";
  print "<center><h3>Penalties for $team: \$$penalty</h3></center>\n";
  my $total_salary = $salary + $penalty;
  print "<center><h3>Total Salary for $team: \$$total_salary</h3></center>\n";
}
else
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td>Team:</td>\n";
  print "<td><select name=f_team><option selected value=\"\">Select a Team\n";
  print "  <option value=\"A Dingo Ate My Brady\">A Dingo Ate My Brady\n";
  print "  <option value=\"Armenia\">Armenia\n";
  print "  <option value=\"Oklahoma Rednecks\">Oklahoma Rednecks\n";
  print "  <option value=\"Death Blow\">Death Blow\n";
  print "  <option value=\"Death To Armenia\">Death To Armenia\n";
  print "  <option value=\"Dublin Tundra Wookies\">Dublin Tundra Wookies\n";
  print "  <option value=\"IN DREW BREES WE TRUST\">IN DREW BREES WE TRUST\n";
  print "  <option value=\"East Bay Gotham Knights\">East Bay Gotham Knights\n";
  print "  <option value=\"Mr Rodgers Neighborhood\">Mr Rodgers Neighborhood\n";
  print "  <option value=\"Shiva Blast\">Shiva Blast\n";
  print "  <option value=\"Mantooth Saints\">Mantooth Saints\n";
  print "  <option value=\"The Bam Bam Bigaloes\">The Bam Bam Bigaloes\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();
