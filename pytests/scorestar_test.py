import abiflib
import pytest
import re
from subprocess import run, PIPE
from abiftestfuncs import *

LOGOBJ = abiflib.LogfileSingleton()

@pytest.mark.parametrize(
    'cmd_args, inputfile, pattern',
    [
        (['-t', 'jabmod', '--add-scores'],
         'testdata/tenn-example/tennessee-example-simple.abif',
         r"                    \"rating\": 3"),
        (['-t', 'jabmod'],
         'testdata/tenn-example/tennessee-example-scores.abif',
         r"                    \"rating\": \"133\""),
        (['-t', 'jabmod', '--add-scores'],
         'testdata/tenn-example/tennessee-example-scores.abif',
         r"                    \"rating\": \"133\""),
        (['-t', 'text', '-m', 'score'],
         'testdata/tenn-example/tennessee-example-scores.abif',
         r"19370 points \(from 100 voters\) -- Knoxville, TN"),
        (['-t', 'text', '-m', 'STAR'],
         'testdata/tenn-example/tennessee-example-STAR.abif',
         r"261 stars \(from 100 voters\) -- Nashville, TN"),
        (['-t', 'text', '-m', 'STAR'],
         'testdata/tenn-example/tennessee-example-STAR.abif',
         r"Nashville, TN preferred by 68 of 100 voters"),
        (['-t', 'text', '-m', 'STAR'],
         'testdata/tenn-example/tennessee-example-STAR.abif',
         r"Winner: Nashville, TN"),
        (['-t', 'text', '-m', 'STAR'],
         'testdata/tenn-example/tennessee-example-STAR-score-difference.abif',
         r"STAR Winner: Chattanooga, TN"),
        (['-t', 'text', '-m', 'score'],
         'testdata/tenn-example/tennessee-example-STAR-score-difference.abif',
         r"Score Winner: Knoxville, TN"),
        (['-t', 'text', '-m', 'Copeland'],
         'testdata/tenn-example/tennessee-example-STAR-score-difference.abif',
         r"Copeland Winner: Nashville, TN"),
        (['-t', 'text'],
         'testdata/tenn-example/tennessee-example-STAR-score-difference.abif',
         r"Nash \(3-0-0\)"),
        (['-t', 'text', '-m', 'score'],
         'testdata/commasep/jman722-example.abif',
         r"88 points \(from 19 voters\) -- Allie"),
        (['-t', 'text', '-m', 'score'],
         'testdata/commasep/tn-example-missing-scores.abif',
         r"17480 points \(from 58 voters\) -- Knoxville"),
        (['-t', 'text', '-m', 'score'],
         'testdata/commasep/tn-example-scores-and-commas.abif',
         r"19370 points \(from 100 voters\) -- Knoxville"),
    ]
)

def test_grep_output_for_regexp(cmd_args, inputfile, pattern):
    """Testing text output from abiftool.py for regexp"""
    # TODO: merge this with the version in debtally_test.py
    try:
        fh = open(inputfile, 'rb')
    except:
        msg = f'Missing file: {inputfile}'
        msg += "Please run './fetchmgr.py *.fetchspec.json' "
        msg += "if you haven't already"
        pytest.skip(msg)
    abiftool_output = get_abiftool_output_as_array(cmd_args)
    LOGOBJ.log("LOGOBJ test_grep_for_regexp/scorestar" +
               f"{inputfile=} {pattern=}\n")
    assert check_regex_in_output(cmd_args, inputfile, pattern)
    return None
