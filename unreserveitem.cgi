#!/usr/bin/perl -wT
$| = 1;
# unreserveitem.cgi

use strict;

my $item;
my $itemhasnotbeenreserved;
my @temp;
my $time;
my $localtime;
my $selecteditem;
my $new_reserved_item_details;
my @reserveddetails;
my %reserveditems;

print "Content-type; text/html\n\n";

print "<HTML><HEAD>\n<TITLE>";
print "Item Reservation - Helen and Derek\'s wedding list.";
print "</TITLE>\n</HEAD>";

print "<BODY bgcolor=palevioletred>\n";

if ($ENV{'HTTP_REFERER'} !~ m#^http://www.todd.uklinux.net/#) {
    print "You may only enter this site via the homepage.\n </BODY></HTML>\n";
    exit;
}

$time = scalar time();
$localtime = scalar localtime(time());

# Get the ID of the item selected
@temp=split(/==/,$ENV{QUERY_STRING});
$selecteditem=$temp[1];


# Get the table details from a csv file and output as a perl data structure

# Get a list of items already selected

# First, read the csv file into an array...
open (RESERVEDITEMS, "+>> reserveditems.cgi") || die "<P>ERROR; Couldn't open reserved list.</P>\n";
flock (RESERVEDITEMS, 2) or die "<P>Can't lock file list:$!</P>\n";
seek (RESERVEDITEMS, 0, 0);
@temp = <RESERVEDITEMS>;

# Now generate a hash
%reserveditems=();
foreach $item (@temp) {
    my @list=split(/,/, $item);
    $reserveditems{ shift (@list) }= \@list;
}

# Double check that it's safe to unreserve ths item!

$itemhasnotbeenreserved= 1;
if (exists $reserveditems{$selecteditem}) {
    @reserveddetails = @{ $reserveditems{$selecteditem} };
    if ($reserveddetails[0] eq "reserve") {
        $itemhasnotbeenreserved = 0;
    }
}

@reserveddetails = @{ $reserveditems{$selecteditem}};




if ($itemhasnotbeenreserved) {
    # OK to 'unreserve' it; add transaction record to list.
    $new_reserved_item_details=$selecteditem\,reserve\,$ENV{'REMOTE_USER'}\,$localtime; # check this
    foreach $item(keys %ENV) {
        $new_reserved_item_details .= "\,";
        $new_reserved_item_details .= join "=", $item, $ENV{$item};
    }
    seek (RESERVEDITEMS, 0, 2);
    print RESERVEDITEMS "$new_reserved_item_details\n";
}
else {
    print "<P>Oops, somethings's gone wrong, I'm afraid. (Better explanation to go here)\n";
    flock (RESERVEDITEMS, 8);
    close (RESERVEDITEMS);
    exit;
}
flock (RESERVEDITEMS, 8);
close (RESERVEDITEMS);

open MAIL, "/usr/bin/sendmail -f" or die "<P> Error in emailing reservation. Please let us know, thanks! $!</P>\n";
print MAIL, "To: made@up.email, addresses@@list\r\n";
print MAIL, "From: Wedding List<made@up.email>\r\n";
print MAIL, "Subject: Test2: $selecteditem\r\n\r\n";
print MAIL, "$new_reserved_item_details\n";
close MAIL or die "<P>ERROR; Couldn't complete EMail notification:$!</P>\n";

print "<P>&nbsp;</P>\n";
print "<P>&Thank you. Your selected item $selecteditem has been reserved.;</P>\n";

print "<P>&nbsp;</P>\n";
print "<P>&nbsp;</P>\n";

print "<P align=center><STRONG>Click <A href=\"wedtable.cgi?item=$selecteditem\">here</A></STRONG></P>\n";

print "</BODY></HTML>\n";



