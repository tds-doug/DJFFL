#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Time::Local;
use POSIX qw(strftime);
use Foozeball;

my $week = Foozeball::admin_getweek();
#my $week = 17;

print header();
print start_html("Fantasy Football Transaction Request");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";


my $cgi_script = "\/cgi-bin\/ffl_2015\/trans_req.cgi";

my $ffl_manager = $ENV{'REMOTE_USER'};

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

sub your_moves{
# Begin Your Moves for Week # Section
  print "<h1><center>Your Moves for Week $week</center></h1>\n";

  print "<table align=\"center\" border=\"5\" width=\"60%\">";
  print "<tr>\n";
  print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">Action</font></b></center></td>\n";
  print "<td width=\"35%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
  print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">NFL Team</font></b></center></td>\n";
  print "<td width=\"15%\"><center><b><font color=\"#FFFFDF\">Position</font></b></center></td>\n";
  print "<td width=\"20%\"><center><b><font color=\"#FFFFDF\">Number of Requests</font></b></center></td>\n";
  print "<tr>\n";

  my $sql_trans = "select action, player, nfl_team, position from transaction_request where week = $week and ffl_team = '$_[0]' order by number desc;";
  my $sth_trans = $dbh->prepare($sql_trans);
  $sth_trans->execute;

  while (my $row = $sth_trans->fetchrow_arrayref)
  {
    print "<tr>\n";
    print "<td width=\"15%\"><font color=\"#FFFFDF\">$row->[0]</font></td>\n";

# Player bit
    print "<td width=\"35%\"><center><a href=\"./search.cgi?f_player=$row->[1]\">$row->[1]</a></center></td>\n";

    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
    print "<td width=\"15%\"><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";

# Number teams requesting bit

    my $sql_num = "select count(*) from transaction_request where week = $week and action = 'add' and player = '$row->[1]';";
    my $sth_num = $dbh->prepare($sql_num);
    $sth_num->execute;
    my $row_num = $sth_num->fetchrow_arrayref;
    print "<td width=\"20%\"><center><font color=\"#FFFFDF\">$row_num->[0]</font></center></td>\n";
#    my $count = int($row_num->[0]);

    print "<tr>\n";
  }

  print "</table>\n";
# End Your Moves for Week # Section
}

if(param( 'f_player'))
{
  my $ffl_team = param('f_ffl_team');
  my $action = param( 'f_action' );
  my $player = param( 'f_player' );
  my $player_l = param( 'f_player_l' );

  my @c_time = (localtime);
  my $currenttime = timelocal(@c_time);
  my $transactiontime = strftime "%e %b %Y %k:%M:%S", @c_time;

  my $name;
  my $position;
  my $nfl_team;
  my $name_l;
  my $position_l;
  my $nfl_team_l;

  if($player=~m/([A-Za-z \'\-\.]+), ([A-Z]+), ([A-Za-z]+)/)
  {
    $name = Foozeball::db_escape($1);
    $position = $2;
    $nfl_team = $3;
  }

  chomp($name);
  chomp($position);
  chomp($nfl_team);

  if($player_l=~m/([A-Za-z \-\.]+), ([A-Z]+), ([A-Za-z]+)/)
  {
    $name_l = Foozeball::db_escape($1);
    $position_l = $2;
    $nfl_team_l = $3;
  }

  chomp($name_l);
  chomp($position_l);
  chomp($nfl_team_l);

  my $sql_count = "select count(*) from transaction_request;";
  my $sth_count = $dbh->prepare($sql_count);
  $sth_count->execute;
  my $row_count = $sth_count->fetchrow_arrayref;
  my $count = int($row_count->[0]);

  if($action eq 'Add')
  {
    my $sql_add = "insert into transaction_request values ($week, $count +1, '$ffl_team', 'Add', '$name','$nfl_team','$position', '$transactiontime');";
    my $sth_add = $dbh->prepare($sql_add);
    $sth_add->execute;
  }

  elsif($action eq 'Drop')
  {
    my $sql_drop = "insert into transaction_request values ($week, $count +1, '$ffl_team', 'Drop', '$name','$nfl_team','$position', '$transactiontime');";
    my $sth_drop = $dbh->prepare($sql_drop);
    $sth_drop->execute;
  }

  elsif($action eq 'Activate')
  {
    my $sql_activate = "insert into transaction_request values ($week, $count +1, '$ffl_team', 'Activate', '$name','$nfl_team','$position', '$transactiontime');";
    my $sth_activate = $dbh->prepare($sql_activate);
    $sth_activate->execute;
  }

  elsif($action eq 'Deactivate')
  {
    my $sql_deactivate = "insert into transaction_request values ($week, $count +1, '$ffl_team', 'Deactivate', '$name','$nfl_team','$position', '$transactiontime');";
    my $sth_deactivate = $dbh->prepare($sql_deactivate);
    $sth_deactivate->execute;
  }

  elsif($action eq 'Link')
  {
    my $sql_add = "insert into transaction_request values ($week, $count +1, '$ffl_team', 'Add', '$name','$nfl_team','$position', '$transactiontime');";
    my $sth_add = $dbh->prepare($sql_add);
    $sth_add->execute;

    my $sql_linked_drop = "insert into transaction_request values ($week, $count +2, '$ffl_team', 'Linked Drop', '$name_l','$nfl_team_l','$position_l', '$transactiontime');";
    my $sth_linked_drop = $dbh->prepare($sql_linked_drop);
    $sth_linked_drop->execute;
  }
  
  your_moves($ffl_team);

# Debug
#  print "$sql_add\n";
#  print "<p>\n";
#  print "$sql_linked_drop\n";

  my $sql_count = "select count(*) from transaction_request;";
  my $sth_count = $dbh->prepare($sql_count);
  $sth_count->execute;

}

elsif(param( 'f_action' ))
{

  my $ffl_team = param('f_team');
  my $action = param( 'f_action' );

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  print "<h1><center>Choose Your Move Wisely</center></h1>\n";

  if($action eq 'Add')
  {
    print "<h3>Select a Player to Add</h3>\n";

    print "The following players are not on any FFL team<p>\n";

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";

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

    print "<input type=hidden name=f_ffl_team value=\"$ffl_team\">\n";
    print "<input type=hidden name=f_action value=\"$action\">\n";

    print "<input type=submit value=\"Submit\">\n";
    print "</form>\n";
  }

  elsif($action eq 'Drop')
  {
    print "<h3>Select a Player to Drop</h3>\n";

    print "The following players are on $ffl_team<p>\n";

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
    print "<td><select name=f_player><option selected value=\"\">Select a Player\n";

    my $sql_drop = "(select player,position,nfl_team from ffl_2015.players_QB where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_WR where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_RB where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_TE where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_K where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_DEF where ffl_team = '$ffl_team')"
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
    print "<input type=hidden name=f_action value=\"$action\">\n";

    print "<input type=submit value=\"Submit\">\n";
    print "</form>\n";
  }

  elsif($action eq 'Link')
  {
    print "<h3>Select a Player to Add</h3>\n";

    print "The following players are not on any FFL team<p>\n";

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";

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

    print "<h3>Select a Player to Drop</h3>\n";

    print "The following players are on $ffl_team<p>\n";

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
    print "<td><select name=f_player_l><option selected value=\"\">Select a Player\n";

    my $sql_drop = "(select player,position,nfl_team from ffl_2015.players_QB where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_WR where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_RB where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_TE where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_K where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_DEF where ffl_team = '$ffl_team')"
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
    print "<input type=hidden name=f_action value=\"Link\">\n";

    print "<input type=submit value=\"Submit\">\n";
    print "</form>\n";
  }

  elsif($action eq 'Trade')
  {
    print "This section coming soon\n";
  }

  elsif($action eq 'Activate')
  {
    print "The following players are on $ffl_team Injured Reserve<p>\n";

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
    print "<td><select name=f_player><option selected value=\"\">Select a Player\n";

    my $sql_deactivate = "(select player,position,nfl_team from ffl_2015.injured_reserve where ffl_team = '$ffl_team')"
        . " order by player asc;";

    my $sth_deactivate = $dbh->prepare($sql_deactivate);
    $sth_deactivate->execute();

    while (my $row = $sth_deactivate->fetchrow_arrayref)
    {
      my $result = "$row->[0], $row->[1], $row->[2]";
      print "  <option value=\"$result\">$result\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    print "</table>\n";

    print "<input type=hidden name=f_ffl_team value=\"$ffl_team\">\n";
    print "<input type=hidden name=f_action value=\"$action\">\n";

    print "<input type=submit value=\"Submit\">\n";
    print "</form>\n";

  }
  elsif($action eq 'Deactivate')
  {
    print "The following players are on $ffl_team<p>\n";

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">Player:</font></td>\n";
    print "<td><select name=f_player><option selected value=\"\">Select a Player\n";

    my $sql_deactivate = "(select player,position,nfl_team from ffl_2015.players_QB where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_WR where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_RB where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_TE where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_K where ffl_team = '$ffl_team')"
        . " union (select player,position,nfl_team from players_DEF where ffl_team = '$ffl_team')"
        . " order by player asc;";

    my $sth_deactivate = $dbh->prepare($sql_deactivate);
    $sth_deactivate->execute();

    while (my $row = $sth_deactivate->fetchrow_arrayref)
    {
      my $result = "$row->[0], $row->[1], $row->[2]";
      print "  <option value=\"$result\">$result\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    print "</table>\n";

    print "<input type=hidden name=f_ffl_team value=\"$ffl_team\">\n";
    print "<input type=hidden name=f_action value=\"$action\">\n";

    print "<input type=submit value=\"Submit\">\n";
    print "</form>\n";

  }
}
else # Nothing selected or first time page is loaded
{
  my $ffl_team = Foozeball::get_ffl_team($ffl_manager);
 
  print "<h1><center>$ffl_team, Your Team Sucks....Make a Change</center></h1>\n";

#  print "Your team is $ffl_team<br>\n";

  your_moves($ffl_team);

  print "<p>\n";

  print "If you make a request prior to Wednesday at midnight and want to withdraw it contact DJ before Thursday.  After that all transactions entered will be processed.\n";

  print "<p>\n";

  print "You are requesting a transaction for week <b><font color=\"#FF0000\">$week</font></b>.\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Action:</font></td>\n";
  print "<td><select name=f_action><option selected value=\"\">Select an action\n";
  print "  <option value=\"Add\">Add a player\n";
  print "  <option value=\"Drop\">Drop a player\n";
  print "  <option value=\"Link\">Linked Drop\n";
#  print "  <option value=\"Trade\">Trade a player\n";
  print "  <option value=\"Activate\">Move a player off the IR\n";
  print "  <option value=\"Deactivate\">Move a player to IR\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=hidden name=f_team value=\"$ffl_team\">\n";
  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";

}
print end_html();
