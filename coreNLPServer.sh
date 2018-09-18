#!/bin/bash
# Run Stanford CoreNLP Server
# Parameter:
# 	$1: maximum heap size
# 	$2: port number

if [ -z "$1" ]
then
	mem=4
else
	mem=$1
fi

if [ -z "$2" ]
then
	port=9000
else
	port=$2
fi

echo Execute Command: java -mx"$mem"g edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port "$port" -timeout 15000
java -mx"$mem"g edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port "$port" -timeout 15000
