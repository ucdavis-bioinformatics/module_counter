#!/usr/bin/perl

opendir($dh, $ARGV[0]);
my @files = grep { /^counts\.\d+_\d+\.out/ && -f "$ARGV[0]/$_" } readdir($dh);
closedir($dh);

%prev=();
%curr = ();
$num=1;
@files = sort @files;
open($fh,"<$files[0]");
while (<$fh>) {
    chomp;
    ($mod,$ver,$count) = split(/\t/,$_,3);
    $prev{$mod}{$ver} = $count;
}
close($fh);

foreach $file (@files[1 .. $#files]) {
    open($fh,"<$file");
    while (<$fh>) {
        chomp;
        ($mod,$ver,$count) = split(/\t/,$_,3);
        $curr{$mod}{$ver} = $count;
    }
    close($fh);

    foreach $mod (keys %curr) {
        foreach $ver (keys %{ $curr{$mod} }) {
            $diff = $curr{$mod}{$ver} - $prev{$mod}{$ver};
            print "$num\t$mod\t$ver\t$diff\n";
            $prev{$mod}{$ver} = $curr{$mod}{$ver};
        }
    }

    #%prev = %curr;
    $num++;
}
