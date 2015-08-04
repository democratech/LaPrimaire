#!/bin/bash
grep -A 1 '"name"' $1 > $1.emails
sed -i '/--/d' $1.emails
sed -i '/class=/d' $1.emails
sed -i -e 's/^[ \t]*//' $1.emails
