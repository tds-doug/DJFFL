#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $cgi_script = "\/cgi-bin\/ffl_2015\/rules.cgi";

print header();
print start_html("Fantasy Football Rules");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Read and Obey</font></center></h1>\n";
print "<p>\n";

if(param( 'f_topic' ))
{

  my $topic = param( 'f_topic' );


  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  my $sql = "select * from rules where topic = \"$topic\" order by number asc;";

  my $sth = $dbh->prepare($sql);
  $sth->execute();

  if($topic eq 'add_drop')
  {
    print "<center><h3>Adding\/Dropping Players</h3></center>\n";
  }
  elsif($topic eq 'contracts')
  {
    print "<center><h3>Contracts</h3></center>\n";
  }
  elsif($topic eq 'cpv')
  {
    print "<center><h3>Current Player Value</h3></center>\n";
  }
  elsif($topic eq 'draft')
  {
    print "<center><h3>Draft</h3></center>\n";
  }
  elsif($topic eq 'elimination')
  {
    print "<center><h3>Elimination Challenge</h3></center>\n";
  }
  elsif($topic eq 'fees')
  {
    print "<center><h3>Fees</h3></center>\n";
  }
  elsif($topic eq 'franchise_player')
  {
    print "<center><h3>Franchise Player</h3></center>\n";
  }
  elsif($topic eq 'free_agent')
  {
    print "<center><h3>Free Agent Market</h3></center>\n";
  }
  elsif($topic eq 'roster')
  {
    print "<center><h3>Rosters</h3></center>\n";
  }
  elsif($topic eq 'schedule')
  {
    print "<center><h3>Schedule and Playoffs</h3></center>\n";
  }
  elsif($topic eq 'trades')
  {
    print "<center><h3>Trades</h3></center>\n";
  }
  
  

  while (my $row = $sth->fetchrow_arrayref)
  {
    #my $rule = $row->[2] . $row->[3] . $row->[4];
    #print "$rule<p>\n";
    print "$row->[2]";
    print "$row->[3]";
    print "$row->[4]<p>\n";
  }

  if($topic eq 'roster')
  {
    print "Managers can choose from the following lineups:<p>\n";
    print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";
    print "<center>\n";
    print "<table border=\"3\" width=\"66%\" height=\"249\">\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\"><b>Regular</b></td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\"><b>Red Gun</b></td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\"><b>Run and Shoot</b></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">QB</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">QB</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">QB</td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">RB</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">RB</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">RB</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">WR</td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">TE</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">TE</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">RB</td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">K</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">K</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">K</td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">DEF</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">DEF</td>\n";
    print "    <td width=\"33%\" align=\"center\" height=\"19\">DEF</td>\n";
    print "  </tr>\n";
    print "</table>\n";
    print "</center>\n";
    print "</font>\n";
  }
  elsif($topic eq 'scoring')
  {
    print "<center>\n";
    print "<h3>Offensive Scoring</h3>\n";
    print "<table border=\"3\" width=\"66%\">\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Passing Yards</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">1 point per 50 yards</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Passing Touchdown</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">3 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Interceptions</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">-2 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Rushing Yards</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">1 point per 10 yards</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Rushing Touchdown</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">3 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Recieving Yards</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">1 point per 10 yards</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Recieving Touchdown</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">3 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Return Touchdown</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">4 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">2 Point Conversion</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">2 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Fumbles Lost</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">-1 point</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Field Goal 0 - 39 Yards</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">2 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Field Goal 40+ Yards</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">3 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Field Goal Missed 0-19 Yards</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">-2 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Field Goal Missed 20-29 Yards</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">-1 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Point After Touchdown</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">1 point</font></td>\n";
    print "  </tr>\n";
    print "</table>\n";

    print "<h3>Defensive/Special Teams Scoring</h3>\n";
    print "<table border=\"3\" width=\"66%\">\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">0 Points Allowed</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">10 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">1 - 6 Points Allowed</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">7 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">7 - 13 Points Allowed</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">4 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">14 - 20 Poinst Allowed</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">1 point</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Sack</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">1 point</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Interception</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">2 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Fumble Recovery</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">2 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Touchdown</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">4 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Safety</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">2 points</font></td>\n";
    print "  </tr>\n";
    print "  <tr>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">Blocked Kick</font></td>\n";
    print "    <td width=\"50%\" align=\"center\" height=\"19\"><font color=\"#FFFFDF\">2 points</font></td>\n";
    print "  </tr>\n";
    print "</table>\n";

    print "</center>\n";
  }
}
else
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Topic:</font></td>\n";
  print "<td><select name=f_topic><option selected value=\"\">Select a Topic\n";
  print "  <option value=\"add_drop\">Adding\/Dropping Players\n";
  print "  <option value=\"contracts\">Contracts\n";
  print "  <option value=\"cpv\">Current Player Value\n";
  print "  <option value=\"draft\">Draft\n";
  print "  <option value=\"elimination\">Elimination Challenge\n";
  print "  <option value=\"franchise_player\">Franchise Player\n";
  print "  <option value=\"free_agent\">Free Agent Market\n";
  print "  <option value=\"injured_reserve\">Injured Reserve\n";
  print "  <option value=\"fees\">League Fees\n";
  print "  <option value=\"roster\">Roster\n";
  print "  <option value=\"schedule\">Schedule and Playoffs\n";
  print "  <option value=\"scoring\">Scoring\n";
  print "  <option value=\"trades\">Trades\n";
  print "  </select></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();
