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
#my $week = 1;

my @teams = (
  'A Dingo Ate My Brady',
  'Armenia',
  'Death Blow',
  'Death To Armenia',
#  'Dublin Tundra Wookies',
#  'East Bay Gotham Knights',
  'Mr Rodgers Neighborhood',
  'IN DREW BREES WE TRUST',
#  'Mantooth Saints',
#  'Oklahoma Rednecks',
  'Shiva Blast',
  'The Bam Bam Bigaloes'
);

my $i;
my $team;

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);
my $ffl_manager = $ENV{'REMOTE_USER'};
my $ffl_team = Foozeball::get_ffl_team($ffl_manager);;
my $cgi_script = "\/cgi-bin\/ffl_2015\/elimination.cgi";
my $cgi_page = "elimination";

# put the self posted shit here

if(param( 'f_pick' ))
{
  my $ffl_team = param( 'f_team' );
  my $elim_pick = param( 'f_pick' );

  my $sql2 = "update elimination set nfl_team = '$elim_pick' where week = $week and ffl_team = '$ffl_team';";
  my $sth2 = $dbh->prepare($sql2);
  $sth2->execute();

  #log_sql($ffl_manager,$cgi_page,$sql2);
  #open(LOGFILE,">>/usr/local/logs/elimination.log");
  #print LOGFILE "$currentdate $currenttime $ffl_manager $sql2\n";
  #print "$currentdate $currenttime $ffl_manager $sql2\n";
  #close(LOGFILE);

}

print header();
print start_html("Fantasy Football Elimination Challenge");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">2015 Elimination Challenge</font></center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"12%\" height=\"38\"></td>\n";

# print the teams across the top of the table
foreach $team (@teams)
{
  print "<td width=\"11%\"><center><b><a href=\"./teams.cgi?f_team=$team&f_order=total_pts\">$team</a></b></center></td>\n";
}
print "</tr>\n";

#for ($i = 1; $i <= 13; $i++) # use this after regular season
for ($i = 1; $i <= $week; $i++)
{
  print "<tr>\n";
  print "  <td width=\"12%\"><b><font color=\"#FFFFDF\">Week $i</font></b></td>\n";

  foreach $team (@teams)
  {
    my $sql = "select nfl_team, win from elimination where week = $i and ffl_team = '$team';";
    my $sth = $dbh->prepare($sql);
    $sth->execute();

    my $row = $sth->fetchrow_arrayref;

    if($row->[1] eq "Y")
    {
      if($row->[0] eq "")
      {
        print "<td width=\"11%\"><center><img src=\"http://www.djffl.net/images/Sad.gif\"></center></
td>\n";
      }
      else
      {
      print "<td width=\"11%\"><center><img src=\"http://www.djffl.net/images/$row->[0]_r.gif\"></center></td>\n";
      }
    }
    else
    {
      if($row->[0] eq "")
      {
        print "<td width=\"11%\"><center><img src=\"http://www.djffl.net/images/ThumbsDown.gif\"></center></td>\n";
      }
      else
      {
      print "<td width=\"11%\"><center><img src=\"http://www.djffl.net/images/$row->[0]_l.gif\"></center></td>\n";
      }
    }
  }
}

print "</tr>\n";
print "</table>\n";

  print "<p>\n";

  print "You can change the elimination pick for week <b><font color=\"#FF0000\">$week</font></b> for $ffl_team.<br>\n";
#  print "Sorry $ffl_team but the elimination challenge is over for the season.  Come back next year to play again!!!<p>\n";

  my $sql_count = "select count(*) from elimination where ffl_team = '$ffl_team' and win = 'N';";
  my $sth_count = $dbh->prepare($sql_count);
  $sth_count->execute();
 
  # There should only ever be 1 row that is returned for the previous sql
  while (my $row = $sth_count->fetchrow_arrayref)
  {
    print "Currently you have <b><font color=\"#FF0000\">$row->[0]</font></b> bad picks.\n";
  } 


if ($ffl_manager ne 'guest')
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Elimination Pick:</font></td>\n";
  print "<td><select name=f_pick><option selected value=\"\">Select a Team\n";
  print "  <option value=\"Ari\">Arizona\n";
  print "  <option value=\"Atl\">Atlanta\n";
  print "  <option value=\"Bal\">Baltimore\n";
  print "  <option value=\"Buf\">Buffalo\n";
  print "  <option value=\"Car\">Carolina\n";
  print "  <option value=\"Chi\">Chicago\n";
  print "  <option value=\"Cin\">Cincinnati\n";
  print "  <option value=\"Cle\">Cleveland\n";
  print "  <option value=\"Dal\">Dallas\n";
  print "  <option value=\"Den\">Denver\n";
  print "  <option value=\"Det\">Detroit\n";
  print "  <option value=\"GB\">Green Bay\n";
  print "  <option value=\"Hou\">Houston\n";
  print "  <option value=\"Ind\">Indianapolis\n";
  print "  <option value=\"Jac\">Jacksonville\n";
  print "  <option value=\"KC\">Kansas City\n";
  print "  <option value=\"Mia\">Miami\n";
  print "  <option value=\"Min\">Minnesota\n";
  print "  <option value=\"NE\">New England\n";
  print "  <option value=\"NO\">New Orleans\n";
  print "  <option value=\"NYG\">New York Giants\n";
  print "  <option value=\"NYJ\">New York Jets\n";
  print "  <option value=\"Oak\">Oakland\n";
  print "  <option value=\"Phi\">Philadelphia\n";
  print "  <option value=\"Pit\">Pittsburgh\n";
  print "  <option value=\"SD\">San Diego\n";
  print "  <option value=\"SF\">San Francisco\n";
  print "  <option value=\"Sea\">Seattle\n";
  print "  <option value=\"StL\">St. Louis\n";
  print "  <option value=\"TB\">Tampa Bay\n";
  print "  <option value=\"Ten\">Tennessee\n";
  print "  <option value=\"Was\">Washington\n";
  print "  </select></td>\n";
  print "</tr>\n";
  print "</table>\n";

  print "<input type=hidden name=f_team value=\"$ffl_team\">\n";
  print "<input type=submit value=\"Submit\">\n";

  print "</form>\n";
}
else
{
  print "<p>\n";
}

print "<p>\n";

print "If you are trying to set an elimination pick and the tool has been locked for the current week (you can only set for next week) but the first NFL game of the week has not started email DJ with your pick.<p>\n";

print "Remember that you can only pick 1 team per season.  If you pick a team that you had previously selected then the second choice will be treated as an incorrect pick, regardless of the outcome of the NFL game.<p>\n";

print "<p>\n";
print "<center>\n";
print "A helmet facing to the right like such <img src=\"http://www.djffl.net/images/SF_r.gif\"> indicates a correct pick for that week.<p>\n";
print "A helmet facing to the left like such <img src=\"http://www.djffl.net/images/Oak_l.gif\"> indicates a wrong pick for that week.<p>\n";
print "A <img src=\"http://www.djffl.net/images/ThumbsDown.gif\"> indicates no pick for a previous week.<p>\n";
print "A <img src=\"http://www.djffl.net/images/Sad.gif\"> indicates no pick for the current week.<p>\n";
print "Only teams still in the competition are listed.\n";
print "</center>\n";

print end_html();
