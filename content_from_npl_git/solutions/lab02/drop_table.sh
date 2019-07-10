#!/usr/bin/env sh

(echo "disable '$USER'" && echo "drop '$USER'") |  hbase shell

