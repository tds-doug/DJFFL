#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $week = Foozeball::getweek();
#my $week = 11;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'root';
my $password = 'yoda';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $ffl_team;

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_deactivate.cgi";
print header();
print start_html("FFL Admin - Deactivate Player from Roster");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

sub roundup {
  my $n = shift;
  return(($n == int($n)) ? $n : int($n + 1))
}

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Player Deactivate Control Page</font></center></h1>\n";

if(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  $ffl_team = param( 'f_ffl_team' );

  my $name;
  my $position;
  my $nfl_team;
  my $value;

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

  print "FFL Team is $ffl_team<br>\n";
  print "Player is $name<br>\n";
  print "Position is $position<br>\n";
  print "NFL Team is $nfl_team<br>\n"; 

  my $sql_upd_players = "update $playerDB set ffl_team = '$ffl_team - Injured Reserve'  where player = '$name' and nfl_team = '$nfl_team';";
  my $sth_upd_players = $dbh->prepare($sql_upd_players);
  $sth_upd_players->execute();

  my $sql_get_salary = "select contract_value, value from $playerDB where player = '$name' and nfl_team = '$nfl_team';";
  my $sth_get_salary = $dbh->prepare($sql_get_salary);
  $sth_get_salary->execute();

  while (my $row_salary = $sth_get_salary->fetchrow_arrayref)
  {
    if($row_salary->[0] == 0)
    {
      $value = $row_salary->[1];
    }
    else
    {
      $value = $row_salary->[0];
    }
  }

  my $tmp_ir_value = int($value) / 2;
  my $ir_value = roundup($tmp_ir_value);

  my $sql_insert_ir = "insert into injured_reserve values ('$name','$nfl_team','$position','$ffl_team',$value,$ir_value);";
  my $sth_insert_ir = $dbh->prepare($sql_insert_ir);
  $sth_insert_ir->execute();

  my $sql_get_number = "select count(*) from transactions;";
  my $sth_get_number = $dbh->prepare($sql_get_number);
  $sth_get_number->execute();

  my $row2 = $sth_get_number->fetchrow_arrayref;
  my $number = int($row2->[0]);
  
  my $sql_upd_trans = "insert into transactions values ($week, $number + 1, '$ffl_team','Deactivate','$name','$nfl_team','$position');";
  my $sth_upd_trans = $dbh->prepare($sql_upd_trans);
  $sth_upd_trans->execute();

  my $sql_upd_lineup = "delete from lineups where week >= $week and ffl_team = '$ffl_team' and player = '$name' and nfl_team = '$nfl_team';";
  my $sth_upd_lineup = $dbh->prepare($sql_upd_lineup);
  $sth_upd_lineup->execute();

  print "player sql is $sql_upd_players<p>\n";
  print "ir sql is $sql_insert_ir<p>\n";
  print "trans sql is $sql_upd_trans<p>\n";
  print "lineup sql is $sql_upd_lineup<p>\n";
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
  print "Please select the team you are about to deactivate a player for week <b><font color=\"#FF0000\">$week</font></b>.<p>\n";

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
