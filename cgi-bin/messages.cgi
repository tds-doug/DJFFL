#!/usr/bin/perl -w

use strict;
use DBI;
use CGI qw(:all);
use Time::Local;
use POSIX qw(strftime);
use Foozeball;

my $cgi_script="\/cgi-bin\/ffl_2015\/messages.cgi";

my $week = Foozeball::getweek();
#my $week = 17;

print header();
print start_html("Fantasy Football Message Board");

print "<body bgcolor=\"#132C06\" link=\"#FFFF80\" vlink=\"#FFFF80\" alink=\"#FFFF80\">\n";
print "<font face=\"Verdana\" color=\"#FFFFDF\">\n";

print "<h1><center><font color=\"#FFFF80\" face=\"Verdana\">Talk Smack If You Dare</font></center></h1>\n";

print "<table border=\"5\" width=\"100%\">";
print "<tr>\n";
print "<td width=\"15%\"><center><b><font color=\"#FFFF80\">Team Name</font></b></center></td>\n";
print "<td width=\"5%\"><center><b><font color=\"#FFFF80\">NFL Week</font></b></center></td>\n";
print "<td width=\"15%\"><center><b><font color=\"#FFFF80\">Smack Time</font></b></center></td>\n";
print "<td><center><b><font color=\"#FFFF80\">Message</font></b></center></td>\n";
print "<tr>\n";

my $server = 'localhost';
my $db = 'ffl_2015';
my $username = 'ffl';
my $password = 'foozeball';

my $dbh = DBI->connect("dbi:mysql:$db:$server", $username, $password);

my @c_time = (localtime);
my $currenttime = timelocal(@c_time);
my $messagetime = strftime "%e %b %Y %k:%M:%S", @c_time;


# put the self posted shit here

if (param( 'f_message' ))
{
  my $team = param( 'f_team');
  my $string = param( 'f_message');

  my $message = Foozeball::db_escape($string);
  my $text1 = substr($message, 0, 255);
  my $text2 = substr($message, 255, 510);
  my $text3 = substr($message, 510, 765);
 
  my $sql2 = "select count(*) from messages;";
  my $sth2 = $dbh->prepare($sql2);
  $sth2->execute();

  my $row2 = $sth2->fetchrow_arrayref;
  my $count = int($row2->[0]);

  my $sql3 = "insert into messages values ($count + 1,'$team','$messagetime',$week,'$text1','$text2','$text3');";
  my $sth3 = $dbh->prepare($sql3);
  $sth3->execute();
}

my $sql = "select * from messages order by id desc;";
my $sth = $dbh->prepare($sql);
$sth->execute();

while (my $row = $sth->fetchrow_arrayref)
{
  print "<tr>\n";
  if($row->[1] eq 'Armenia')
  {
    #print "<td><font color=\"#FF00FF\"><center>$row->[1]</center></font>";
    print "<td><center><font color=\"#FF0000\">A</font>";
    print "<font color=\"#FFA500\">r</font>";
    print "<font color=\"#FFFF00\">m</font>";
    print "<font color=\"#008000\">e</font>";
    print "<font color=\"#00FF00\">n</font>";
    print "<font color=\"#800080\">ia</font";
    print "</center></td>\n";
  }
  else
  {
    print "<td><font color=\"#FFFFDF\"><center>$row->[1]</center></font></td>\n";
  }

  if($row->[3] eq '0')
  {
    print "<td><font color=\"#FFFFDF\"><center>Pre-Season</center></font></td>\n";
  }
  else
  {
    print "<td><font color=\"#FFFFDF\"><center>$row->[3]</center></font></td>\n";
  }

  print "<td><font color=\"#FFFFDF\"><center>$row->[2]</center></font></td>\n";

  my $message = $row->[4] . $row->[5] . $row->[6];
  print "<td><font color=\"#FFFFDF\">$message</font></td>\n";

  print "<tr>\n";
}

print "</table>\n";

print "<p>\n";


# Get the remote user
my $ffl_manager = $ENV{'REMOTE_USER'};
my $ffl_team = Foozeball::get_ffl_team($ffl_manager);

print "<center><h3>Type your smack here</h3></center>\n";

my $sql_count = "select count(*) from messages where ffl_team = '$ffl_team';";
my $sth_count = $dbh->prepare($sql_count);
$sth_count->execute();

my $row_count = $sth_count->fetchrow_arrayref;

if ($row_count->[0] > 0)
{
  print "<font face=\"Verdana\" color=\"#FFFFDF\"><center>You have talked smack <b><font color=\"#FF0000\">$row_count->[0]</font></b> times.</center></font>\n";
}
else
{
  print "<font face=\"Verdana\" color=\"#FFFFDF\"><center>You have never talked smack!!!  What are you afraid of???.</center></font>\n";
}

print "<p>\n";

print "<form action=\"$cgi_script\" method=\"post\">\n";
print "<table>\n";
print "<tr>\n";
print "<td><font color=\"#FFFFDF\">Message:</font></td>\n";
print "<td><input type=text size=50 name=f_message value=\"\"></td>\n";
print "</tr>\n";
print "</table>\n";
print "<input type=hidden name=f_team value=\"$ffl_team\">\n";
print "<input type=submit value=\"Send Your Smack!\">\n";
print "</form>\n";

print end_html();

#sub db_escape() 
#{ 
#  my ( $string ) = @_; 
#  $string =~ s/\\/\\\\/g;
#  $string =~ s/'/\\'/g;
#  $string =~ s/-/\\-/g;
#  return( $string );
#}
