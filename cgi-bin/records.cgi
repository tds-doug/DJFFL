#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my @categories = ('Single Game Scoring','Season Scoring','Win/Lose Streaks','Season Record','Fantasy Bowl','Challenges');
my $category;
my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';
my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

print header();
print start_html("Fantasy Football Records");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font face=\"Verdana\" color=\"#FFFF80\">Fantasy Football Hall of Records</font></center></h1>\n";

foreach $category (@categories)
{
  print "<h2><center><b><font color=\"#FFFFDF\">$category</font></b></center></h2>\n";

  print "<table align=\"center\" border=\"5\" width=\"80%\">";
  print "<tr>\n";
  #print "<td><center><b><font color=\"#FFFFDF\">Category</font></b></center></td>\n";
  print "<td><center><b><font color=\"#FFFFDF\">Record Title</font></b></center></td>\n";
  print "<td><center><b><font color=\"#FFFFDF\">Record Value</font></b></center></td>\n";
  print "<td><center><b><font color=\"#FFFFDF\">FFL Season(s)</font></b></center></td>\n";
  print "<td><center><b><font color=\"#FFFFDF\">Record Holder(s)</font></b></center></td>\n";
  print "<tr>\n";

  my $sql = "select * from records2 where category = '$category' order by id asc;";
  my $sth = $dbh->prepare($sql);
  $sth->execute();

  while (my $row = $sth->fetchrow_arrayref)
  {
    print "<tr>\n";
    #print "<td><center><font color=\"#FFFFDF\">$row->[1]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[2]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[3]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[4]</font></center></td>\n";
    print "<td><center><font color=\"#FFFFDF\">$row->[5]</font></center></td>\n";
    print "<tr>\n";
  }

  print "</table>\n";
  print "<p>\n";
}

print end_html();
