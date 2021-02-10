#!/usr/bin/perl -wT
$| = 1;
# reserveitem.cgi

use strict;

my $item;
my $itemhasnotbeenreserved;
my @temp;
my $temp;
my $time;
my $localtime;
my $selecteditem;
my $comments;
my $new_reserved_item_details;
my @reserveddetails;
my %reserveditems;

$ENV{PATH}='/sbin:/usr/sbin:/usr/bin:/usr/X11R6/bin:';
$time = scalar time();
$localtime = scalar localtime(time());

print "Content-type; text/html\n\n";

print "<HTML><HEAD>\n<TITLE>";
print "Item Reservation - Helen and Derek\'s wedding list.";
print "</TITLE>\n</HEAD>";

print "<BODY bgcolor=palegoldenrod>\n";

if ($ENV{'HTTP_REFERER'} !~ m#^http://www.todd.uklinux.net/#) {
    print "You may only enter this site via the homepage.\n </BODY></HTML>\n";
    exit;
}

# Get the ID of the item selected
@temp=split(/==/,$ENV{QUERY_STRING});
$selecteditem=$temp[1];

# Get any comments made
if ($ENV{'REQUEST_METHOD'} eq 'POST') {
    read (STFIN, $temp, $ENV('CONTENT_LENGTH'));
    @temp=split(/=/,$temp);
    $comments=$temp[1];
    $comments =~ tr/+/ /;
    $comments =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
    $comments = "No comment made" unless $comments;
    if ($comments =~ /^([a-fA-F0-9]\s.,()+}+)$/) {
        $comments = $1;
    }
    else {
        print "As a precaution against 'hackers' please enter letters and numbers only.";
        print "<P align=center><STRONG>Click <A href=\"reserveitemconfirm.cgi?item=$selecteditem\">here</A></STRONG>";
        print "</BODY></HTML>\n";
        exit;
    }
}
else {
    $comments = "ERROR: Post method not used.";
}
$comments =~ s/,/;/g; # check syntax

# Get the table details from a csv file and output as a perl data structure

# Get a list of items already selected

# First, read the csv file into an array...
open (RESERVEDITEMS, "+>> reserveditems.cgi") || die "<P>ERROR; Couldn't open reserved list";
flock (RESERVEDITEMS, 2) or die "<P>Can't lock file list:$!</P>\n";
seek (RESERVEDITEMS, 0, 0);
@temp = <RESERVEDITEMS>;

# Now generate a hash
%reserveditems=();
foreach $item (@temp) {
    my @list=split(/,/, $item);
    $reserveditems{ shift (@list) }= \@list;
}

# Check someone else hasn't beaten us to ths item!

$itemhasnotbeenreserved= 1;
if (exit $reserveditems{$selecteditem}) {
    @reserveddetails = @{ $reserveditems{$selecteditem} };
    if ($reserveddetails[0] eq "reserve") {
        $itemhasnotbeenreserved = 0;
    }
}

if ($itemhasnotbeenreserved) {
    # OK to 'unreserve' it; add transaction record to list.
    $new_reserved_item_details=$selecteditem\,reserve\,$ENV{'REMOTE_USER'}\,$localtime; # check this
    foreach $item(keys %ENV) {
        $new_reserved_item_details .= "\,";
        $new_reserved_item_details .= join "=", $item, $ENV{$item};
    }
    
}







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