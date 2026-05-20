#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $week = Foozeball::getweek();
my $year = Foozeball::getyear();

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'root';
my $password = 'yoda';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $ffl_team;

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_upd_contract.cgi";
print header();
print start_html("FFL Admin - Update Contract for a Player");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

sub roundup
{
  my $n = shift;
  return(($n == int($n)) ? $n : int($n + 1))
}

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Player Contract Control Page</font></center></h1>\n";

if(param( 'f_contract_yrs' ))
{
  my $player = param( 'f_player' );
  my $ffl_team = param( 'f_ffl_team' );
  my $nfl_team = param( 'f_nfl_team' );
  my $position = param( 'f_position' );
  my $contract_yrs = param( 'f_contract_yrs' );;
  my $contract_value = param( 'f_contract_value' );;
  my $contract_start;
  my $contract_end;

  my $playerDB = "players_" . $position;

  print "Player is $player<br>\n";
  print "FFL Team is $ffl_team<br>\n";
  print "Position is $position<br>\n";
  print "NFL Team is $nfl_team<p>\n";

  if($contract_yrs eq '1')
  {
    $contract_start = $year;
    $contract_end = $year;
  }
  elsif($contract_yrs eq '2')
  {
    $contract_start = $year;
    $contract_end = $year +1;
  }
  elsif($contract_yrs eq '3')
  {
    $contract_start = $year;
    $contract_end = $year +2;
  }

  my $sql_upd_contract = "update $playerDB set contract_yrs = $contract_yrs, contract_start = $contract_start, contract_end = $contract_end, contract_value = $contract_value  where player = '$player' and ffl_team = '$ffl_team' and nfl_team = '$nfl_team';";
  my $sth_upd_contract = $dbh->prepare($sql_upd_contract);
  $sth_upd_contract->execute();

  print "Contract years is $contract_yrs<br>\n";
  print "Contract start is $contract_start<br>\n";
  print "Contract end is $contract_end<br>\n";
  print "Contract value is \$$contract_value<br>\n";
  print "Contract SQL is $sql_upd_contract<p>\n";

  print "Click <a href=\"./search.cgi?f_player=$player\">here</a> to see the player stats<br>\n";
  print "Click <a href=\"./teams.cgi?f_team=$ffl_team&f_order=total_pts\">here</a> to see FFL Team\n";



}
elsif(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  $ffl_team = param( 'f_ffl_team' );

  my $name;

  my $position;
  my $nfl_team;
  my $value;

  if($player=~m/([A-Za-z \-\.]+), ([A-Z]+), ([A-Za-z]+)/)
  {
    $name = Foozeball::db_escape($1);
    $position = $2;
    $nfl_team = $3;
  }

  chomp($name);
  chomp($position);
  chomp($nfl_team);

  my $playerDB = "players_" . $position;

  my $sql_get_contract = "select contract_yrs, contract_start, contract_end, contract_value, value from $playerDB where player = '$name' and nfl_team = '$nfl_team';";
  my $sth_get_contract = $dbh->prepare($sql_get_contract);
  $sth_get_contract->execute();

  my $row = $sth_get_contract->fetchrow_arrayref;

  print "FFL Team is $ffl_team<br>\n";
  print "Player is $name<br>\n";
  print "Position is $position<br>\n";
  print "NFL Team is $nfl_team<br>\n"; 
  print "Current Value is $row->[4]<p>\n";

  if( $row->[0] ne '0')
  { 
    print "Contract Years is <font color=\"#FF0000\">$row->[0]</font><br>\n";
    print "Contract Start is <font color=\"#FF0000\">$row->[1]</font><br>\n";
    print "Contract End is <font color=\"#FF0000\">$row->[2]</font><br>\n";
    print "Contract Value is <font color=\"#FF0000\">$row->[3]</font><br>\n";
  }
  else
  { 
    print "Contract Years is $row->[0]<br>\n";
    print "Contract Start is $row->[1]<br>\n";
    print "Contract End is $row->[2]<br>\n";
    print "Contract Value is $row->[3]<br>\n";
  }

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Contract Years:</font></td>\n";
  print "<td><select name=f_contract_yrs><option selected value=\"\">Select Years\n";
  print "  <option value=\"1\">1\n";
  print "  <option value=\"2\">2\n";
  print "  <option value=\"3\">3\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Contract Value:</font></td>\n";
  print "<td><input type=text size = 64 name=f_contract_value value=\"$row->[4]\"></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=hidden name=f_ffl_team value=\"$ffl_team\">\n";
  print "<input type=hidden name=f_player value=\"$name\">\n";
  print "<input type=hidden name=f_position value=\"$position\">\n";
  print "<input type=hidden name=f_nfl_team value=\"$nfl_team\">\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
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

  my $sql_players = "(select player, position, nfl_team from ffl_2015.players_QB where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_WR where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_RB where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_TE where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_K where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_DEF where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.players_DEF where ffl_team = '$ffl_team')"
        . " union (select player, position, nfl_team from ffl_2015.injured_reserve where ffl_team = '$ffl_team')"
        . " order by player asc;";

  my $sth_players = $dbh->prepare($sql_players);
  $sth_players->execute();

  while (my $row = $sth_players->fetchrow_arrayref)
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
  print "Please select the team you are about to sign a player to a contract for.<p>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Team:</font></td>\n";
  print "<td><select name=f_ffl_team><option selected value=\"\">Select a Team\n";
  print "  <option value=\"A Dingo Ate My Brady\">A Dingo Ate My Brady\n";
  print "  <option value=\"Armenia\">Armenia\n";
  print "  <option value=\"Death Blow\">Death Blow\n";
  print "  <option value=\"Death To Armenia\">Death To Armenia\n";
  print "  <option value=\"Dublin Tundra Wookies\">Dublin Tundra Wookies\n";
  print "  <option value=\"East Bay Gotham Knights\">East Bay Gotham Knights\n";
  print "  <option value=\"Mr Rodgers Neighborhood\">Mr Rodgers Neighborhood\n";
  print "  <option value=\"IN DREW BREES WE TRUST\">IN DREW BREES WE TRUST\n";
  print "  <option value=\"Shiva Blast\">Shiva Blast\n";
  print "  <option value=\"Mantooth Saints\">Mantooth Saints\n";
  print "  <option value=\"Oklahoma Rednecks\">Oklahoma Rednecks\n";
  print "  <option value=\"The Bam Bam Bigaloes\">The Bam Bam Bigaloes\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}





print end_html();
