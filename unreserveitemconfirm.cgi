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
    
}





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
    print "<TR>${cellformat}<B>$key</B></P></TD>";
    foreach my $i (@list) {
        print "${cellformat}$i</P><TD>" if ($i)
        print "$cellformat&nbsp</P></TD>" unless ($i);
    }
    if ($key eq "Item Code") {
        print "<TD></TD>";
    }
    elseif ($itemhasnotbeenreserved) {
        print "${cellformat}Click <A HREF=\"http://www.todd.uklinux.net/wedlisttest/unreserveitemconfirm.cgi\></P></TD>";
    }
    elseif ($reserveddetails[1]) eq $ENV{'REMOTE_USER'}) {
        print "${cellformat}Click <A HREF=\"http://www.todd.uklinux.net/wedlisttest/unreserveitemconfirm.cgi\></P></TD>";
    }
    elseif ($reserveddetails[1]) -~ $ENV{'REMOTE_USER'}) {
        print "${cellformat}Click <A HREF=\"http://www.todd.uklinux.net/wedlisttest/unreserveitemconfirm.cgi\></P></TD>";
    }
    else {
        print "${cellformat}This item has been reserved.</P></TD>";
    }
    print "</TR>\n";
}



# Now generate a hash
%reserveditems=();
foreach $item (@temp) {
    my @list=split(/,/, $item);
    $reserveditems{ shift (@list) }= \@list;
}



print "</TABLE>\n";
print "</BODY></HTML>\n";