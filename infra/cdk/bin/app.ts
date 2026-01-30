#!/usr/bin/env node
import * as cdk from "aws-cdk-lib";
import { BedrockKbWithS3SourceStack } from "../lib/bedrock-kb-with-s3-source-stack";

const app = new cdk.App();

new BedrockKbWithS3SourceStack(app, "BedrockKbWithS3SourceStack", {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: "ap-southeast-2"
  },
});
