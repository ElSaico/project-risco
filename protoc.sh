#!/bin/sh
protoc -I=proto --python_out=communication proto/communication.proto
