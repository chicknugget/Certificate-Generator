"""
Certificate Generator Core Module
Handles the main certificate generation logic using Pillow and ReportLab
"""

import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io
import datetime

class CertificateGenerator:
    def __init__(self, config):
        """Initialize certificate generator with configuration"""
        self.config = config
        self.template_path = config['certificate']['template_path']
        self.output_path = config['certificate']['output_path']
        self.width = config['certificate']['width']
        self.height = config['certificate']['height']
        self.background_color = config['certificate']['background_color']
        
        # Font configuration
        self.default_font_path = config['fonts']['default_font']
        self.title_font_size = config['fonts']['title_font_size']
        self.name_font_size = config['fonts']['name_font_size']
        self.details_font_size = config['fonts']['details_font_size']
        self.font_color = config['fonts']['font_color']
        
        # Positioning
        self.positions = config['positioning']
        
        # Output settings
        self.output_format = config['output']['format']
        self.quality = config['output']['quality']
        self.dpi = config['output']['dpi']
        
        # Load fonts
        self._load_fonts()
    
    def _load_fonts(self):
        """Load font files"""
        try:
            self.title_font = ImageFont.truetype(self.default_font_path, self.title_font_size)
            self.name_font = ImageFont.truetype(self.default_font_path, self.name_font_size)
            self.details_font = ImageFont.truetype(self.default_font_path, self.details_font_size)
        except OSError:
            print(f"Warning: Could not load font {self.default_font_path}, using default font")
            self.title_font = ImageFont.load_default()
            self.name_font = ImageFont.load_default()
            self.details_font = ImageFont.load_default()
    
    def create_template(self):
        """Create a basic certificate template if one doesn't exist"""
        if not os.path.exists(self.template_path):
            # Create template directory
            template_dir = os.path.dirname(self.template_path)
            os.makedirs(template_dir, exist_ok=True)
            
            # Create a basic template
            template = Image.new('RGB', (self.width, self.height), self.background_color)
            draw = ImageDraw.Draw(template)
            
            # Add decorative border
            border_width = 20
            draw.rectangle([border_width, border_width, 
                          self.width - border_width, self.height - border_width], 
                         outline="#2C3E50", width=5)
            
            # Add inner decorative border
            inner_border = 40
            draw.rectangle([inner_border, inner_border, 
                          self.width - inner_border, self.height - inner_border], 
                         outline="#3498DB", width=3)
            
            # Add corner decorations
            corner_size = 60
            corners = [(inner_border, inner_border), 
                      (self.width - inner_border - corner_size, inner_border),
                      (inner_border, self.height - inner_border - corner_size),
                      (self.width - inner_border - corner_size, self.height - inner_border - corner_size)]
            
            for corner in corners:
                draw.ellipse([corner[0], corner[1], corner[0] + corner_size, corner[1] + corner_size], 
                           outline="#E74C3C", width=3)
            
            template.save(self.template_path)
            print(f"✨ Created template at {self.template_path}")
    
    def generate_certificate(self, participant_data):
        """Generate certificate for a single participant"""
        # Ensure template exists
        self.create_template()
        
        # Load template
        template = Image.open(self.template_path)
        if template.mode != 'RGB':
            template = template.convert('RGB')
        
        # Create a copy for editing
        certificate = template.copy()
        draw = ImageDraw.Draw(certificate)
        
        # Extract participant information
        name = participant_data.get('name', 'Unknown')
        course = participant_data.get('course', 'Unknown Course')
        completion_date = participant_data.get('completion_date', datetime.datetime.now().strftime('%B %d, %Y'))
        
        # Add certificate title
        title_text = "Certificate of Completion"
        self._draw_centered_text(draw, title_text, self.positions['title_y'], 
                                self.title_font, self.font_color)
        
        # Add participant name
        self._draw_centered_text(draw, name, self.positions['name_y'], 
                                self.name_font, self.font_color)
        
        # Add course information
        course_text = f"has successfully completed the course: {course}"
        self._draw_centered_text(draw, course_text, self.positions['course_y'], 
                                self.details_font, self.font_color)
        
        # Add completion date
        date_text = f"Date of Completion: {completion_date}"
        self._draw_centered_text(draw, date_text, self.positions['date_y'], 
                                self.details_font, self.font_color)
        
        # Save certificate
        self._save_certificate(certificate, name)
    
    def _draw_centered_text(self, draw, text, y_position, font, color):
        """Draw text centered horizontally"""
        # Get text dimensions
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Calculate x position for centering
        x_position = (self.width - text_width) // 2
        
        # Draw text
        draw.text((x_position, y_position), text, font=font, fill=color)
    
    def _save_certificate(self, certificate, participant_name):
        """Save certificate in specified format(s)"""
        # Clean participant name for filename
        safe_name = "".join(c for c in participant_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        if self.output_format in ['png', 'both']:
            png_path = os.path.join(self.output_path, f"{safe_name}_certificate.png")
            certificate.save(png_path, 'PNG', quality=self.quality, dpi=(self.dpi, self.dpi))
        
        if self.output_format in ['pdf', 'both']:
            self._save_as_pdf(certificate, safe_name)
    
    def _save_as_pdf(self, certificate, participant_name):
        """Save certificate as PDF"""
        pdf_path = os.path.join(self.output_path, f"{participant_name}_certificate.pdf")
        
        # Convert PIL image to bytes
        img_buffer = io.BytesIO()
        certificate.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Create PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        
        # Calculate dimensions to fit letter size
        letter_width, letter_height = letter
        aspect_ratio = self.width / self.height
        
        if aspect_ratio > (letter_width / letter_height):
            # Image is wider, fit to width
            img_width = letter_width - 40  # 20pt margin on each side
            img_height = img_width / aspect_ratio
        else:
            # Image is taller, fit to height
            img_height = letter_height - 40  # 20pt margin on each side
            img_width = img_height * aspect_ratio
        
        # Center the image
        x = (letter_width - img_width) / 2
        y = (letter_height - img_height) / 2
        
        # Draw image
        c.drawImage(ImageReader(img_buffer), x, y, width=img_width, height=img_height)
        c.save()
