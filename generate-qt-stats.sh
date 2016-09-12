#!/bin/bash
statbranches="master stable9"
sourcedir=$1
pwd=$(pwd)

run_stats() {
    local name=$1
    shift
    perl $pwd/stats.pl --no-recurse --gnuplot $name --limit 10 --refs 'refs/heads/*' "$@"
    gnuplot $name.gnuplot
#     rm -f $name.employer.total.png
}

run_module() {
    local name=$1
    shift
    # regular 16-week stats
    run_stats $name "$@"
    # full-time
    run_stats $name-full --since Oct.24.2011 "$@"
}

run_branchstats() {
    local name=$1
    local branches=$2
    shift 2
    $pwd/perl stats.pl --no-recurse --no-author --no-employer --branches --gnuplot $name.branch --refs "$branches" "$@"
    gnuplot $name.branch.gnuplot
    mv -f $name.branch.branch.absolute.png $name.branch.absolute.png
    mv -f $name.branch.branch.relative.png $name.branch.relative.png
    mv -f $name.branch.branch.csv $name.branch.csv
    rm -f $name.branch.branch.*
}

run_branchstats_module() {
    local name=$1
    local branches=$2
    shift 2
    # nine-month branch stats
    run_branchstats $name "$branches" --since nine.months.ago "$@"
    # full-time
    run_branchstats $name-full "$branches" --since Oct.24.2011 "$@"
}

now=$(date +%F)
output=$(pwd)/output/$now
mkdir -p $output

# Update core
cd $sourcedir
git fetch -f >/dev/null

# Generate stats for qtbase
cd $output
# run_module core $sourcedir
# run_branchstats_module core "$statbranches" $sourcedir

# wait %1 || true

# Do the whole project now
run_module core-all $sourcedir
