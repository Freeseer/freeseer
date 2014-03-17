#!/bin/bash

function run_or_fail {
    WORKING_DIR="$1";
    COMMAND=$2;

    pushd $WORKING_DIR > /dev/null;
    echo "@RUNNING: $COMMAND";
    $COMMAND; STATUS=$?;
    echo "@EXIT WITH STATUS: $STATUS";
    popd > /dev/null;

    if [ $STATUS -ne 0 ]; then
        echo '@FAILING...';
        exit $STATUS;
    fi
    echo;
}

function run_and_continue {
    WORKING_DIR="$1";
    COMMAND=$2;

    pushd $WORKING_DIR > /dev/null;
    echo "@RUNNING: $COMMAND";
    $COMMAND; STATUS=$?;
    echo "@EXIT WITH STATUS: $STATUS";
    popd > /dev/null;
    echo;
}

# Make sure we're in the root of the git repo
cd "$(git rev-parse --show-toplevel)"

# First lint and check "PEP8" compliance
run_or_fail "." "flake8 src";

# Run unit tests
run_or_fail "src" "coverage run setup.py test"

# Upload unit test results to coveralls
run_and_continue "src" "coveralls"

# Build documentation
run_or_fail "docs" "make html"
