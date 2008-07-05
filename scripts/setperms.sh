#!/bin/sh

for f in `find .`; do test -w $f && chmod go+w $f; done
