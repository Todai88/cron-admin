#!/bin/sh

# run the tests with the correct env
# Pass nosetest switches if you want e.g. -v

ENV=test nosetests $*
