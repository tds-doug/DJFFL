#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $week = Foozeball::getweek();
#my $week = 1;

my $adminweek = Foozeball::admin_getweek();
#my $adminweek = 1;

my $lastweek = $week - 1;
my $nextweek = $week + 1;

# stats week is just to display the week the stats status is for
my $statsweek = $lastweek;
#my $statsweek = $week;

#my $transactions = 'Processed';
my $transactions = 'Not Processed';
#my $transactions = 'No More for the season!!!';
#my $transactions = 'The season starts Sept 10.';

#my $stats = 'The season starts Sept 10.';
my $stats = 'Uploaded';
#my $stats = 'Uploaded thru Sunday';
#my $stats = 'Uploaded thru Thursday';
#my $stats = 'Not Uploaded';

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $ffl_manager = $ENV{'REMOTE_USER'};
my $ffl_team = Foozeball::get_ffl_team($ffl_manager);

print header();
print start_html("Fantasy Football Main Page");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

# TOP OF PAGE

#print "<center><h1><blink>FFL Draft is Wednesday September 2 at 7PM PST!!!</blink></h1></center><p>\n";
#print "<center><h2>NFL 2015 First Game: September 10 at 5:30PM PST</h2></center>\n";
#print "<p><hr><p>\n";

#print "<center><h3>FFL 2014 FFL Bowl Winner: The Bam Bam Bigaloes</h3></center>\n";
#print "<center><h4>FFL 2014 Toilet Bowl Winner: Oklahoma Rednecks</h4></center>\n";

print "<p><hr><p>\n";

# WEEKLY LEAGUE STATUS
#print "<table align=\"center\" width=\"100%\">";
#print "<tr>\n";
#print "<td>\n";
#print "<center><font face=\"Verdana\" color=\"#FFFF80\">Current Week<br></font><font face=\"Verdana\" color=\"#FFFFDF\">$week</font></center>\n";
#print "</td>\n";

# Status: Not Processed / Processed 
#print "<td>\n";
#print "<center><font face=\"Verdana\" color=\"#FFFF80\">Week $week Transactions<br></font><font face=\"Verdana\" color=\"#FFFFDF\">$transactions</font></center>\n";
#print "</td>\n";

# Status: Not Uploaded / Not Completed / Uploaded / None
#if($lastweek eq '0')
#print "<td>\n";
#print "<center>";

#if($lastweek == 0)
#{
#  print "<font face=\"Verdana\" color=\"#FFFF80\">Week 1 Stats<br></font><font face=\"Verdana\" color=\"#FFFFDF\">$stats</font>\n";
#}
#else
#{
#  print "<font face=\"Verdana\" color=\"#FFFF80\">Week $statsweek Stats<br></font><font face=\"Verdana\" color=\"#FFFFDF\">$stats</font>\n";
#}

#print "</center>";
#print "</td>\n";
#print "</tr>\n";
#print "</table>\n";

# END WEEKLY LEAGUE STATUS

#print "<p><hr><p>\n";

# Begin Your Matchups and ...Of The Week Section
print "<table width=\"100%\">";
print "<tr>\n";

print "<td>\n";
print "<h3><font face=\"Verdana\" color=\"#FFFF80\"><center>Matchups</center></font></h3><p>\n";
print "</td>\n";
print "<td>\n";
print "<h3><font face=\"Verdana\" color=\"#FFFF80\"><center>...Of The Week for Week $lastweek</center></font></h3><p>\n";
print "</td>\n";
print "</tr>\n";

print "<tr>\n";

# BEGIN MATCHUPS SECTION
print "<td>\n";

# Last weeks matchups
print "<center><a href=\"./matchups.cgi?f_week=$lastweek\"><font face=\"Verdana\" color=\"#FFFF80\">Last Weeks Matchups</font></a></center>\n";
print "<center>\n";
print "<table border=\"1\" width=\"80%\">";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Week</center></b></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Home Team</center></b></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Away Team</center></b></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Outcome</center></b></font></td>\n";

my $sql_last_week = "select * from schedule3 where week = $lastweek and home_status = \'H\'";
my $sth_last_week = $dbh->prepare($sql_last_week);
$sth_last_week->execute();

print "<tr>\n";
while (my $row = $sth_last_week->fetchrow_arrayref)
{
  print "<tr>\n";

  if( $ffl_team eq $row->[1] or $ffl_team eq $row->[4] )
  {
    print "<td width=\"10%\"><center><font color=\"#FF0000\">$row->[0]</font></center></td>\n";
    print "<td width=\"40%\"><center><font color=\"#FF0000\">$row->[1]</font></center></td>\n";
    print "<td width=\"40%\"><center><font color=\"#FF0000\">$row->[4]</font></center></td>\n";
    print "<td width=\"10%\"><center><font color=\"#FF0000\">$row->[2] - $row->[5]</font></center></td>\n";
  }
  else
  {
    print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[0]</font></center></td>\n";
    print "<td width=\"40%\"><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
    print "<td width=\"40%\"><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
    print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[2] - $row->[5]</font></center></td>\n";
  }
print "</tr>\n";
}

print "</table>\n";
print "</center>\n";

print "<p>\n";

# This week Matchup
print "<center><font face=\"Verdana\" color=\"#FFFF80\">Your Next Matchup</font></center>\n";
print "<center>\n";
print "<table border=\"1\" width=\"80%\">";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Week</center></b></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Your Team</center></b></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Opponent</center></b></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Outcome</center></b></font></td>\n";

my $sql_current = "select * from schedule3 where week = $week and ffl_team = '$ffl_team';";
my $sth_current = $dbh->prepare($sql_current);
$sth_current->execute();

print "<tr>\n";
while (my $row = $sth_current->fetchrow_arrayref)
{
  print "<tr>\n";
  print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[0]</font></center></td>\n";
  print "<td width=\"40%\"><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
  print "<td width=\"40%\"><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
  print "<td width=\"10%\"><center><font color=\"#FFFFDF\">$row->[2] - $row->[5]</font></center></td>\n";
  print "<tr>\n";
}
print "</tr>\n";

print "</table>\n";
print "</center>\n";
print "</td>\n";
# END OF MATCHUPS SECTION 

# ...OF THE WEEK SECTION
print "<td>\n";

# MANAGER OF THE WEEK SECTION
print "<center><font face=\"Verdana\" color=\"#FFFF80\"><a href=\"./motw.cgi\">Manager of the Week</a></font></center>\n";

my $sql_motw = "select * from motw where week = $lastweek;";
my $sth_motw = $dbh->prepare($sql_motw);
$sth_motw->execute();

print "<center>\n";
print "<table border=\"1\" width=\"80%\">\n";
print "<tr>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Manager</b></center></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Max Points</b></center></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Missed By</b></center></font></td>\n";
print "</tr>\n";

while (my $row_motw = $sth_motw->fetchrow_arrayref)
{
  print "<tr>\n";

  if ($ffl_team eq $row_motw->[1])
  {
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_motw->[1]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_motw->[2]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_motw->[4] pts</center></font></td>\n";
  }
  else
  {
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_motw->[1]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_motw->[2]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_motw->[4] pts</center></font></td>\n";
  }

  print "</tr>\n";
}

print "</table>\n";
# END MANAGER KILL OF THE WEEK SECTION

print "<p>\n";

# ZOMBIE KILL OF THE WEEK SECTION
print "<center><font face=\"Verdana\" color=\"#FFFF80\"><a href=\"./zombie.cgi\">Zombie Kill of the Week</a></font></center>\n";

my $sql_zombie = "select * from zombie_kills where week = $lastweek;";
my $sth_zombie = $dbh->prepare($sql_zombie);
$sth_zombie->execute();

print "<center>\n";
print "<table border=\"1\" width=\"80%\">\n";
print "<tr>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Killer</b></center></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Killee</b></center></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Killed By</b></center></font></td>\n";
print "</tr>\n";

while (my $row_zombie = $sth_zombie->fetchrow_arrayref)
{
  print "<tr>\n";

  if ($ffl_team eq $row_zombie->[1] or $ffl_team eq $row_zombie->[2])
  {
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_zombie->[1]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_zombie->[2]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_zombie->[4] pts</center></font></td>\n";
  }
  else
  {
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_zombie->[1]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_zombie->[2]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_zombie->[4] pts</center></font></td>\n";
  }

  print "</tr>\n";
}

print "</table>\n";
# END ZOMBIE KILL OF THE WEEK SECTION

print "<p>\n";

# CONEHEAD OF THE WEEK SECTION
print "<center><font face=\"Verdana\" color=\"#FFFF80\"><a href=\"./conehead.cgi\">Conehead of the Week</a></font></center>\n";

my $sql_conehead = "select * from conehead where week = $lastweek;";
my $sth_conehead = $dbh->prepare($sql_conehead);
$sth_conehead->execute();

print "<center>\n";
print "<table border=\"1\" width=\"80%\">\n";
print "<tr>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Manager</b></center></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Max Points</b></center></font></td>\n";
print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center><b>Missed By</b></center></font></td>\n";
print "</tr>\n";

while (my $row_conehead = $sth_conehead->fetchrow_arrayref)
{
  print "<tr>\n";

  if ($ffl_team eq $row_conehead->[1])
  {
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_conehead->[1]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_conehead->[2]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FF0000\"><center>$row_conehead->[4] pts</center></font></td>\n";
  }
  else
  {
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_conehead->[1]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_conehead->[2]</center></font></td>\n";
    print "<td><font face=\"Verdana\" color=\"#FFFFDF\"><center>$row_conehead->[4] pts</center></font></td>\n";
  }

  print "</tr>\n";
}

print "</table>\n";
# END CONEHEAD OF THE WEEK SECTION

print "</tr>\n";
print "</table>\n";
print "</center>\n";

print "<p><hr><p>\n";

# SMACK TALK SECTION
print "<center><h3><font face=\"Verdana\" color=\"#FFFF80\">Recent <a href=\"./messages.cgi\">Smack Talk</a></font></h3></center>\n";

my $sql = "select * from messages order by id desc limit 5;";
#my $sql = "select * from messages where week = $week order by id desc;";
my $sth = $dbh->prepare($sql);
$sth->execute();

print "<table align=center border=\"1\" width=\"80%\">";
print "<tr>\n";
print "<td width=\"20%\"><center><b><font color=\"#FFFF80\">Team Name</font></b></center></td>\n";
print "<td width=\"80%\"><center><b><font color=\"#FFFF80\">Message</font></b></center></td>\n";
print "<tr>\n";

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";

  if($row->[1] eq 'Armenia')
  {
    print "<td width=\'15%\'><center><font color=\"#FF0000\">A</font>";
    print "<font color=\"#FFA500\">r</font>";
    print "<font color=\"#FFFF00\">m</font>";
    print "<font color=\"#008000\">e</font>";
    print "<font color=\"#00FF00\">n</font>";
    print "<font color=\"#800080\">ia</font";
    print "</center></td>\n";
  }
  else
  {
  print "<td width=\"20%\"><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
  }
  my $message = $row->[4] . $row->[5] . $row->[6];
  print "<td width=\"80%\"><font color=\"#FFFFDF\">$message</font></td>\n";
  print "<tr>\n";
}

print "</table>\n";

print "<p><hr><p>\n";

#print "<center><h3><font face=\"Verdana\" color=\"#FFFF80\">2015 Draft Order</font></h3></center><p>\n";
#print "<ol>\n";
#print "<li>Oklahoma Rednecks (2014 Toilet Bowl Winner)</li>\n";
#print "<li>Dublin Tundra Wookies</li>\n";
#print "<li>A Dingo Ate My Brady</li>\n";
#print "<li>Mr Rodgers Neighborhood</li>\n";
#print "<li>Death To Armenia</li>\n";
#print "<li>East Bay Gotham Knights</li>\n";
#print "<li>Mantooth Saints</li>\n";
#print "<li>Death Blow</li>\n";
#print "<li>IN DREW BREES WE TRUST</li>\n";
#print "<li>Armenia (2013 League Champion)</li>\n";
#print "<li>Shiva Blast</li>\n";
#print "<li>The Bam Bam Bigaloes</li>\n";
#print "</ol>\n";

#print "FFL Draft is Wednesday September 2 at 6PM PST!!!<p>\n";
#print "It\'s on you to ensure your Gtalk / Google Hangout works.  Failure to do so prior to the start of the draft results in a \$10 salary penalty.<p>\n";

#print "<p><hr><p>\n";

#print "<center><h3><font face=\"Verdana\" color=\"#FFFF80\">2015 Playoff Picture</font></h3></center><p>\n";

#print "<u>Week 14</u><br>\n";
#print "Quarter Final Match (QF1) - Shiva Blast (4) vs Mantooth Saints (5)<br>\n";
#print "Quarter Final Match (QF2) - Death Blow (3) vs IN DREW BREES WE TRUST (6)<br>\n";
#print "Toilet Bowl - Oklahoma Rednecks vs Mr Rodgers Neighborhood<br>\n";
#print "<p>\n"; 

#print "<u>Week 15</u><br>\n";
#print "Semi Final Match (SF1) - Armenia (1) vs Shiva Blast (4)<br>\n";
#print "Semi Final Match (SF2) - The Bam Bam Bigaloes (2) vs IN DREW BREES WE TRUST (6)<br>\n";
#print "<p>\n";

#print "<u>Week 16</u><br>\n";
#print "Fantasy Bowl - Shiva Blast (4) vs The Bam Bam Bigaloes (2)\n";

#print "<p><hr><p>\n";

print "<center><font face=\"Verdana\" color=\"#FFFF80\"><h3>Commish Note</h3></font></center>\n";

#print "NFL schedule is NOT updated.<p>\n";
#print "NFL Bye Weeks are NOT updated.<p>\n";

#print "This year's Manager of the Year with 6 MotW awards is Mr Rodgers Neighborhood.  They will recieve +\$10 on their salary cap for next year.<p>\n";
#print "This year's Conehead of the Year with 4 CotW awards is Shiva Blast.  They will recieve -\$10 on their salary cap for next year.<p>\n";

#print "Elimination Challenge Winners:<p>\n";
#print "This Year\'s Elimination Challenge Winners:<p>\n";
#print "<ul>\n";
#print "<li>Armenia - 3 wrong picks -> +\$4 on next year\'s salary cap</li>\n";
#print "<li>Death Blow - 2 wrong picks -> +\$6 on this year\'s salary cap</li>\n";
#print "<li>Death To Armenia - 3 wrong picks -> +\$4 on next year\'s salary cap</li>\n";
#print "<li>Mr Rodgers Neighborhood - 2 wrong picks -> +\$6 on this year\'s salary cap</li>\n";
#print "<li>IN DREW BREES WE TRUST - 1 wrong pick -> +\$8 on next year\'s salary cap</li>\n";
#print "<li>The Bam Bam Bigaloes - 1 wrong pick -> +\$8 on this year\'s salary cap</li>\n";
#print "</ul>\n";


#print "<p>\n";

#print "lazy.\n";

#print "<p><hr><p>\n";


#print "Teams that have confirmed they will play this year so far:<p>\n";
#print "<ul>\n";
#print "<li>Armenia</li>\n";
#print "<li>Death Blow</li>\n";
#print "<li>Death To Armenia</li>\n";
#print "<li>Dublin Tundra Wookies</li>\n";
#print "<li>East Bay Gotham Knights</li>\n";
#print "<li>Shiva Blast</li>\n";
#print "<li>IN DREW BREES WE TRUST</li>\n";
#print "<li>Mr Rodgers Neighborhood</li>\n";
#print "<li>Mantooth Saints</li>\n";
#print "<li>Oklahoma Rednecks</li>\n";
#print "<li>The Bam Bam Bigaloes</li>\n";
#print "</ul>\n";

#print "Teams that have confirmed they will <b>NOT</b> play this year:<p>\n";
#print "<ul>\n";
#print "<li>Niner Knights</li>\n";
#print "</ul>\n";

print "<p><hr><p>\n";

# BYE WEEK SECTION
print "<center><h3><font face=\"Verdana\" color=\"#FFFF80\">NFL Teams With A Bye This Week</font></h3></center>\n";
#print "No byes until week 4.\n";
#print "No byes this week.\n";
#print "No more byes until next season!\n";

print "<center>\n";
print "<table border=\"0\" cellpadding=\"0\" cellspacking=\"0\" style=\"border-collapse: collapse\" width=\"60%\">\n";
print "<tr>\n";
print "  <td><center><img src=\"http://www.djffl.net/images/Atl.gif\"></center></td>\n";
print "  <td><center><img src=\"http://www.djffl.net/images/Ind.gif\"></center></td>\n";
print "  <td><center><img src=\"http://www.djffl.net/images/SD.gif\"></center></td>\n";
print "  <td><center><img src=\"http://www.djffl.net/images/SF.gif\"></center></td>\n";
#print "  <td><center><img src=\"http://www.djffl.net/images/GB.gif\"></center></td>\n";
#print "  <td><center><img src=\"http://www.djffl.net/images/Ten.gif\"></center></td>\n";

print "</tr>\n";
print "<tr>\n";
print "  <td><center><font color=\"#FFFFDF\">Atlanta</font></center></td>\n";
print "  <td><center><font color=\"#FFFFDF\">Indianapolis</font></center></td>\n";
print "  <td><center><font color=\"#FFFFDF\">San Diego</font></center></td>\n";
print "  <td><center><font color=\"#FFFFDF\">San Francisco</font></center></td>\n";
#print "  <td><center><font color=\"#FFFFDF\">Detroit</font></center></td>\n";
#print "  <td><center><font color=\"#FFFFDF\">Green Bay</font></center></td>\n";
print "</tr>\n";
print "</table>\n";
print "</center>\n";

print "<p><hr><p>\n";

print "<center><h3><font face=\"Verdana\" color=\"#FFFF80\">League WebSite Changes</font></h3></center>\n";

print "<ol>\n";
print "<li>Added the NFL Bye Week to the FFL Teams page</li>\n";
print "<li>Updated schedule for 12 teams</li>\n";
print "</ol>\n";

print end_html();
