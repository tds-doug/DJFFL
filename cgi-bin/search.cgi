#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Foozeball;

my $cgi_script = "\/cgi-bin\/ffl_2015\/search.cgi";

my $week = Foozeball::getweek();
#my $week = 17;

print header();
print start_html("Fantasy Football Players");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Looking For Someone?</font></center></h1>\n";
print "<p>\n";

if(param( 'f_player' ))
{

  my $player = param( 'f_player' );

  print "<center><h3>Results for $player</h3></center>\n";

  print "<table border=\"5\" width=\"100%\">";
  print "<tr>\n";
  print "<td><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
  print "<td><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
#  print "<td><center><b>Contracted Thru</b></center></td>\n";
  print "<td><center><b><font color=\"#FFFFDF\">Fantasy Salary</font></b></center></td>\n";
  print "<td><center><b><font color=\"#FFFFDF\">Points This Season</font></b></center></td>\n";

  my $i;
  for ($i = 1; $i <= $week; $i++)
  {
    print "<td><center><b><font color=\"#FFFFDF\">Week $i Pts</font></b></center></td>\n";
  }

  print "<tr>\n";

  my $server = 'localhost';
  my $db = 'ffl_2015';
  my $username = 'ffl';
  my $password = 'foozeball';

  my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

  my $sql = "(select * from ffl_2015.players_QB where player like '%$player%')"
          . " union (select * from ffl_2015.players_WR where player like '%$player%')"
          . " union (select * from ffl_2015.players_RB where player like '%$player%')"
          . " union (select * from ffl_2015.players_TE where player like '%$player%')"
          . " union (select * from ffl_2015.players_K where player like '%$player%')"
          . " union (select * from ffl_2015.players_DEF where player like '%$player%')"
          . " order by player asc;";

  my $sth = $dbh->prepare($sql);
  $sth->execute();

  my $salary = 0;

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<tr>\n";
    print "  <td><center><font color=\"#FFFFDF\">$row->[0] ($row->[7]-$row->[1])</font></center></td>\n";

# Added this logic for IR players
    if($row->[2]=~/([A-Za-z0-9 ]+) - Injured Reserve/)
    {
      my $temp_ffl_team = $1;
      print "  <td><center><a href=\"./teams.cgi?f_team=$temp_ffl_team&f_order=total_pts\">$temp_ffl_team</a></center></td>\n";
    }
    else
    {
      print "  <td><center><a href=\"./teams.cgi?f_team=$row->[2]&f_order=total_pts\">$row->[2]</a></center></td>\n";
    }

# This was the Contract Thru part, but I don't think it is relevant here
#    if($row->[6] eq '0')
#    {
#      print "  <td><center>N\/A</center></td>\n";
#    }
#    else
#    {
#      print "  <td><center>$row->[5]</center></td>\n";
#    }

# This is the Fantasy Salary part
    if($row->[6] eq '0')
    {
      print "  <td><center><font color=\"#FFFFDF\">\$$row->[26]</font></center></td>\n";
    }
    else
    {
      print "  <td><center><font color=\"#FFFFDF\">\$$row->[6]</font></center></td>\n";
    }

    print "  <td><center><font color=\"#FFFFDF\">$row->[25]</font></center></td>\n";

  my $m;
  for ($m = 1; $m <= $week; $m++)
  {
    my $n = $m + 7;
    print "  <td><center><font color=\"#FFFFDF\">$row->[$n]</font></center></td>\n";
  }

    print "</tr>\n";

  }

  print "</table>\n";

  print "<p>\n";

}
else
{
  print "<form action=\"$cgi_script\" method=\"post\">\n";
  print "<table>\n";

  print "<tr>\n";
  print "<td><font color=\"#FFFFDF\">Last Name:</font></td>\n";
  print "<td><input type=text name=f_player value=\"\"></td>\n";
  print "</tr>\n";

  print "</table>\n";

  print "<input type=submit value=\"Submit\">\n";
  print "</form>\n";
}
print end_html();
