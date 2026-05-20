#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);

my $cgi_script="\/cgi-bin\/ffl_2015\/fam.cgi";

print header();
print start_html("Fantasy Football Free Agent Market");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center>Free Agent Market</center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"40%\"><center><b><font color=\"#FFFFDF\">Player</font></b></center></td>\n";
print "<td width=\"40%\"><center><b><font color=\"#FFFFDF\">FFL Team</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">Start Bid</font></b></center></td>\n";
print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">Winning Bid</font></b></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my $sql = "select * from free_agent_market order by id asc;";
my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
    print "<td width=\"40%\"><center><b><font color=\"#FFFFDF\">$row->[1]</font></b></center></td>\n";
    print "<td width=\"40%\"><center><b><font color=\"#FFFFDF\">$row->[2]</font></b></center></td>\n";
    print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">$row->[3]</font></b></center></td>\n";
    print "<td width=\"10%\"><center><b><font color=\"#FFFFDF\">$row->[4]</font></b></center></td>\n";
  print "<tr>\n";
}

print "</table>\n";

print end_html();

sub db_escape() 
{ 
  my ( $string ) = @_; 
  $string =~ s/\\/\\\\/g;
  $string =~ s/'/\\'/g;
  return( $string );
}

