#!/usr/bin/perl -wT
$| = 1;
# wedtable.cgi



use strict;
my $item;
my $itemhasnotbeenreserved;
my $key;
my @wedfile;
my @temp;
my %reserveditems;
my @reserveddetails;
my $cellformat;

print "Content-type; text/html\n\n";

print "<HTML><HEAD>\n<TITLE>";
print "Helen and Derek\'s wedding list";
print "</TITLE>\n</HEAD>";

print "<BODY BGCOLOR=\"#9933ff\">\n";

if ($ENV{'HTTP_REFERER'} !~ m#^http://www.todd.uklinux.net/#) {
    print "You may only enter this site via the homepage.\n </BODY></HTML>\n";
    exit;
}

print "<H2>The wedding list</H2>";

# Get a list of items already selected

# First, read the csv file into an array...
open (TEMP, "<reserveditems.cgi") || die "<P>ERROR; Couldn't open reserved list";
@temp = <TEMP>;
close (TEMP);

# Now generate a hash
%reserveditems=();
foreach $item (@temp) {
    my @list=split(/,/, $item);
    $reserveditems{ shift (@list) }= \@list;
}




# Get the table details from a csv file and output to the display

# First, read the csv file into an array...
open (TEMP, "wedtablelst.cgi") || die "<P>ERROR; Couldn't open wedding list file";
@wedfile = <TEMP>;
close (TEMP);

print "<TABLE align=center border bgcolor=aqua cellpadding=2 width=95\%>";

# Now, build a table
foreach $item (@wedfile) {
    my @list=split(/,/, $item);
    $key=shift(@list);
    $itemhasnotbeenreserved = 1;
    $reserveddetails = ();
    if (exists $reserveditems{$key}) {
        @reserveddetails = @{  $reserveditems{$key} };
        if ($reserveddetails[0] eq "reserve") {
            $itemhasnotbeenreserved = 0;
        }
    }
    if ($itemhasnotbeenreserved) {
        $cellformat="<TD BGCOLOR=\"#ffffcc\"><P>";
    }
    elseif ($reserveddetails[1] eq $ENV('REMOTE_USER')) {
        $cellformat = "<TD BGCOLOR=\"#99ccff\"><P>";
    }
    else {
        $cellformat="<TD BGCOLOR=\"#acafff\"><P>";
    }
    if ($key eq "Iem Code") {
        $cellformat="TD BGCOLOR=\"#6699ff\"><P ALIGN=CENTER>";
    }
    print "<TR>${ cellformat }<B>$key</B></P></TD>";
    foreach my $i (@list) {
        print "${ cellformat }$i</P><TD>" if ($i)
        print "$cellformat&nbsp</P></TD>" unless ($i);
    }
    if ($key eq "Item Code") {
        print "<TD></TD>";
    }
    elseif ($itemhasnotbeenreserved) {
        print "${ cellformat }Click <A HREF=\http://www.todd.uklinux.net"
    }
}