import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as s3 from "aws-cdk-lib/aws-s3";
import * as iam from "aws-cdk-lib/aws-iam";
import * as bedrock from "aws-cdk-lib/aws-bedrock";

export class BedrockKbWithS3SourceStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ======== CONFIG (safe defaults, no project-specific refs) ========
    const kbName = "bedrock-kb";
    const embeddingModelArn =
      "arn:aws:bedrock:ap-southeast-2::foundation-model/amazon.titan-embed-text-v2:0";

    // OpenSearch Serverless collection ARN MUST be supplied by you
    const aossCollectionArn = cdk.Fn.importValue("AossCollectionArn");

    const vectorIndexName = "bedrock-knowledge-base-index";
    const vectorField = "vector";
    const textField = "text";
    const metadataField = "metadata";
    // ================================================================

    // Execution role for the Knowledge Base (created cleanly by CDK)
    const kbRole = new iam.Role(this, "BedrockKnowledgeBaseRole", {
      assumedBy: new iam.ServicePrincipal("bedrock.amazonaws.com"),
    });

    // S3 bucket to hold source documents for the KB
    const docsBucket = new s3.Bucket(this, "KbDocsBucket", {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      encryption: s3.BucketEncryption.S3_MANAGED,
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    });

    const docsPrefix = "kb/";

    // Allow the KB execution role to read the docs bucket/prefix
    docsBucket.grantRead(kbRole, `${docsPrefix}*`);

    // Knowledge Base
    const kb = new bedrock.CfnKnowledgeBase(this, "KnowledgeBase", {
      name: kbName,
      roleArn: kbRole.roleArn,
      knowledgeBaseConfiguration: {
        type: "VECTOR",
        vectorKnowledgeBaseConfiguration: {
          embeddingModelArn,
        },
      },
      storageConfiguration: {
        type: "OPENSEARCH_SERVERLESS",
        opensearchServerlessConfiguration: {
          collectionArn: aossCollectionArn,
          vectorIndexName,
          fieldMapping: {
            vectorField,
            textField,
            metadataField,
          },
        },
      },
    });

    // S3 Data Source
    const ds = new bedrock.CfnDataSource(this, "S3DataSource", {
      name: "kb-s3-data-source",
      knowledgeBaseId: kb.attrKnowledgeBaseId,
      dataSourceConfiguration: {
        type: "S3",
        s3Configuration: {
          bucketArn: docsBucket.bucketArn,
          inclusionPrefixes: [docsPrefix],
        },
      },
      vectorIngestionConfiguration: {
        parsingConfiguration: {
          parsingStrategy: "BEDROCK_DATA_AUTOMATION",
        },
      },
      dataDeletionPolicy: "DELETE",
    });

    new cdk.CfnOutput(this, "DocsBucketName", {
      value: docsBucket.bucketName,
    });

    new cdk.CfnOutput(this, "DocsPrefix", {
      value: docsPrefix,
    });

    new cdk.CfnOutput(this, "KnowledgeBaseId", {
      value: kb.attrKnowledgeBaseId,
    });

    new cdk.CfnOutput(this, "DataSourceId", {
      value: ds.attrDataSourceId,
    });
  }
}
