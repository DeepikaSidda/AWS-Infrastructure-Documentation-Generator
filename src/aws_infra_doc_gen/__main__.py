import click
import yaml
import os
import json
from datetime import datetime
from .scanner.aws_scanner import AWSResourceScanner
from .visualizer.diagram_generator import ArchitectureDiagramGenerator
from .documentation.doc_generator import DocumentationGenerator
from .tracker.change_tracker import ChangeTracker
from .compliance.compliance_checker import ComplianceChecker
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom datetime converter function to serialize datetime objects to ISO format
def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()  # Convert datetime to ISO format string
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

# Utility function to ensure that all datetime objects are converted within a dict or list
def convert_datetimes(data):
    if isinstance(data, dict):
        return {key: convert_datetimes(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_datetimes(item) for item in data]
    elif isinstance(data, datetime):
        return datetime_converter(data)
    else:
        return data

@click.group()
def cli():
    """AWS Infrastructure Documentation Generator CLI."""
    pass

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), required=True,
              help='Path to configuration file')
@click.option('--region', '-r', help='AWS region to scan')
def scan(config, region):
    """Scan AWS infrastructure and generate documentation."""
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        
        region = region or config_data['aws'].get('regions', ['us-east-1'])[0]
        
        scanner = AWSResourceScanner(region)
        diagram_gen = ArchitectureDiagramGenerator(config_data['output']['directory'])
        doc_gen = DocumentationGenerator(
            config_data['output']['directory'],
            config_data['templates']['directory']
        )
        
        resources = scanner.scan_resources(config_data['aws']['resources'])
        resources = convert_datetimes(resources)

        try:
            raw_output_path = os.path.join(config_data['output']['directory'], 'scan_results.json')
            with open(raw_output_path, 'w') as f:
                json.dump(resources, f, default=datetime_converter, indent=4)
        except KeyError as e:
            print(f"Missing key in config data: {e}")
        
        for fmt in config_data['output']['diagrams']:
            diagram_gen.generate_diagram(resources, f"architecture.{fmt}")
        
        doc_gen.generate_documentation(resources, config_data['output']['format'])
        
        if config_data.get('change_tracking', {}).get('enabled', False):
            tracker = ChangeTracker(
                storage_type=config_data['change_tracking']['storage'],
                **config_data['change_tracking']['config']
            )
            tracker.save_snapshot(resources)
        
        if config_data.get('compliance', {}).get('enabled', False):
            checker = ComplianceChecker(config_data['compliance']['rules_file'])
            results = checker.check_compliance(resources)
            
            report = checker.generate_report(
                results,
                format=config_data['compliance'].get('report_format', 'json')
            )
            
            report_path = os.path.join(
                config_data['output']['directory'],
                f"compliance_report.{config_data['compliance'].get('report_format', 'json')}"
            )
            with open(report_path, 'w') as f:
                f.write(report)
        
        logger.info("Documentation generation completed successfully")
        
    except Exception as e:
        logger.error(f"Error generating documentation: {e}")
        raise click.ClickException(str(e))

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), required=True,
              help='Path to configuration file')
@click.option('--start-time', '-s', required=True,
              help='Start time for change tracking (ISO format)')
@click.option('--end-time', '-e',
              help='End time for change tracking (ISO format)')
def track_changes(config, start_time, end_time):
    """Track infrastructure changes between two points in time."""
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if not config_data.get('change_tracking', {}).get('enabled', False):
            raise click.ClickException("Change tracking is not enabled in config")
        
        start_time_dt = datetime.fromisoformat(start_time)
        end_time_dt = datetime.fromisoformat(end_time) if end_time else None
        
        tracker = ChangeTracker(
            storage_type=config_data['change_tracking']['storage'],
            **config_data['change_tracking']['config']
        )
        
        changes = tracker.get_changes(start_time_dt, end_time_dt)
        changes = convert_datetimes(changes)
        
        report_path = os.path.join(
            config_data['output']['directory'],
            'changes_report.json'
        )
        with open(report_path, 'w') as f:
            json.dump(changes, f, default=datetime_converter, indent=4)
        
        logger.info(f"Changes report saved to {report_path}")
        
    except Exception as e:
        logger.error(f"Error tracking changes: {e}")
        raise click.ClickException(str(e))

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), required=True,
              help='Path to configuration file')
def check_compliance(config):
    """Check infrastructure compliance and generate report."""
    try:
        with open(config, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if not config_data.get('compliance', {}).get('enabled', False):
            raise click.ClickException("Compliance checking is not enabled in config")
        
        region = config_data['aws'].get('regions', ['us-east-1'])[0]
        scanner = AWSResourceScanner(region)
        resources = scanner.scan_resources(config_data['aws']['resources'])
        resources = convert_datetimes(resources)
        
        checker = ComplianceChecker(config_data['compliance']['rules_file'])
        results = checker.check_compliance(resources)
        
        report = checker.generate_report(
            results,
            format=config_data['compliance'].get('report_format', 'json')
        )
        
        report_path = os.path.join(
            config_data['output']['directory'],
            f"compliance_report.{config_data['compliance'].get('report_format', 'json')}"
        )
        with open(report_path, 'w') as f:
            f.write(report)
        
        logger.info(f"Compliance report saved to {report_path}")
        
    except Exception as e:
        logger.error(f"Error checking compliance: {e}")
        raise click.ClickException(str(e))

@cli.command()
@click.option('--input', '-i', type=click.Path(exists=True), required=True,
              help='Path to existing scan results JSON file')
@click.option('--output-dir', '-o', type=click.Path(), required=True,
              help='Directory to save the generated diagrams')
@click.option('--formats', '-f', multiple=True, default=['png'],
              help='Diagram formats to generate (e.g., png, svg, pdf)')
def create_diagrams(input, output_dir, formats):
    """Generate architecture diagrams from existing scan results."""
    try:
        with open(input, 'r') as f:
            resources = json.load(f)
        
        diagram_gen = ArchitectureDiagramGenerator(output_dir)
        
        for fmt in formats:
            diagram_name = f"architecture.{fmt}"
            diagram_gen.generate_diagram(resources, diagram_name)
            logger.info(f"Diagram generated: {os.path.join(output_dir, diagram_name)}")

        logger.info("All diagrams generated successfully.")

    except Exception as e:
        logger.error(f"Error generating diagrams: {e}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    cli()
