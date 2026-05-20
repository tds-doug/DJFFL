#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $ffl_manager = Foozeball::get_ffl_mgr($ENV{'REMOTE_USER'});

print header();
print start_html("Fantasy Football Side Bar");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFF80\">\n";

if($ffl_manager eq 'Dr. Keledjian')
{
  #print "<center><h3>Welcome<br><font color=\"#FF00FF\">$ffl_manager</h3></center></font>\n";
  print "<center><i><h3><font color=\"#FF0000\">Dr.</font>";
  print "<font color=\"#FFA500\">Ke</font>";
  print "<font color=\"#FFFF00\">le</font>";
  print "<font color=\"#008000\">dj</font>";
  print "<font color=\"#00FF00\">ia</font>";
  print "<font color=\"#800080\">n</font></h3></i></center>\n";
}
else
{
  print "<center><h3>Welcome<br><i>$ffl_manager</h3></center></i>\n";
}
print "<p>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr><td>\n";
print "<center><b><font color=\"#FFFF80\">2015 FFL Tools</font></b></center>\n";
print "</tr></td>\n";

if($ffl_manager eq 'DJ')
{
# Admin Section
  print "<tr><td>\n";
  print "<center><font color=\"#FFFFDF\">Admin</font></center>\n";
  print "<ul>\n";
  print "  <li><b><a href=\"./admin_tr.cgi\" target=\"main\">Admin TR</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin TR</font></b></li>\n";
  print "  <li><b><a href=\"./admin_add.cgi\" target=\"main\">Admin Add</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Add</font></b></li>\n";
  print "  <li><b><a href=\"./admin_drop.cgi\" target=\"main\">Admin Drop</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Drop</font></b></li>\n";
  print "  <li><b><a href=\"./admin_activate.cgi\" target=\"main\">Admin Activate</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Activate</font></b></li>\n";
  print "  <li><b><a href=\"./admin_deactivate.cgi\" target=\"main\">Admin Deactivate</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Deactivate</font></b></li>\n";

  print "<p>\n";

  print "  <li><b><a href=\"./admin_new_player.cgi\" target=\"main\">Admin New Player</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin New Player</font></b></li>\n";
  print "  <li><b><a href=\"./admin_upd_team.cgi\" target=\"main\">Admin Update Team</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Update Team</font></b></li>\n";
  print "  <li><b><a href=\"./admin_elimination.cgi\" target=\"main\">Admin Elimination</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin  Elimination</font></b></li>\n";

  print "<p>\n";

  print "  <li><b><a href=\"./admin_upd_points.cgi\" target=\"main\">Admin Update Points</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Update Points</font></b></li>\n";
  print "  <li><b><a href=\"./admin_upd_contract.cgi\" target=\"main\">Admin Update Contract</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Update Contract</font></b></li>\n";
  print "  <li><b><a href=\"./admin_fam.cgi\" target=\"main\">Admin FAM</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin FAM</font></b></li>\n";
  print "  <li><b><a href=\"./admin_franchise.cgi\" target=\"main\">Admin Franchise</a></b></li>\n";
#  print "  <li><b><font color=\"#FFFFDF\">Admin Franchise</font></b></li>\n";
#  print "  <li><b><a href=\"./admin_draft.cgi\" target=\"main\">Admin Draft</a></b></li>\n";
  print "  <li><b><font color=\"#FFFFDF\">Admin Draft</font></b></li>\n";
  print "  <li><b><a href=\"./admin_snapshot.cgi\" target=\"main\">Admin Snapshot</a></b></li>\n";
  print "</ul>\n";
  print "</td></tr>\n";
}

# Team Mgmt Section
print "<tr><td>\n";
print "<center><font color=\"#FFFFDF\">Team Mgmt</font></center>\n";
print "<ul>\n";
print "  <li><b><a href=\"./teams.cgi\" target=\"main\">FFL Teams</a></b></li>\n";
#print "  <li><b><a href=\"./schedule.cgi\" target=\"main\">Your Schedule</a></b></li>\n";
print "  <li><b><a href=\"./schedule3.cgi\" target=\"main\">Your Schedule</a></b></li>\n";

if ($ffl_manager eq 'Guest')
{
  print "  <li><b>Change Lineup</b></li>\n";
}
else
{
  print "  <li><b><a href=\"./change_lineup.cgi\" target=\"main\">Change Lineup</a></b></li>\n";
#  print "  <li><b>Change Lineup</b></li>\n";
}

if ($ffl_manager eq 'Guest')
{
print "  <li><b>Request a Transaction</b></li>\n";
}
else
{
print "  <li><b><a href=\"./trans_req.cgi\" target=\"main\">Request a Transaction</a></b></li>\n";
#print "  <li><b>Request a Transaction</b></li>\n";
}

print "  <li><b><a href=\"./elimination.cgi\" target=\"main\">Elimination Challenge</a></b></li>\n";
print "</ul>\n";
print "</td></tr>\n";

# Week to Week Section
print "<tr><td>\n";
print "<center><font color=\"#FFFFDF\">Week To Week</font></center>\n";
print "<ul>\n";
print "  <li><b><a href=\"./standings.cgi\" target=\"main\">Current Standings</a></b></li>\n";

if ($ffl_manager eq 'Guest')
{
  print "  <li><b>Smack Talk</b></li>\n";
}
else
{
  print "  <li><b><a href=\"./messages.cgi\" target=\"main\">Smack Talk</a></b></li>\n";
}

print "<p>\n";

print "  <li><b><a href=\"./matchups.cgi\" target=\"main\">Matchups</a></b></li>\n";
print "  <li><b><a href=\"./power.cgi\" target=\"main\">Power Scores</a></b></li>\n";
print "  <li><b><a href=\"./lineup.cgi\" target=\"main\">Weekly Lineup</a></b></li>\n";
print "  <li><b><a href=\"./motw.cgi\" target=\"main\">Manager of the Week</a></b></li>\n";
print "  <li><b><a href=\"./zombie.cgi\" target=\"main\">Zombie Kill of the Week</a></b></li>\n";
print "  <li><b><a href=\"./conehead.cgi\" target=\"main\">Conehead of the Week</a></b></li>\n";
print "</ul>\n";
print "</td></tr>\n";

# League Mgmt Section
print "<tr><td>\n";
print "<center><font color=\"#FFFFDF\">General League</font></center>\n";
print "<ul>\n";
print "  <li><b><a href=\"./transactions.cgi\" target=\"main\">Processed Transactions</a></b></li>\n";
print "  <li><b><a href=\"./tr.cgi\" target=\"main\">Previous Requests</a></b></li>\n";
print "  <li><b><a href=\"./waivers.cgi\" target=\"main\">Waivers</a></b></li>\n";
#print "  <li><b><a href=\"./bye_week.cgi\" target=\"main\">NFL Bye Weeks</a></b></li>\n";
print "  <li><b><a href=\"./nfl_byes.cgi\" target=\"main\">NFL Bye Weeks</a></b></li>\n";
print "  <li><b><a href=\"./records.cgi\" target=\"main\">Hall of Records</a></b></li>\n";
print "  <li><b><a href=\"./history.cgi\" target=\"main\">League History</a></b></li>\n";
print "  <li><b><a href=\"./rules.cgi\" target=\"main\">League Rules</a></b></li>\n";
print "</ul>\n";
print "</td></tr>\n";

# Transactions Section
#print "<tr><td>\n";
#print "<center><font color=\"#FFFFDF\">Transactions</font></center>\n";
#print "<ul>\n";
#print "</ul>\n";
#print "</td></tr>\n";

# Players Section
print "<tr><td>\n";
print "<center><font color=\"#FFFFDF\">Players</font></center>\n";
print "<ul>\n";
print "  <li><b><a href=\"./search.cgi\" target=\"main\">Player Search</a></b></li>\n";
print "  <li><b><a href=\"./players.cgi\" target=\"main\">Players By Position</a></b></li>\n";
print "  <li><b><a href=\"./free_players.cgi\" target=\"main\">Available Players</a></b></li>\n";
print "  <li><b><a href=\"./owned.cgi\" target=\"main\">Owned Players</a></b></li>\n";
print "  <li><b><a href=\"./franchise.cgi\" target=\"main\">Franchise Players</a></b></li>\n";
print "  <li><b><a href=\"./top20.cgi\" target=\"main\">Top Players</a></b></li>\n";
print "</ul>\n";
print "</td></tr>\n";

# Free Agent Market and Draft Section
print "<tr><td>\n";
print "<center><font color=\"#FFFFDF\">Free Agent and Draft</font></center>\n";
print "<ul>\n";
print "  <li><b><a href=\"./freeagent.cgi\" target=\"main\">Free Agent Market</a></b></li>\n";
#print "  <li><b><font color=\"#FFFFDF\">Draft Central</font></b></li>\n";
print "  <li><b><a href=\"./draft_central.cgi\" target=\"main\">Draft Central</a></b></li>\n";
print "  <li><b><font color=\"#FFFFDF\">Draft Results</font></b></li>\n";
#print "  <li><b><a href=\"./draft.cgi\" target=\"main\">Draft Results</a></b></li>\n";
print "</ul>\n";
print "</td></tr>\n";

print "</table>\n";

print "<p>\n";

print "<center>Help support the FFL via PayPal</center>\n";
print " <form action=\"https://www.paypal.com/cgi-bin/webscr\" method=\"post\">\n";
print " <input type=\"hidden\" name=\"cmd\" value=\"_donations\">\n";
print " <input type=\"hidden\" name=\"business\" value=\"dj\@seabass.org\">\n";
print " <input type=\"hidden\" name=\"item_name\" value=\"DJ FFL Support\">\n";
print " <input type=\"hidden\" name=\"no_shipping\" value=\"0\">\n";
print " <input type=\"hidden\" name=\"no_note\" value=\"1\">\n";
print " <input type=\"hidden\" name=\"currency_code\" value=\"USD\">\n";
print " <input type=\"hidden\" name=\"tax\" value=\"0\">\n";
print " <input type=\"hidden\" name=\"lc\" value=\"US\">\n";
print " <input type=\"hidden\" name=\"bn\" value=\"PP-DonationsBF\">\n";
print " <p><center><input type=\"image\" src=\"https://www.paypal.com/en_US/i/btn/btn_donate_LG.gif\" border=\"0\" name=\"submit\" alt=\"PayPal - The safer, easier way to pay online!\"></center>\n";
#print " <img alt=\"\" border=\"0\" src=\"https://www.paypal.com/en_US/i/scr/pixel.gif\" width=\"1\" height=\"1\">\n";
print " </form>\n";

# Website version control
# v1.0 - blue and white netcool motif
# v2.0 - dark blue on light blue background
# v3.0 - cream on dark green background
# v3.1 - organized side bar - moved html -> cgi links
# v3.2 - added free agent market link
# v3.3 - old message board, elimination challenge added
# v3.3.1 - added nfl opponents to weekly lineup
# v3.3.2 - added inverted helmets to indicate loss for elimination challenge
# v3.4 - added hall of records
# v3.4.1 - extended the "talk smack here" box to bigger size
# v3.4.2 - added elimincation challenge tool
# v3.4.3 - changed games back to percentage in standings
# v3.5 - moved main page to cgi and added smack talk and your matchups
# v3.5.1 - changed schedule from weekly games to personal season schedule for each manager
# v3.5.2 - changed smack talk to be non-link for guest login
# v3.5.3 - added Available Players link
# v3.6 - added PayPal button
# v3.7 - changed team page to have split tables for IR and Salary Penalty
# v3.7.1 - changed change_lineup to use player, position and team instead of just player
# v3.8 - added transaction request tool
# v3.8.1 - added owned tool - looks like I wrote it 5 years ago and never finished it
# v3.8.2 - removed player by position tool - looks like I wrote it 5 years ago and never finished it
# v3.8.3 - updated smack talk page to include smack time and number of times someone has talked smack
# v3.9 - restricted guest access to elimination, change lineup and smack talk
# v3.9.1 - added franchise player tool
# v3.10 - added draft central page
# v3.10.1 - added draft ranking tool but have not rolled it out to rest of league
# v3.10.2 - reorganized the side bar and added a table with borders to make it easier to find a specific tool
# v3.11 - added zombie kill of the week tool
# v3.11.1 - changed top20 to split out defense
# v3.11.2 - added NFL Week to Smack Talk and changed "Bye Weeks" to "NFL Bye Weeks" in side.cgi
# v3.11.3 - added admin_upd_team to change NFL teams for a player
# v3.11.4 - added admin_upd_contract to change a contract for a player
# v3.12 - reorganized sections and added Manager of the Week and Conhead of the Week links
# v3.12.1 - added admin_upd_points to update weekly points for a player
# v3.13 - Changed the NFL Bye Weeks to use the nfl_schedule table null entries
# v3.14 - Added the NFL Bye Week to the teams.cgi page


print "<font size=1><center>\n";

print "<p>\n";

print "<center><img src=\"http://www.djffl.net/images/PoweredByMacOSX.gif\"></center>\n";

print "<p>\n";
print "Website version 3.14<br>\n";

# Last Updated to give mgr's idea of when I have updated site
print "Last updated 16 October 2015\n";
print "</center></font>\n";
print end_html();
