#!/bin/sh

#go install mover.go && 
env GOOS=darwin GOARCH=amd64 go build -o copyfil mover.go
FROM=/Users/hesdx/Documents/ipfs/plotman/copyop/temp
TO=/Users/hesdx/Documents/ipfs/plotman/copyop/dst/

./copyfil $FROM $TO 10010001 farmm.log