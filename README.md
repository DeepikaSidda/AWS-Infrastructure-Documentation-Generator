# AWS Infrastructure Documentation Generator

An automated tool for AWS infrastructure documentation, visualization, and compliance reporting.

## Features

- **Infrastructure Scanning**: Auto-discovers AWS resources and their metadata
- **Architecture Diagrams**: Generates visual representations of your infrastructure
- **Documentation**: Creates human-readable documentation for all resources
- **Change Tracking**: Monitors and records infrastructure changes over time
- **Compliance Reporting**: Validates infrastructure against security rules and generates reports

## Step-by-Step Setup and Execution Guide

### 1. Prerequisites Setup

1. Ensure you have Python 3.8+ installed on your system
2. Configure AWS credentials using one of these methods:
   - AWS CLI: Run `aws configure`
   - Environment variables: Set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
   - IAM role: If running on AWS infrastructure

### 2. Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aws-infra-doc-gen
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

1. Review and customize `config/config.yaml`:
   - Set AWS regions to scan
   - Select resources to document (ec2, s3, rds, lambda, vpc, apigateway)
   - Configure output formats (html, markdown, pdf)
   - Enable/disable change tracking
   - Set compliance checking options

2. Review and customize `config/compliance_rules.yaml`:
   - Adjust security rules for EC2 (encryption, instance types)
   - Configure S3 security policies (encryption, public access)
   - Set RDS requirements (encryption, multi-AZ)
   - Define Lambda function rules (runtimes, VPC config)

### 4. Execution Workflow

1. **Infrastructure Scanning**:
   ```bash
   python -m aws_infra_doc_gen scan --region us-east-1
   ```
   - Discovers all AWS resources in specified regions
   - Collects detailed metadata and configurations
   - Stores results in memory for processing

2. **Documentation Generation**:
   ```bash
   python -m aws_infra_doc_gen generate-docs
   ```
   - Processes scanned data
   - Uses templates from `templates/` directory
   - Generates documentation in configured formats
   - Output saved to `output/` directory

3. **Architecture Diagram Creation**:
   ```bash
   python -m aws_infra_doc_gen create-diagrams
   ```
   - Creates visual infrastructure diagrams
   - Generates both PNG and SVG formats
   - Shows resource relationships and connections

4. **Compliance Checking**:
   ```bash
   python -m aws_infra_doc_gen compliance-check
   ```
   - Validates infrastructure against rules in compliance_rules.yaml
   - Checks encryption, security, and best practices
   - Generates compliance report in HTML or JSON format

5. **Change Tracking** (if enabled):
   - Automatically tracks infrastructure changes
   - Stores history in Git repository or S3 bucket
   - Maintains version control of documentation

### 5. Output Structure

The tool generates the following outputs in the `output/` directory:
- Documentation files (HTML, Markdown, PDF)
- Architecture diagrams (PNG, SVG)
- Compliance reports
- Change history (if tracking enabled)

## Project Structure

```
aws-infra-doc-gen/
├── src/
│   ├── scanner/         # AWS resource discovery and metadata collection
│   ├── visualizer/      # Architecture diagram generation
│   ├── documentation/   # Documentation generation
│   ├── tracker/         # Change tracking and version control
│   └── compliance/      # Compliance validation and reporting
├── tests/              # Unit and integration tests
├── config/             # Configuration files
│   ├── config.yaml     # Main configuration
│   └── compliance_rules.yaml  # Security and compliance rules
├── templates/          # Documentation templates
└── output/            # Generated documentation and reports
```

## Configuration Example

```yaml
aws:
  regions: ['us-east-1']
  resources:
    - ec2
    - s3
    - rds
    - lambda
    - vpc
    - apigateway

output:
  directory: ./output
  format:
    - html
    - markdown
    - pdf
  diagrams:
    - png
    - svg

change_tracking:
  enabled: true
  storage: git  # or 's3'
  config:
    repo_path: ./history

compliance:
  enabled: true
  rules_file: ./config/compliance_rules.yaml
  report_format: html
```

## Troubleshooting

1. **AWS Credentials Issues**:
   - Verify AWS credentials are properly configured
   - Ensure IAM permissions include required services

2. **Scanning Failures**:
   - Check network connectivity to AWS
   - Verify region settings in config.yaml
   - Ensure resource permissions are correct

3. **Output Generation Issues**:
   - Check write permissions in output directory
   - Verify template files exist and are valid
   - Ensure required dependencies are installed

## License

MIT License

#   A W S - I n f r a s t r u c t u r e - D o c u m e n t a t i o n - G e n e r a t o r  
 