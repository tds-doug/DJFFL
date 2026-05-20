#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $week = Foozeball::getweek();
#my $week = 1;
my $i;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'root';
my $password = 'yoda';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_add.cgi";
print header();
print start_html("FFL Admin - Add Player to Roster");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Player Add Control Page</font></center></h1>\n";
print "You are adding a player for week <b><font color=\"#FF0000\">$week</font></b><p>\n";

if(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  my $ffl_team = param( 'f_ffl_team' );

  my $name;
  my $position;
  my $nfl_team;

  my $sql_upd_lineup;

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

  my $sql_upd_players = "update $playerDB set ffl_team = '$ffl_team'  where player = '$name' and nfl_team = '$nfl_team';";
  my $sth_upd_players = $dbh->prepare($sql_upd_players);
  $sth_upd_players->execute();

  my $sql_get_number = "select count(*) from transactions;";
  my $sth_get_number = $dbh->prepare($sql_get_number);
  $sth_get_number->execute();

  my $row2 = $sth_get_number->fetchrow_arrayref;
  my $number = int($row2->[0]);
  
  my $sql_upd_trans = "insert into transactions values ($week, $number + 1, '$ffl_team','Add','$name','$nfl_team','$position');";
  my $sth_upd_trans = $dbh->prepare($sql_upd_trans);
  $sth_upd_trans->execute();

# The following will only insert 1 row into lineups for the current week.  To change this 
# for the rest of the regular season change the $i <= $week to $i <= 13

  for ($i = $week; $i <= $week; $i++) # Playoff line
#  for ($i = $week; $i <= 13; $i++)    # Regular season line
  {
    $sql_upd_lineup = "insert into lineups values ('$ffl_team', $i, '$position', '$name', '$nfl_team', 'N', 0);";
    my $sth_upd_lineup = $dbh->prepare($sql_upd_lineup);
    $sth_upd_lineup->execute();
  }

  print "player sql is $sql_upd_players<p>\n";
  print "trans sql is $sql_upd_trans<p>\n";
  print "lineup sql is $sql_upd_lineup<p>\n";
}
else  
{
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

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
  print "<td><select name=f_player><option selected value=\"\">Select a Player\n";

  my $sql_free = "(select player,position,nfl_team from ffl_2015.players_QB where ffl_team = '')"
        . " union (select player,position,nfl_team from players_WR where ffl_team = '')"
        . " union (select player,position,nfl_team from players_RB where ffl_team = '')"
        . " union (select player,position,nfl_team from players_TE where ffl_team = '')"
        . " union (select player,position,nfl_team from players_K where ffl_team = '')"
        . " union (select player,position,nfl_team from players_DEF where ffl_team = '')"
        . " order by player asc;";

  my $sth_free = $dbh->prepare($sql_free);
  $sth_free->execute();

  while (my $row = $sth_free->fetchrow_arrayref)
  {
    my $result = "$row->[0], $row->[1], $row->[2]";
    print "  <option value=\"$result\">$result\n";
  }

  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}

print end_html();
