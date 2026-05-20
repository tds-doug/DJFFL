#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $week = Foozeball::getweek();
my $year = Foozeball::getyear();
#my $week = 11;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'root';
my $password = 'yoda';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $ffl_team;

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_drop.cgi";
print header();
print start_html("FFL Admin - Drop Player from Roster");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Player Drop Control Page</font></center></h1>\n";

if(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  $ffl_team = param( 'f_ffl_team' );

  my $name;
  my $position;
  my $nfl_team;

  if($player=~m/([A-Za-z \'\-\.]+), ([A-Z]+), ([A-Za-z]+)/)
  {
    $name = Foozeball::db_escape($1);
    $position = $2;
    $nfl_team = $3;
  }

  chomp($name);
  chomp($position);
  chomp($nfl_team);

  my $playerDB = "players_" . $position;
  my $isFranchisePlayer = "N";

  print "FFL Team is $ffl_team<br>\n";
  print "Player is $name<br>\n";
  print "Position is $position<br>\n";
  print "NFL Team is $nfl_team<br>\n"; 

  my $sql_chk_franchise = "select franchise_player from $playerDB where player = '$name' and nfl_team = '$nfl_team';";
  my $sth_chk_franchise = $dbh->prepare($sql_chk_franchise);
  $sth_chk_franchise->execute();

  while (my $row = $sth_chk_franchise->fetchrow_arrayref)
  {
    $isFranchisePlayer = $row->[0];
  }

  if ($isFranchisePlayer eq "Y")
  {
    print "Unable to drop player.  $player is a franchise player.\n";
  }
  else
  {
    my $sql_chk_penalty = "select contract_start,contract_end,contract_value from $playerDB where player = '$name' and nfl_team = '$nfl_team';";
    my $sth_chk_penalty = $dbh->prepare($sql_chk_penalty);
    $sth_chk_penalty->execute();

    while (my $row = $sth_chk_penalty->fetchrow_arrayref)
    {
      my $contract_start = int($row->[0]);
      my $contract_end = int($row->[1]);
      my $contract_value = int($row->[2]);
      my $penalty;

      if ( ($contract_end - $year) == 0)
      {
        $penalty =  2;
      }
      elsif ( ($contract_end - $year) == 1)
      {
        $penalty =  4;
      }
      elsif ( ($contract_end - $year) == 2)
      {
        $penalty =  6;
      }
      print "PENALTY IS \$$penalty<p>\n";

      if ($penalty != 0)
      {
        my $sql_upd_penalty = "insert into salary_penalty values ('N','$ffl_team','$name','$position','$nfl_team',$contract_start,$contract_end,$year,$contract_value,$penalty);";
        my $sth_upd_penalty = $dbh->prepare($sql_upd_penalty);
        $sth_upd_penalty->execute();
        print "Update salary_penalty sql is $sql_upd_penalty<p>\n";
      }
    }

    my $sql_upd_players = "update $playerDB set ffl_team = '', contract_yrs = 0, contract_start = 0, contract_end = 0, contract_value = 0  where player = '$name' and nfl_team = '$nfl_team';";
    my $sth_upd_players = $dbh->prepare($sql_upd_players);
    $sth_upd_players->execute();
    print "Update player sql is $sql_upd_players<p>\n";

    my $sql_get_number = "select count(*) from transactions;";
    my $sth_get_number = $dbh->prepare($sql_get_number);
    $sth_get_number->execute();

    my $row2 = $sth_get_number->fetchrow_arrayref;
    my $number = int($row2->[0]);
  
    my $sql_upd_trans = "insert into transactions values ($week, $number + 1, '$ffl_team','Drop','$name','$nfl_team','$position');";
    my $sth_upd_trans = $dbh->prepare($sql_upd_trans);
    $sth_upd_trans->execute();
    print "Update transactions sql is $sql_upd_trans<p>\n";

    my $sql_upd_lineup = "delete from lineups where week >= $week and ffl_team = '$ffl_team' and player = '$name' and nfl_team = '$nfl_team';";
    my $sth_upd_lineup = $dbh->prepare($sql_upd_lineup);
    $sth_upd_lineup->execute();
    print "Update lineup sql is $sql_upd_lineup<p>\n";
  }
}
elsif(param( 'f_ffl_team' ))  
{
  $ffl_team = param( 'f_ffl_team' );

  print "The following players are on $ffl_team<p>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
  print "<td><select name=f_player><option selected value=\"\">Select a Player\n";

  my $sql_drop = "(select player, position, nfl_team from ffl_2015.players_QB where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_WR where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_RB where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_TE where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_K where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_DEF where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from injured_reserve where ffl_team = '$ffl_team')"
        . " order by player asc;";

  my $sth_drop = $dbh->prepare($sql_drop);
  $sth_drop->execute();

  while (my $row = $sth_drop->fetchrow_arrayref)
  {
    my $result = "$row->[0], $row->[1], $row->[2]";
    print "  <option value=\"$result\">$result\n";
  }

  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=hidden name=f_ffl_team value=\"$ffl_team\">\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
} 
else
{
  print "Please select the team you are about to drop a player for week <b><font color=\"#FF0000\">$week</font></b>.<p>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Team:</font></td>\n";
  print "<td><select name=f_ffl_team><option selected value=\"\">Select a Team\n";
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
