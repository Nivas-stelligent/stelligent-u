#!/bin/bash

regions=($(jq -r '.regions[]' labs1.3.1-regions.json))

for region in "${regions[@]}"; do
  stack_name="test-stack-$region"
  aws cloudformation create-stack --stack-name $stack_name --template-body file://labs1.3.1.yaml --region $region
done