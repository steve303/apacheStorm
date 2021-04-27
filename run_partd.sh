#! /bin/bash
mvn clean package
storm jar ./target/storm-example-0.0.1-SNAPSHOT.jar org.apache.storm.flux.Flux --local -R /part_d_topology.yaml -s 30000
