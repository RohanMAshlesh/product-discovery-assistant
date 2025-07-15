from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime
import io

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        # Add custom styles for different sections
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#0066CC')
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.HexColor('#1E1E1E')
        ))

    def _format_text_report(self, product_idea: str, analysis_results: dict) -> str:
        """Generate a formatted text report."""
        report = []
        
        # Add header
        report.append("=" * 80)
        report.append("PRODUCT DISCOVERY STRATEGY REPORT")
        report.append("=" * 80)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("\n")
        
        # Add product idea
        report.append("PRODUCT IDEA")
        report.append("-" * 80)
        report.append(product_idea)
        report.append("\n")
        
        # Add each framework analysis
        frameworks = {
            'jtbd': 'JOBS TO BE DONE ANALYSIS',
            'value_proposition': 'VALUE PROPOSITION CANVAS',
            'opportunity_solution': 'OPPORTUNITY SOLUTION TREE',
            'four_fit': '4-FIT MODEL ASSESSMENT'
        }
        
        for key, title in frameworks.items():
            report.append(title)
            report.append("-" * 80)
            report.append(analysis_results[key]['analysis'])
            report.append("\n")
        
        return "\n".join(report)

    def _format_pdf_report(self, product_idea: str, analysis_results: dict) -> bytes:
        """Generate a PDF report."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the PDF content
        story = []
        
        # Add title
        story.append(Paragraph("Product Discovery Strategy Report", self.styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                             self.styles['Normal']))
        story.append(Spacer(1, 24))
        
        # Add product idea
        story.append(Paragraph("Product Idea", self.styles['SectionHeader']))
        story.append(Paragraph(product_idea, self.styles['Normal']))
        story.append(Spacer(1, 24))
        
        # Add each framework analysis
        frameworks = {
            'jtbd': 'Jobs to Be Done Analysis',
            'value_proposition': 'Value Proposition Canvas',
            'opportunity_solution': 'Opportunity Solution Tree',
            'four_fit': '4-Fit Model Assessment'
        }
        
        for key, title in frameworks.items():
            story.append(Paragraph(title, self.styles['SectionHeader']))
            story.append(Paragraph(analysis_results[key]['analysis'], self.styles['Normal']))
            story.append(Spacer(1, 24))
        
        # Build the PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

    def generate_report(self, product_idea: str, analysis_results: dict, format: str = 'txt') -> tuple:
        """
        Generate a report in the specified format.
        Returns a tuple of (file_data, mime_type, file_extension)
        """
        if format.lower() == 'pdf':
            return (
                self._format_pdf_report(product_idea, analysis_results),
                'application/pdf',
                'pdf'
            )
        else:
            return (
                self._format_text_report(product_idea, analysis_results).encode('utf-8'),
                'text/plain',
                'txt'
            ) 