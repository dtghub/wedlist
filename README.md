# wedlist
#
# This is a late draft of the PERL code I wrote for a cgi based Wedding list - used for our actual wedding list around 20 years ago.
#
# The code dynamically generated a series of tables using the data imported from a csv file, which also marked items as 'reserved' or presented a reserve button if the item had not been reserved by someone else - if it had been reserved by you, you also had the option to 'unreserve' the item
#
# The idea was to keep things as simple as possible to min9imise the potential for bugs. The list of reserve and unreserve transactions were recorded and the transactions were played back into the list just before each rendering of the list. Since it was a multi-user website, the chances of a race condition for two users attempting to reserve he same item simultaneously were minimised by presenting a 'confirm' stage before the reservation was completed. 
#
#
#
