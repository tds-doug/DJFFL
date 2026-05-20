#!/usr/bin/perl -w
use Time::Local;
use POSIX qw(strftime);

my @c_time = (localtime);
my $currenttime = timelocal(@c_time);
my $currentdate = strftime "%e%b%Y", @c_time;

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $week = Foozeball::admin_getweek();
#my $week = 17;

print header();
print start_html("Fantasy Football Lineup Management");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font color=\"#FFFF80\" face=\"Verdana\">Weekly Starting Lineup Management</font></center></h1>\n";

my $ffl_manager = $ENV{'REMOTE_USER'};

my $cgi_script = "\/cgi-bin\/ffl_2015\/change_lineup.cgi";
my $cgi_page = "change_lineup";

if(param( 'f_starter1' ))
{

  my @starters;
  $starters[0] = param( 'f_starter1' );
  $starters[1] = param( 'f_starter2' );
  $starters[2] = param( 'f_starter3' );
  $starters[3] = param( 'f_starter4' );
  $starters[4] = param( 'f_starter5' );
  $starters[5] = param( 'f_starter6' );
  $starters[6] = param( 'f_starter7' );
  $starters[7] = param( 'f_starter8' );

  my $ffl_team = param( 'f_team' );
  my $i;

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  my $sql_bench = "update lineups set starter = 'N' where week = $week and ffl_team = '$ffl_team';";

  my $sth_bench = $dbh->prepare($sql_bench);
  $sth_bench->execute();

  foreach $i (@starters)
  {
    my $player;
    my $position;
    my $nfl_team;

    if($i=~m/([A-Za-z \'\-\.]+),([A-Z]+),([A-Za-z]+)/)
    {
      $player = Foozeball::db_escape($1);
      $position = $2;
      $nfl_team = $3;
    }

    chomp($player);
    chomp($position);
    chomp($nfl_team);

    my $sql_start = "update lineups set starter = 'Y' where week = $week and ffl_team = '$ffl_team' and player = '$player' and position = '$position' and nfl_team = '$nfl_team';";
    my $sth_start = $dbh->prepare($sql_start);
    $sth_start->execute();

    log_sql($ENV{'REMOTE_USER'},$cgi_page,$sql_start);

#DEBUG
#print "DEBUG: Starter is $i<br>\n";
#print "DEBUG: SQL is $sql_start<br>\n";
  }

  print "Lineup for $ffl_team has been updated for Week $week<p>\n";
  print "Click <a href=\"./lineup.cgi?f_team=$ffl_team&f_week=$week\">here</a> to see your new lineup\n";

}
elsif(param( 'f_formation' ))
{

  my $ffl_team = param('f_team');
  my $formation = param( 'f_formation' );

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);


  print "<h3>Select Players for a $formation Formation</h3>\n";

  if($formation eq 'Regular')
  {

    print "You are changing your lineup for:<br><h1><blink><font color=\"#FF0000\">Week $week</font></blink></h1><p>\n";

    # Quarterback section
    my $sql_qb = "select player,position,nfl_team from lineups where week = $week and position = 'QB' and ffl_team = '$ffl_team' order by player;";
    my $sth_qb = $dbh->prepare($sql_qb);
    $sth_qb->execute();

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";
    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">QB:</font></td>\n";
    print "<td><select name=f_starter1><option selected value=\"\">Select a QB\n";

    while (my $row = $sth_qb->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Wide Receiver section
    my $sql_wr = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr = $dbh->prepare($sql_wr);
    $sth_wr->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter2><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    my $sql_wr2 = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr2 = $dbh->prepare($sql_wr2);
    $sth_wr2->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter3><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr2->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Running Back section
    my $sql_rb = "select player,position,nfl_team from lineups where week = $week and position = 'RB' and ffl_team = '$ffl_team' order by player;";

    my $sth_rb = $dbh->prepare($sql_rb);
    $sth_rb->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">RB:</font></td>\n";
    print "<td><select name=f_starter4><option selected value=\"\">Select a RB\n";

    while (my $row = $sth_rb->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";


    my $sql_rb2 = "select player,position,nfl_team from lineups where week = $week and position = 'RB' and ffl_team = '$ffl_team' order by player;";

    my $sth_rb2 = $dbh->prepare($sql_rb2);
    $sth_rb2->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">RB:</font></td>\n";
    print "<td><select name=f_starter5><option selected value=\"\">Select a RB\n";

    while (my $row = $sth_rb2->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Tight End section
    my $sql_te = "select player,position,nfl_team from lineups where week = $week and position = 'TE' and ffl_team = '$ffl_team' order by player;";

    my $sth_te = $dbh->prepare($sql_te);
    $sth_te->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">TE:</font></td>\n";
    print "<td><select name=f_starter6><option selected value=\"\">Select a TE\n";

    while (my $row = $sth_te->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Kicker section
    my $sql_k = "select player,position,nfl_team from lineups where week = $week and position = 'K' and ffl_team = '$ffl_team' order by player;";

    my $sth_k = $dbh->prepare($sql_k);
    $sth_k->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">K:</font></td>\n";
    print "<td><select name=f_starter7><option selected value=\"\">Select a K\n";

    while (my $row = $sth_k->fetchrow_arrayref)
    {
          print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Defense section
    my $sql_def = "select player,position,nfl_team from lineups where week = $week and position = 'DEF' and ffl_team = '$ffl_team' order by player;";

    my $sth_def = $dbh->prepare($sql_def);
    $sth_def->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">DEF:</font></td>\n";
    print "<td><select name=f_starter8><option selected value=\"\">Select a DEF\n";

    while (my $row = $sth_def->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    print "</table><p>\n";
    print "<input type=hidden name=f_team value=\"$ffl_team\">\n";
    print "<input type=submit value=\"Submit\">\n";
    print "</form>\n";

  }
  elsif($formation eq 'Red Gun')
  {
    print "You are changing your lineup for:<br><h1><blink><font color=\"#FF0000\">Week $week</font></blink></h1><p>\n";
    # Quarterback section

    my $sql_qb = "select player,position,nfl_team from lineups where week = $week and position = 'QB' and ffl_team = '$ffl_team' order by player;";

    my $sth_qb = $dbh->prepare($sql_qb);
    $sth_qb->execute();

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";
    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">QB:</font></td>\n";
    print "<td><select name=f_starter1><option selected value=\"\">Select a QB\n";

    while (my $row = $sth_qb->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Wide Receiver section
    my $sql_wr = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr = $dbh->prepare($sql_wr);
    $sth_wr->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter2><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    my $sql_wr2 = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr2 = $dbh->prepare($sql_wr2);
    $sth_wr2->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter3><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr2->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    my $sql_wr3 = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr3 = $dbh->prepare($sql_wr3);
    $sth_wr3->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter4><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr3->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Running Back section

    my $sql_rb = "select player,position,nfl_team from lineups where week = $week and position = 'RB' and ffl_team = '$ffl_team' order by player;";

    my $sth_rb = $dbh->prepare($sql_rb);
    $sth_rb->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">RB:</font></td>\n";
    print "<td><select name=f_starter5><option selected value=\"\">Select a RB\n";

    while (my $row = $sth_rb->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Tight End section
    my $sql_te = "select player,position,nfl_team from lineups where week = $week and position = 'TE' and ffl_team = '$ffl_team' order by player;";

    my $sth_te = $dbh->prepare($sql_te);
    $sth_te->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">TE:</font></td>\n";
    print "<td><select name=f_starter6><option selected value=\"\">Select a TE\n";

    while (my $row = $sth_te->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Kicker section
    my $sql_k = "select player,position,nfl_team from lineups where week = $week and position = 'K' and ffl_team = '$ffl_team' order by player;";

    my $sth_k = $dbh->prepare($sql_k);
    $sth_k->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">K:</font></td>\n";
    print "<td><select name=f_starter7><option selected value=\"\">Select a K\n";

    while (my $row = $sth_k->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Defense section
    my $sql_def = "select player,position,nfl_team from lineups where week = $week and position = 'DEF' and ffl_team = '$ffl_team' order by player;";

    my $sth_def = $dbh->prepare($sql_def);
    $sth_def->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">DEF:</font></td>\n";
    print "<td><select name=f_starter8><option selected value=\"\">Select a DEF\n";

    while (my $row = $sth_def->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    print "</table><p>\n";
    print "<input type=hidden name=f_team value=\"$ffl_team\">\n";
    print "<input type=submit value=\"Submit\">\n";

  }
  elsif($formation eq 'Run and Shoot')
  {
    print "You are changing your lineup for:<br><h1><blink><font color=\"#FF0000\">Week $week</font></blink></h1><p>\n";

    # Quarterback section
    my $sql_qb = "select player,position,nfl_team from lineups where week = $week and position = 'QB' and ffl_team = '$ffl_team' order by player;";

    my $sth_qb = $dbh->prepare($sql_qb);
    $sth_qb->execute();

    print "<form action=\"$cgi_script\" method=\"post\">\n";
    print "<table>\n";
    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">QB:</font></td>\n";
    print "<td><select name=f_starter1><option selected value=\"\">Select a QB\n";

    while (my $row = $sth_qb->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Wide Receiver section
    my $sql_wr = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr = $dbh->prepare($sql_wr);
    $sth_wr->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter2><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    my $sql_wr2 = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr2 = $dbh->prepare($sql_wr2);
    $sth_wr2->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter3><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr2->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    my $sql_wr3 = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr3 = $dbh->prepare($sql_wr3);
    $sth_wr3->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter4><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr3->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    my $sql_wr4 = "select player,position,nfl_team from lineups where week = $week and position = 'WR' and ffl_team = '$ffl_team' order by player;";

    my $sth_wr4 = $dbh->prepare($sql_wr4);
    $sth_wr4->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">WR:</font></td>\n";
    print "<td><select name=f_starter5><option selected value=\"\">Select a WR\n";

    while (my $row = $sth_wr4->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Running Back section

    my $sql_rb = "select player,position,nfl_team from lineups where week = $week and position = 'RB' and ffl_team = '$ffl_team' order by player;";

    my $sth_rb = $dbh->prepare($sql_rb);
    $sth_rb->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">RB:</font></td>\n";
    print "<td><select name=f_starter6><option selected value=\"\">Select a RB\n";

    while (my $row = $sth_rb->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Kicker section
    my $sql_k = "select player,position,nfl_team from lineups where week = $week and position = 'K' and ffl_team = '$ffl_team' order by player;";

    my $sth_k = $dbh->prepare($sql_k);
    $sth_k->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">K:</font></td>\n";
    print "<td><select name=f_starter7><option selected value=\"\">Select a K\n";

    while (my $row = $sth_k->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    # Defense section
    my $sql_def = "select player,position,nfl_team from lineups where week = $week and position = 'DEF' and ffl_team = '$ffl_team' order by player;";

    my $sth_def = $dbh->prepare($sql_def);
    $sth_def->execute();

    print "<tr>\n";
    print "<td><font color=\"#FFFFDF\">DEF:</font></td>\n";
    print "<td><select name=f_starter8><option selected value=\"\">Select a DEF\n";

    while (my $row = $sth_def->fetchrow_arrayref)
    {
      print "  <option value=\"$row->[0],$row->[1],$row->[2]\">$row->[0] - $row->[2]\n";
    }

    print "  </select></td>\n";
    print "</tr>\n";

    print "</table><p>\n";
    print "<input type=hidden name=f_team value=\"$ffl_team\">\n";
    print "<input type=submit value=\"Submit\">\n";

  }

  else
  {

    print "No such formation.  What the hell are you trying to do?\n";
  }

}
else
{
  my $ffl_team = Foozeball::get_ffl_team($ffl_manager);

  print "Your team is $ffl_team<br>\n";
  print "You are changing your lineup for:<br><h1><blink><font color=\"#FF0000\">Week $week</font></blink></h1><p>\n";

  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Formation:</font></td>\n";
  print "<td><select name=f_formation><option selected value=\"\">Select a Formation\n";
  print "  <option value=\"Regular\">Regular\n";
  print "  <option value=\"Red Gun\">Red Gun\n";
  print "  <option value=\"Run and Shoot\">Run and Shoot\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table><p>\n";

  print "<input type=hidden name=f_team value=\"$ffl_team\">\n";
  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";

  print "<p>\n";

  print "If you are trying to change your lineup and the tool has been locked for the current week (you can only set for next week) but the first NFL game of the week has not started email DJ with your lineup.<p>\n";

}

sub log_sql{ # create subroutine to log sql commands
  my ($ffl_mgr) = $_[0];
  my ($cgi_page) = $_[1];
  my ($sql_command) = $_[2];

  my $log_file = "/usr/local/logs/" . $cgi_page . ".log";
  #my $log_file = $cgi_page . ".log";

  open(LOG_FILE,">>$log_file");

  print LOG_FILE "$currentdate $currenttime $ffl_mgr $sql_command\n";
  #print "$log_file $currentdate $currenttime $ffl_mgr $sql_command\n";

  close(LOG_FILE);

} # end subroutine for logging sql command

print end_html();
