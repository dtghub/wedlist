#!/usr/bin/perl -wT
$| = 1;
# unreserveitemconfirm.cgi



use strict;
my $item;
my $itemhasnotbeenreserved;
my $key;
my @wedfile;
my @temp;
my $time;
my $selecteditem;
my @reserveddetails;
my %reserveditems;
my $comments;

print "Content-type; text/html\n\n";

print "<HTML><HEAD>\n<TITLE>";
print "Confirm Cancelled Item - Helen and Derek\'s wedding list.";
print "</TITLE>\n</HEAD>";

print "<BODY BGCOLOR=\"#cc66cc\">\n";

if ($ENV{'HTTP_REFERER'} !~ m#^http://www.todd.uklinux.net/#) {
    print "You may only enter this site via the homepage.\n </BODY></HTML>\n";
    exit;
}

print "<H2>Please confirm your cancelled item;</H2>";

# Get the ID of the item selected
@temp=split(/==/,$ENV{QUERY_STRING});
$selecteditem=$temp[1];

# Get the table details from a csv file and output as a perl data structure

# First, read the csv file into an array...
open (TEMP, "<wedtablelist.cgi");
@wedfile = <TEMP>;
close (TEMP);

print "<TABLE align=center border bgcolor=aqua cellpadding=2 width=95\%>";

# Now, locate and dispay the selected item
foreach $item (@wedfile) {
    my @list=split(/,/, $item);
    $key=shift(@list);
    if ($key eq $selecteditem) {
        print "<TR><TD><B>$key</B>";
        foreach my $i (@list) {
            print "<TD>$i";
            print "&nbsp" unless ($i);
        }
        print "</TR>\n";
    }

print "</TABLE>\n";

open (TEMP, "<reserveditems.cgi") || die "<P>ERROR; Couldn't open reserved list.";
@temp = <TEMP>;
close (TEMP);

# Now generate a hash

foreach $item (@temp) {
    my @list=split(/,/, $item);
    $reserveditems{ shift (@list) }= \@list;
}
@reserveddetails = @{$reserveditems{$selecteditem}};

# Check no-one's been editing location info.
if (($ENV{'REMOTE_USER'} eq $reserveddetails[1]) or ("derekhelenatodd" =~ $ENV{'REMOTE_USER'})) {
    print "<P>Reserved by; $reserveddetails[1]</P>\n";
    print "<P>&nbsp;</P>\n";
    print "<P>Reserved at; $reserveddetails[2]</P>\n";
    print "<P>&nbsp;</P>\n";
    $comments=$reserveddetails[3];
    $comments =~ s/;/,/g;
    print "<P>Comments; $comments</P>\n";
    print "<P>&nbsp;</P>\n";
    print "<P>&nbsp;</P>\n";

    $time = scalar time();
    print "<P align=center><STRONG>Click <A href=\"unreserveitem.cgi?item=$selecteditem\">here</A></STRONG>";
    print "FORM action=\"unreserveitem.cgi\" method=post>";
    print "INPUT type=submit value=\"Cancel Reservation\">";
    print "</FORM>";
}

print "</BODY></HTML>\n";