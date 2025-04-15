import json
from datetime import datetime
import os
import markdown
from jinja2 import Environment, FileSystemLoader
import logging
from typing import Dict, List, Any

# Logger setup
logger = logging.getLogger(__name__)

# Custom datetime converter function
def datetime_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()  # Convert datetime to ISO format string
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

class DocumentationGenerator:
    """Generates documentation from AWS resource data."""
    
    def __init__(self, output_dir: str, template_dir: str):
        """Initialize the documentation generator.
        
        Args:
            output_dir: Directory to save generated documentation
            template_dir: Directory containing documentation templates
        """
        self.output_dir = output_dir
        self.template_dir = template_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate_documentation(self, resources: Dict[str, List[Dict[str, Any]]], formats: List[str]):
        """Generate documentation in specified formats.
        
        Args:
            resources: Dictionary of AWS resources by type
            formats: List of output formats ('html', 'markdown', 'pdf')
        """
        # Generate base markdown
        markdown_content = self._generate_markdown(resources)
        
        # Save in requested formats
        for fmt in formats:
            if fmt == 'markdown':
                self._save_markdown(markdown_content)
            elif fmt == 'html':
                self._save_html(markdown_content)
            elif fmt == 'pdf':
                self._save_pdf(markdown_content)
            else:
                logger.warning(f"Unsupported format: {fmt}")
    
    def _generate_markdown(self, resources: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate markdown documentation from resource data."""
        template = self.jinja_env.get_template('resources.md.j2')
        
        # Serialize datetime properly using the custom converter
        generation_time = datetime.now()
        
        return template.render(
            resources=resources,
            generation_time=datetime_converter(generation_time),  # Use datetime_converter to format the datetime
            resource_counts={ 
                resource_type: len(resource_list) 
                for resource_type, resource_list in resources.items()
            }
        )
    
    def _save_markdown(self, content: str):
        """Save documentation in markdown format."""
        output_path = os.path.join(self.output_dir, 'documentation.md')
        with open(output_path, 'w') as f:
            f.write(content)
    
    def _save_html(self, markdown_content: str):
        """Convert markdown to HTML and save."""
        html_content = markdown.markdown(
            markdown_content,
            extensions=['tables', 'fenced_code', 'toc']
        )
        
        template = self.jinja_env.get_template('base.html.j2')
        final_html = template.render(content=html_content)
        
        output_path = os.path.join(self.output_dir, 'documentation.html')
        with open(output_path, 'w') as f:
            f.write(final_html)
    
    def _save_pdf(self, markdown_content: str):
        """Convert markdown to PDF and save."""
        try:
            from weasyprint import HTML, CSS
            
            # First convert to HTML
            html_content = markdown.markdown(
                markdown_content,
                extensions=['tables', 'fenced_code', 'toc']
            )
            
            template = self.jinja_env.get_template('base.html.j2')
            final_html = template.render(content=html_content)
            
            # Convert HTML to PDF
            output_path = os.path.join(self.output_dir, 'documentation.pdf')
            HTML(string=final_html).write_pdf(
                output_path,
                stylesheets=[CSS(string='body { font-family: Arial, sans-serif; }')]
            )
        except ImportError:
            logger.error("WeasyPrint is required for PDF generation. Please install it first.")
    
    def generate_resource_details(self, resource_type: str, resource: Dict[str, Any]) -> str:
        """Generate detailed documentation for a specific resource."""
        template_name = f"{resource_type}_details.md.j2"
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(resource=resource)
        except Exception as e:
            logger.error(f"Error generating details for {resource_type}: {e}")
            return json.dumps(resource, default=datetime_converter, indent=2)  # Ensure datetime is serialized correctly
