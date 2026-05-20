#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $cgi_script = "\/cgi-bin\/ffl_2015\/teams.cgi";

print header();
print start_html("Fantasy Football Rosters");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

if(param( 'f_team' ))
{

  my $team = param( 'f_team' );
  my $order = param( 'f_order');
  my $asc_desc = 'asc';

  if ( ($order eq "total_pts") or ($order eq "value") or ($order eq 'contract_end') )
  {
    $asc_desc = 'desc';
  }

  print "<h1><center>$team</center></h1>\n";
  print "<p>\n";

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  my $sql_mgr = "select * from managers where ffl_team = '$team';";
  my $sth_mgr = $dbh->prepare($sql_mgr);
  $sth_mgr->execute();

  my $row = $sth_mgr->fetchrow_arrayref;

  print "<center><h3>Managed by <a href=mailto:$row->[2]>$row->[0]</a></h3></center>\n";

  print "<center><h3>Active Roster</h3></center>\n";

  print "<table border=\"5\" width=\"100%\">";
  print "<tr>\n";
  print "<td width=\"20%\"><center><a href=\"./teams.cgi?f_team=$team&f_order=player\"><h3>Player</h3></a></center></td>\n";
  print "<td width=\"10%\"><center><a href=\"./teams.cgi?f_team=$team&f_order=nfl_team\"><h3>Team</h3></a></center></td>\n";
  print "<td width=\"10%\"><center><a href=\"./teams.cgi?f_team=$team&f_order=position\"><h3>Position</h3></a></center></td>\n";
  #print "<td width=\"10%\"><center><a href=\"./teams.cgi?f_team=$team&f_order=position\"><h3>Bye Week</h3></a></center></td>\n";
  print "<td width=\"10%\"><center><font color=\"#FFFF80\"><h3>NFL Bye Week</h3></font></center></td>\n";
  print "<td width=\"20%\"><center><a href=\"./teams.cgi?f_team=$team&f_order=contract_end\"><h3>Contracted Thru</h3></a></center></td>\n";
  print "<td width=\"15%\"><center><a href=\"./teams.cgi?f_team=$team&f_order=total_pts\"><h3>Points This Season</h3></a></center></td>\n";
  print "<td width=\"15%\"><center><a href=\"./teams.cgi?f_team=$team&f_order=value\"><h3>Fantasy Value</h3></a></center></td>\n";
  print "<tr>\n";

  my $sql = "(select player,nfl_team,position,contract_end,contract_value,total_pts,value,franchise_player from ffl_2015.players_QB where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value,franchise_player from ffl_2015.players_WR where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value,franchise_player from ffl_2015.players_RB where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value,franchise_player from ffl_2015.players_TE where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value,franchise_player from ffl_2015.players_K where ffl_team = '$team')"
          . " union (select player,nfl_team,position,contract_end,contract_value,total_pts,value,franchise_player from ffl_2015.players_DEF where ffl_team = '$team')"
          . " order by $order $asc_desc;";

  my $sth = $dbh->prepare($sql);
  $sth->execute();

  my $salary = 0;
  my $count = 0;

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<tr>\n";
    print "<td width=\"20%\"><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
    print "<td width=\"10%\"><center><img src=\"http://www.djffl.net/images/$row->[1]_h.gif\"></center></td>\n";
#    print "<td width=\"15%\"><center><img src=\"http://192.168.1.175/images/$row->[1]_h.gif\"></center></td>\n";
    print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";

    # Begin section to list bye week
    my $sql_bye_week = "select * from nfl_schedule where nfl_team = '$row->[1]'";
    my $sth_bye_week = $dbh->prepare($sql_bye_week);
    $sth_bye_week->execute();

    my $bye_week;
    while (my $row_bye_week = $sth_bye_week->fetchrow_arrayref)
    {
      for ($bye_week = 1; $bye_week <= 13; $bye_week++)
      {
        if($row_bye_week->[$bye_week] eq '')
        {
          print "<td width=\"10%\"><center>$bye_week</center></td>\n";
        }
      }
    }
    # End section to list bye week




    if($row->[3] eq '0')
    {
      print "<td width=\"20%\"><center><font color=\"#FFFFDF\">Not Under Contract</font></center></td>\n";
    }
    else
    {
      if($row->[7] eq 'Y')
      {
      print "<td width=\"20%\"><center><font color=\"#FFFFDF\">$row->[3]<br>Franchise Player</font></center></td>\n";
      }
      else
      {
      print "<td width=\"20%\"><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";
      }
    }

    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">$row->[5]</font></center></td>\n";

    if($row->[4] eq '0')
    {
      print "<td width=\"15%\"><center><font color=\"#FFFFDF\">\$$row->[6]</font></center></td>\n";
      $salary = $salary + int($row->[6]);
    }
    else
    {
      # Print the salary being paid first, then the CPV in ()'s
      print "<td width=\"15%\"><center><font color=\"#FFFFDF\">\$$row->[4] (\$$row->[6])</font></center></td>\n";
      $salary = $salary + int($row->[4]);
    }

    $count++;

    print "</tr>\n";

  }

  print "</table>\n";

  print "<p>\n";

  print "<font face=\"Verdana\" color=\"#FFFFDF\"><center>$team currently has $count players on their active roster.</center></font><br>\n";
  print "<font face=\"Verdana\" color=\"#FFFFDF\"><center>The \$ displayed is the salary you are paying.  If the player is under contract then the \$ in ()'s indicates the player's CPV for this season.  If you sort on value realize it sorts by the \$ in the ()'s.</center></font><br>\n";
  print "<hr><p>\n";


  print "<table width=\"100%\">";
  print "<tr>\n";

  print "<td>\n";
  print "<h3><font face=\"Verdana\" color=\"#FFFFDF\"><center>Non-Active Roster</center></font></h3><p>\n";
  print "</td>\n";
  print "<td>\n";
  print "<h3><font face=\"Verdana\" color=\"#FFFFDF\"><center>Salary Penalties</center></font></h3><p>\n";
  print "</td>\n";
  print "</tr>\n";

# Injured Reserve Section
  print "<td>\n";
  my $ir_count = 0;

  print "<table align=\"center\" border=\"2\" width=\"50%\">";
  print "<tr>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Player</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Team</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Position</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Fantasy Salary</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">IR Salary</font></h3></center></td>\n";
  print "<tr>\n";

  my $sql_ir = "select player,  nfl_team, position, original_salary, injury_salary from ffl_2015.injured_reserve where ffl_team = '$team';";
  my $sth_ir = $dbh->prepare($sql_ir);
  $sth_ir->execute();

  while (my $row = $sth_ir->fetchrow_arrayref)
  { 
    print "<tr>\n";
    print "<td><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
    print "<td><center><img src=\"http://www.djffl.net/images/$row->[1]_h.gif\"></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">\$$row->[3]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">\$$row->[4]</font></center></td>\n";
    print "</tr>\n";

    $salary = $salary + int($row->[4]);
    $ir_count++;
  }
  
  print "</table>\n";

  print "</td>\n";
# End Injured ReserveSection


# Salary Penalty Section
  print "<td>\n";
  my $penalty_count = 0;
  my $penalty = 0;

  print "<table align=\"center\" border=\"2\" width=\"50%\">";
  print "<tr>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Player</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Team</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Position</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Contracted Through</font></h3></center></td>\n";
  print "<td><center><h3><font color=\"#FFFFDF\">Contract Terminated</font></h3></center></td>\n";
  print "<tr>\n";

  my $sql_penalty = "select player_name,  nfl_team, position, contract_end, contract_terminated,current_penalty from ffl_2015.salary_penalty where ffl_team = '$team';";
  my $sth_penalty = $dbh->prepare($sql_penalty);
  $sth_penalty->execute();

  while (my $row = $sth_penalty->fetchrow_arrayref)
  { 
    print "<tr>\n";
    print "<td><center><a href=\"./search.cgi?f_player=$row->[0]\">$row->[0]</a></center></td>\n";
    print "<td><center><img src=\"http://www.djffl.net/images/$row->[1]_h.gif\"></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
    print "</tr>\n";

    $penalty = $penalty + int($row->[5]);
    $penalty_count++;
  }
  
  print "</table>\n";
  print "</td>\n";
# End SalaryPenalty Section

print "</tr>\n";
print "<tr>";
# Summary section for IR and Salary Penalty
  print "<td>\n";
  print "<font face=\"Verdana\" color=\"#FFFFDF\"><center>$team currently has $ir_count players on their non-active roster.</center></font>\n";
  print "</td>\n";
  print "<td>\n";
  print "<font face=\"Verdana\" color=\"#FFFFDF\"><center>$team currently is paying a penalty on $penalty_count players.</center></font>\n";
  print "</td>\n";

  print "</tr>\n";
  print "</table>\n";

  print "<hr><p>\n";

  
#
# End Salary Penalty Section
#

  my $total_expenses = $salary + $penalty;
  my $remaining_funds = int($row->[3]) - $total_expenses;

#  print "<center><h3>Player Salary for $team: \$$salary</h3></center>\n";
#  print "<center><h3>Penalties for $team: \$$penalty</h3></center>\n";
#  print "<center><h3>Total Salary for $team: \$$total_expenses</h3></center>\n";


# Begin Team Finances Section

#  print "<center><h3>The Bank of America Team Finance Center</h3></center>\n";
  print "<center><h3>The <img src=\"http://www.djffl.net/images/wells_fargo.gif\"> Team Finance Center</h3></center>\n";

  print "<table align=\"center\" border=\"2\" width=\"60%\">";

  print "<tr>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">Salary Cap</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">Player Salaries</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">Penalties</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">Total Expenses</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">Remaining Funds</font></center></td>\n";
  print "</tr>\n";

  print "<tr>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">\$$row->[3]</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">\$$salary</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">\$$penalty</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">\$$total_expenses</font></center></td>\n";
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">\$$remaining_funds</font></center></td>\n";
  print "</tr>\n";

  print "</table>\n";


# End Team Finances Section
}
else
{
  print "<center><h1>&nbsp;</h1></center>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Team:</font></td>\n";
  print "<td><select name=f_team><option selected value=\"\">Select a Team\n";
  print "  <option value=\"A Dingo Ate My Brady\">A Dingo Ate My Brady - Courtney Castillo\n";
  print "  <option value=\"Armenia\">Armenia - Jason Keledjian\n";
  print "  <option value=\"Death Blow\">Death Blow - Prashanth Charapalli\n";
  print "  <option value=\"Death To Armenia\">Death To Armenia - Doug Johnson\n";
  print "  <option value=\"Dublin Tundra Wookies\">Dublin Tundra Wookies - Jake Garris\n";
  print "  <option value=\"IN DREW BREES WE TRUST\">IN DREW BREES WE TRUST - Shannon Patel\n";
  print "  <option value=\"East Bay Gotham Knights\">East Bay Gotham Knights - Shay Patel\n";
  print "  <option value=\"Mr Rodgers Neighborhood\">Mr Rodgers Neighborhood - Cortney Johnson\n";
  print "  <option value=\"Shiva Blast\">Shiva Blast - Eric Foster\n";
  print "  <option value=\"Mantooth Saints\">Mantooth Saints - Paul Etcheverry\n";
  print "  <option value=\"Oklahoma Rednecks\">Oklahoma Rednecks - Brandon Butler\n";
  print "  <option value=\"The Bam Bam Bigaloes\">The Bam Bam Bigaloes - Patrick Balzan\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=hidden name=f_order value=total_pts>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();
