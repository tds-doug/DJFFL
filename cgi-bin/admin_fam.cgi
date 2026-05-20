#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'root';
my $password = 'yoda';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $cgi_script = "\/cgi-bin\/ffl_2015\/admin_fam.cgi";
print header();
print start_html("FFL Admin - Free Agent Market");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Free Agent Market Control Page</font></center></h1>\n";

if(param( 'f_player' ))
{
  my $player = param( 'f_player' );
  my $ffl_team = param( 'f_ffl_team' );
  my $start_bid = param( 'f_start_bid' );
  my $winning_bid = param( 'f_winning_bid' );

  my $id;
  my $name;
  my $position;
  my $nfl_team;

  if($player=~m/([A-Za-z]+\. [A-Za-z]+), ([A-Z]+), ([A-Za-z]+)/)
  {
    $name = $1;
    $position = $2;
    $nfl_team = $3;
  }
  elsif($player=~m/([A-Za-z ]+), ([A-Z]+), ([A-Za-z]+)/)
  {
    $name = $1;
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
  print "Starting bid was $start_bid<br>\n";
  print "Winning bid was $winning_bid<br>\n";

  my $sql_upd_players = "update $playerDB set ffl_team = '$ffl_team', contract_yrs = 1, contract_start = 2015 , contract_end = 2015, contract_value = $winning_bid where player = '$name' and nfl_team = '$nfl_team';";
  my $sth_upd_players = $dbh->prepare($sql_upd_players);
  $sth_upd_players->execute();

  my $sql_upd_fam = "insert into free_agent values ('$name','$position','$nfl_team','$ffl_team',$start_bid,$winning_bid);";
#								($round,'$ffl_team','$name','$nfl_team');";
  my $sth_upd_fam = $dbh->prepare($sql_upd_fam);
  $sth_upd_fam->execute();

  my $sql_upd_draft_rank = "update draft_ranking set picked_up = 'Y' where player = \'$name\' and nfl_team = \'$nfl_team\' and position = \'$position\';";
  my $sth_upd_draft_rank = $dbh->prepare($sql_upd_draft_rank);
  $sth_upd_draft_rank->execute();

  print "Player Update sql is $sql_upd_players<p>\n";
  print "FAM sql is $sql_upd_fam<p>\n";
  print "Draft Rank sql is $sql_upd_draft_rank<p>\n";
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

  my $sql_free = "(select player,position,nfl_team from ffl_2015.players_QB where ffl_team = \'\')"
        . " union (select player,position,nfl_team from players_WR where ffl_team = \'\')"
        . " union (select player,position,nfl_team from players_RB where ffl_team = \'\')"
        . " union (select player,position,nfl_team from players_TE where ffl_team = \'\')"
        . " union (select player,position,nfl_team from players_K where ffl_team = \'\')"
        . " union (select player,position,nfl_team from players_DEF where ffl_team = \'\')"
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

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Start Bid:</font></td>\n";
  print "<td><input type=text size = 5 name=f_start_bid value=\"0\"></td>\n";
  print "</tr>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Winning Bid:</font></td>\n";
  print "<td><input type=text size = 5 name=f_winning_bid value=\"0\"></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}

print end_html();
