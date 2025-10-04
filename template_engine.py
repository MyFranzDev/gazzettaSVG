"""
Template Engine for Gazzetta SVG Banner Generator
Renders SVG banners based on JSON template configurations
"""

import json
import base64
import os
from typing import Dict, List, Any, Optional


class TemplateEngine:
    """Generic SVG rendering engine driven by JSON templates"""

    def __init__(self):
        self.fonts = {}
        self.content_data = {}
        self.background = {}

    def load_fonts(self):
        """Load and encode fonts as base64"""
        font_files = {
            "Oswald-Bold": ["Oswald-Bold.woff2", "Oswald-Bold.ttf"],
            "Oswald-BoldItalic": ["Oswald-BoldItalic.woff2", "Oswald-BoldItalic.ttf", "Oswald HeavyItalic 800.ttf"],
            "Roboto-Regular": ["Roboto-Regular.woff2", "Roboto-Regular.ttf"],
            "Roboto-Bold": ["Roboto-Bold.woff2", "Roboto-Bold.ttf"],
            "Roboto-BoldItalic": ["Roboto-BoldItalic.woff2", "Roboto-BoldItalic.ttf"]
        }

        for name, filenames in font_files.items():
            loaded = False
            for filename in filenames:
                try:
                    path = os.path.join("font", filename)
                    with open(path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                        # Determine format from extension
                        font_format = "woff2" if filename.endswith(".woff2") else "truetype"
                        self.fonts[name] = f"data:font/{font_format};base64,{b64}"
                        loaded = True
                        break
                except FileNotFoundError:
                    continue

            if not loaded:
                # Suppress font warnings to avoid polluting SVG output when called from frontend
                # print(f"⚠️ Font {name} not found (tried {', '.join(filenames)}), using system fallback", file=sys.stderr)
                self.fonts[name] = None

    def set_content_data(self, data: Dict[str, Any]):
        """Set content data (texts, images, background, etc.)"""
        self.content_data = data

    def set_background(self, bg_data: Dict[str, str]):
        """Set background data"""
        self.background = bg_data

    def render_template(self, template: Dict[str, Any]) -> str:
        """Render SVG from template configuration"""
        width = template["width"]
        height = template["height"]

        svg_parts = []
        svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')

        # Add font definitions
        svg_parts.append(self._generate_font_defs())

        # Render background if present
        if self.background.get("image"):
            svg_parts.append(self._render_background(width, height))

        # Render each component
        for component in template.get("components", []):
            svg_parts.append(self._render_component(component, width, height))

        # Add debug guides if enabled
        if template.get("debug_guides", False):
            svg_parts.append(self._render_debug_guides(template))

        svg_parts.append('</svg>')

        return '\n'.join(svg_parts)

    def _generate_font_defs(self) -> str:
        """Generate font face definitions"""
        defs = ['<defs>', '<style type="text/css">']

        for name, data_uri in self.fonts.items():
            if data_uri:
                font_family = name.replace("-", " ").replace("BoldItalic", "Bold").replace("Italic", "")
                weight = "bold" if "Bold" in name else "normal"
                style = "italic" if "Italic" in name else "normal"
                defs.append(f'''
                @font-face {{
                    font-family: '{font_family}';
                    font-weight: {weight};
                    font-style: {style};
                    src: url('{data_uri}') format('woff2');
                }}''')

        defs.append('</style>')
        defs.append('</defs>')

        return '\n'.join(defs)

    def _render_background(self, width: int, height: int) -> str:
        """Render background image"""
        if self.background.get("image"):
            return f'<image href="{self.background["image"]}" x="0" y="0" width="{width}" height="{height}" preserveAspectRatio="xMidYMid slice"/>'
        return ""

    def _render_component(self, comp: Dict[str, Any], canvas_width: int, canvas_height: int) -> str:
        """Render a single component based on its type"""
        comp_type = comp.get("type")

        if comp_type == "background_layer":
            return self._render_background_layer(comp, canvas_width, canvas_height)
        elif comp_type == "text_block":
            return self._render_text_block(comp, canvas_width, canvas_height)
        elif comp_type == "text_only":
            return self._render_text_only(comp, canvas_width, canvas_height)
        elif comp_type == "image":
            return self._render_image(comp, canvas_width, canvas_height)
        elif comp_type == "smartphone_mockup":
            return self._render_smartphone(comp, canvas_width, canvas_height)
        elif comp_type == "cta_button":
            return self._render_cta_button(comp, canvas_width, canvas_height)
        elif comp_type == "logo":
            return self._render_logo(comp, canvas_width, canvas_height)
        elif comp_type == "bullet_list":
            return self._render_bullet_list(comp, canvas_width, canvas_height)
        elif comp_type == "price_display":
            return self._render_price_display(comp, canvas_width, canvas_height)
        elif comp_type == "logo_text_group":
            return self._render_logo_text_group(comp, canvas_width, canvas_height)

        return ""

    def _parse_dimension(self, value: Any, reference: int) -> float:
        """Parse dimension value (%, px, or number)"""
        if isinstance(value, str):
            if value.endswith("%"):
                return float(value.rstrip("%")) / 100 * reference
            elif value.endswith("px"):
                return float(value.rstrip("px"))
        return float(value)

    def _get_geometry(self, comp: Dict, canvas_width: int, canvas_height: int) -> Dict[str, float]:
        """Calculate actual geometry from component definition"""
        geom = comp.get("geometry", {})

        return {
            "x": self._parse_dimension(geom.get("x", 0), canvas_width),
            "y": self._parse_dimension(geom.get("y", 0), canvas_height),
            "width": self._parse_dimension(geom.get("width", canvas_width), canvas_width),
            "height": self._parse_dimension(geom.get("height", canvas_height), canvas_height)
        }

    def _get_content(self, source: str) -> str:
        """Get content from content_data by source key"""
        return self.content_data.get(source, "")

    def _render_background_layer(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render a colored background layer or background image"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        parts = []

        # Check if this component should use the background image
        use_bg_image = style.get("use_background_image", False)

        if use_bg_image and self.background.get("image_data"):
            # Render background image clipped to this area
            clip_id = f"clip-{comp.get('id', 'bg')}"
            parts.append(f'<defs><clipPath id="{clip_id}"><rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}"/></clipPath></defs>')
            parts.append(f'<image href="data:image/png;base64,{self.background["image_data"]}" x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{clip_id})"/>')
        else:
            # Render solid color
            fill = style.get("background", self.background.get("color", "#223047"))
            opacity = style.get("opacity", 1)
            parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" fill="{fill}" opacity="{opacity}"/>')

        return '\n'.join(parts)

    def _render_text_block(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render text block with header and main text using HTML/CSS with auto-fit"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        # Get header and main content
        header_source = comp.get("header_source", "")
        content_source = comp.get("content_source", "")

        header_text = self._get_content(header_source) if header_source else ""
        main_text = self._get_content(content_source)

        if not header_text and not main_text:
            return ""

        # Text styling
        text_color = style.get("text_color", "#FFFFFF")
        alignment = style.get("alignment", "center")
        bg_color = style.get("background", None)

        header_font_family = style.get("header_font_family", "Roboto Bold")
        header_font_size = style.get("header_font_size", 24)
        main_font_family = style.get("font_family", "Oswald Bold")
        main_font_size = style.get("font_size", 48)

        # Quick estimate for scale factor
        line_height = 1.2
        estimated_height = 0
        if header_text:
            estimated_height += header_font_size * line_height
        if main_text:
            estimated_height += main_font_size * line_height
        if header_text and main_text:
            estimated_height += 10  # margin between

        scale_factor = min(1.0, (geom["height"] * 0.95) / estimated_height) if estimated_height > geom["height"] else 1.0

        # Convert alignment to CSS
        text_align_css = alignment if alignment in ['left', 'right', 'center'] else 'center'

        # Use foreignObject with HTML/CSS
        parts = []
        parts.append(f'<foreignObject x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}">')

        # Outer container for centering
        align_items_css = {'left': 'flex-start', 'right': 'flex-end', 'center': 'center'}.get(alignment, 'center')
        parts.append('<div xmlns="http://www.w3.org/1999/xhtml" style="')
        parts.append('width: 100%; height: 100%;')
        parts.append('display: flex; align-items: center;')
        parts.append(f'justify-content: {align_items_css};')
        if bg_color:
            parts.append(f'background: {bg_color};')
        parts.append('">')

        # Inner container with scale and column layout
        parts.append('<div style="')
        parts.append('display: flex; flex-direction: column;')
        parts.append(f'align-items: {align_items_css};')
        parts.append(f'transform: scale({scale_factor});')
        parts.append('transform-origin: center;')
        parts.append('">')

        # Header
        if header_text:
            parts.append(f'<div style="')
            parts.append(f'color: {text_color};')
            parts.append(f'font-family: \'{header_font_family}\';')
            parts.append(f'font-size: {header_font_size}px;')
            parts.append(f'text-align: {text_align_css};')
            parts.append('word-wrap: break-word;')
            parts.append(f'max-width: {geom["width"]}px;')
            parts.append('line-height: 1.2;')
            parts.append('">' + header_text + '</div>')

        # Main text
        if main_text:
            parts.append(f'<div style="')
            parts.append(f'color: {text_color};')
            parts.append(f'font-family: \'{main_font_family}\';')
            parts.append(f'font-size: {main_font_size}px;')
            parts.append(f'text-align: {text_align_css};')
            parts.append('word-wrap: break-word;')
            parts.append(f'max-width: {geom["width"]}px;')
            parts.append('line-height: 1.2;')
            if header_text:
                parts.append('margin-top: 10px;')
            parts.append('">' + main_text + '</div>')

        parts.append('</div>')  # Close inner
        parts.append('</div>')  # Close outer
        parts.append('</foreignObject>')

        return '\n'.join(parts)

    def _render_text_only(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render text with automatic word-wrap in fixed container"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        text_content = self._get_content(content_source)
        if not text_content:
            return ""

        text_color = style.get("text_color", "#FFFFFF")
        font_family = style.get("font_family", "Roboto")
        font_size = style.get("font_size", 24)
        alignment = style.get("alignment", "center")

        # Convert alignment to CSS
        text_align_css = alignment if alignment in ['left', 'right', 'center'] else 'center'

        # Use foreignObject with fixed dimensions
        parts = []
        parts.append(f'<foreignObject x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}">')

        # Single container with all styling - fixed size, overflow hidden
        parts.append(f'<div xmlns="http://www.w3.org/1999/xhtml" style="')
        parts.append(f'width: {geom["width"]}px;')
        parts.append(f'height: {geom["height"]}px;')
        parts.append('box-sizing: border-box;')
        parts.append('display: flex;')
        parts.append('align-items: center;')
        parts.append(f'justify-content: {text_align_css};')
        parts.append('overflow: hidden;')
        parts.append(f'color: {text_color};')
        parts.append(f'font-family: \'{font_family}\';')
        parts.append(f'font-size: {font_size}px;')
        parts.append(f'text-align: {text_align_css};')
        parts.append('word-wrap: break-word;')
        parts.append('line-height: 1.2;')
        parts.append(f'">{text_content}</div>')

        parts.append('</foreignObject>')

        return '\n'.join(parts)

    def _render_image(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render user image"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        image_data = self._get_content(content_source)
        if not image_data:
            return ""

        # Check if preserve_aspect is enabled (default to meet for logos)
        if style.get("preserve_aspect", False):
            preserve_aspect = "xMidYMid meet"
        else:
            fit = style.get("fit", "cover")
            preserve_aspect = "xMidYMid slice" if fit == "cover" else "xMidYMid meet"

        return f'<image href="{image_data}" x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" preserveAspectRatio="{preserve_aspect}"/>'

    def _render_smartphone(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render smartphone mockup with image inside"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        content_source = comp.get("content_source", "")
        style = comp.get("style", {})

        image_data = self._get_content(content_source)

        parts = []

        # Smartphone frame (rounded rect with border)
        phone_color = style.get("frame_color", "#1a1a1a")
        border_radius = style.get("border_radius", 30)

        parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" rx="{border_radius}" ry="{border_radius}" fill="{phone_color}"/>')

        # Screen area (slightly inset)
        screen_inset = 8
        screen_x = geom["x"] + screen_inset
        screen_y = geom["y"] + screen_inset
        screen_w = geom["width"] - screen_inset * 2
        screen_h = geom["height"] - screen_inset * 2
        screen_radius = border_radius - 5

        if image_data:
            parts.append(f'<clipPath id="screen-clip-{comp.get("id", "default")}"><rect x="{screen_x}" y="{screen_y}" width="{screen_w}" height="{screen_h}" rx="{screen_radius}" ry="{screen_radius}"/></clipPath>')
            parts.append(f'<image href="{image_data}" x="{screen_x}" y="{screen_y}" width="{screen_w}" height="{screen_h}" preserveAspectRatio="xMidYMid slice" clip-path="url(#screen-clip-{comp.get("id", "default")})"/>')
        else:
            parts.append(f'<rect x="{screen_x}" y="{screen_y}" width="{screen_w}" height="{screen_h}" rx="{screen_radius}" ry="{screen_radius}" fill="#000000"/>')

        # Optional label badge
        if style.get("show_label"):
            label_text = style.get("label_text", "SPECIALE US OPEN")
            badge_y = geom["y"] + geom["height"] - 60
            parts.append(f'<rect x="{geom["x"]}" y="{badge_y}" width="{geom["width"]}" height="25" fill="#E4087C"/>')
            parts.append(f'<text x="{geom["x"] + geom["width"]/2}" y="{badge_y + 17}" font-family="Roboto Bold" font-size="10" fill="#FFFFFF" text-anchor="middle">{label_text}</text>')

        # G+ logo badge
        if style.get("show_gplus_badge"):
            badge_y = geom["y"] + geom["height"] - 30
            parts.append(f'<rect x="{geom["x"]}" y="{badge_y}" width="{geom["width"]}" height="30" fill="#E4087C"/>')
            parts.append(f'<text x="{geom["x"] + 15}" y="{badge_y + 20}" font-family="Roboto Bold" font-size="18" fill="#FFFFFF">G+</text>')
            parts.append(f'<text x="{geom["x"] + 35}" y="{badge_y + 13}" font-family="Roboto Bold" font-size="7" fill="#FFFFFF">CONTENUTI</text>')
            parts.append(f'<text x="{geom["x"] + 35}" y="{badge_y + 22}" font-family="Roboto Bold" font-size="7" fill="#FFFFFF">PREMIUM</text>')

        return '\n'.join(parts)

    def _calculate_optimal_font_size(self, text: str, available_width: float, available_height: float,
                                       font_family: str, min_size: int = 10, max_size: int = 60,
                                       padding_ratio: float = 0.85) -> int:
        """Calculate optimal font size to fit text in available space

        Uses approximate character width calculation:
        - Roboto Bold: ~0.6 * font_size per character
        - Oswald Bold: ~0.55 * font_size per character (condensed)

        Args:
            padding_ratio: How much of available width to use (0.85 = 15% padding, 0.75 = 25% padding)
        """
        if not text:
            return max_size

        # Character width ratio based on font
        if "Oswald" in font_family:
            char_width_ratio = 0.55
        else:  # Roboto or other fonts
            char_width_ratio = 0.6

        # Calculate font size based on width constraint
        # Formula: text_width ≈ len(text) * font_size * char_width_ratio
        font_size_for_width = int((available_width * padding_ratio) / (len(text) * char_width_ratio))

        # Also consider height constraint (text should be ~80% of height)
        font_size_for_height = int(available_height * 0.8)

        # Use the smaller of the two, clamped to min/max
        optimal_size = min(font_size_for_width, font_size_for_height)
        return max(min_size, min(optimal_size, max_size))

    def _render_cta_button(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render CTA button with auto-fit using HTML/CSS"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        text_content = self._get_content(content_source)

        # Button styling
        bg_color = style.get("background", "#FFD700")
        border_radius = style.get("border_radius", 8)
        text_color = style.get("text_color", "#000000")
        font_family = style.get("font_family", "Roboto Bold")
        font_style = style.get("font_style", "normal")
        font_size = style.get("font_size", 20)

        # Calculate scale factor for auto-fit
        char_width_ratio = 0.6
        estimated_width = len(text_content) * font_size * char_width_ratio
        available_width = geom["width"] * 0.8  # 20% padding
        scale_factor = min(1.0, available_width / estimated_width) if estimated_width > 0 else 1.0

        font_style_css = 'italic' if font_style == 'italic' else 'normal'

        # Use foreignObject with HTML/CSS
        parts = []
        parts.append(f'<foreignObject x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}">')

        # Button div with border-radius and flexbox centering
        parts.append(f'<div xmlns="http://www.w3.org/1999/xhtml" style="')
        parts.append('width: 100%; height: 100%;')
        parts.append(f'background: {bg_color};')
        parts.append(f'border-radius: {border_radius}px;')
        parts.append('display: flex; align-items: center; justify-content: center;')
        parts.append('">')

        # Text with scale
        parts.append(f'<span style="')
        parts.append(f'color: {text_color};')
        parts.append(f'font-family: \'{font_family}\';')
        parts.append(f'font-style: {font_style_css};')
        parts.append(f'font-size: {font_size}px;')
        parts.append(f'transform: scale({scale_factor});')
        parts.append('white-space: nowrap;')
        parts.append('">' + text_content + '</span>')

        parts.append('</div>')
        parts.append('</foreignObject>')

        return '\n'.join(parts)

    def _render_logo(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render logo (user uploaded or default G+) with optional color overlay"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        parts = []

        # Check if user provided a logo image
        logo_image = self._get_content(content_source) if content_source else None
        logo_color = style.get("logo_color", None)

        if logo_image:
            # User uploaded logo - use foreignObject for CSS filter support
            bg_color = style.get("background", "#FFFFFF")
            padding = style.get("padding", 10)

            parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" fill="{bg_color}"/>')
            parts.append(f'<foreignObject x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}">')

            parts.append('<div xmlns="http://www.w3.org/1999/xhtml" style="')
            parts.append('width: 100%; height: 100%;')
            parts.append('display: flex; justify-content: center; align-items: center;')
            parts.append(f'padding: {padding}px;')
            parts.append('box-sizing: border-box;')
            parts.append('">')

            # Apply CSS filter for color overlay if logo_color is specified
            logo_filter = ''
            if logo_color:
                logo_filter = 'filter: brightness(0) saturate(100%) invert(48%) sepia(79%) saturate(2476%) hue-rotate(316deg) brightness(98%) contrast(119%);'

            parts.append(f'<img src="{logo_image}" style="max-width: 100%; max-height: 100%; {logo_filter}" />')
            parts.append('</div>')
            parts.append('</foreignObject>')
        else:
            # Default G+ logo (fallback)
            bg_color = style.get("background", "#E4087C")
            parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" fill="{bg_color}"/>')

            # G+ text
            font_size = style.get("font_size", 24)
            text_x = geom["x"] + geom["width"] / 2
            text_y = geom["y"] + geom["height"] / 2 + font_size / 3

            parts.append(f'<text x="{text_x}" y="{text_y}" font-family="Roboto Bold" font-size="{font_size}" fill="#FFFFFF" text-anchor="middle">G+</text>')

            # Optional subtitle
            if style.get("show_subtitle"):
                subtitle_size = font_size * 0.3
                parts.append(f'<text x="{text_x}" y="{text_y + subtitle_size + 2}" font-family="Roboto Bold" font-size="{subtitle_size}" fill="#FFFFFF" text-anchor="middle">CONTENUTI</text>')
                parts.append(f'<text x="{text_x}" y="{text_y + subtitle_size * 2 + 4}" font-family="Roboto Bold" font-size="{subtitle_size}" fill="#FFFFFF" text-anchor="middle">PREMIUM</text>')

        return '\n'.join(parts)

    def _render_price_display(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render price with auto-fit using HTML/CSS flexbox

        Layout:
        [14]  [,99€]
              [/ANNO]
        """
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        # Get price and period from content sources
        price_source = comp.get("price_source", "")
        period_source = comp.get("period_source", "")

        price_text = self._get_content(price_source) if price_source else ""
        period_text = self._get_content(period_source) if period_source else ""

        if not price_text:
            return ""

        text_color = style.get("text_color", "#FFFFFF")
        font_family = style.get("font_family", "Oswald Bold")
        font_style = style.get("font_style", "normal")
        alignment = style.get("alignment", "center")

        # Split price into integer and decimal parts
        import re
        match = re.match(r'^(\d+)([.,]\d+)?(.*)$', price_text.strip())

        if match:
            integer_part = match.group(1)  # "14"
            decimal_part = (match.group(2) or "") + (match.group(3) or "")  # ",99€"
        else:
            integer_part = price_text
            decimal_part = ""

        # Font sizes
        large_size = int(geom["height"] * 0.75)
        small_size = int(geom["height"] * 0.35)
        period_size = int(geom["height"] * 0.25)

        # Calculate scale factor for auto-fit
        char_width_ratio = 0.55 if "Oswald" in font_family else 0.6
        estimated_width = len(integer_part) * large_size * char_width_ratio + len(decimal_part) * small_size * char_width_ratio
        available_width = geom["width"] * 0.95
        scale_factor = min(1.0, available_width / estimated_width) if estimated_width > 0 else 1.0

        # Convert alignment to CSS
        justify_content = {'left': 'flex-start', 'right': 'flex-end', 'center': 'center'}.get(alignment, 'center')
        font_style_css = 'italic' if font_style == 'italic' else 'normal'

        # Use foreignObject with HTML/CSS
        parts = []
        parts.append(f'<foreignObject x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}">')

        # Outer container for centering
        parts.append('<div xmlns="http://www.w3.org/1999/xhtml" style="')
        parts.append('width: 100%; height: 100%; display: flex;')
        parts.append('align-items: center;')
        parts.append(f'justify-content: {justify_content};')
        parts.append('">')

        # Inner container with scale
        # Gap proportional to font size (16% of large size)
        gap = int(large_size * 0.16)
        parts.append('<div style="')
        parts.append(f'display: flex; gap: {gap}px;')
        parts.append(f'transform: scale({scale_factor}); transform-origin: center;')
        parts.append('">')

        # Integer part (left side, large)
        parts.append(f'<div style="color: {text_color}; font-family: \'{font_family}\'; font-style: {font_style_css}; font-size: {large_size}px; line-height: 1;">{integer_part}</div>')

        # Decimal + period column (right side)
        if decimal_part or period_text:
            # Calculate offset to align decimal top with integer top (approximately 10% of large size)
            offset = int(large_size * 0.10)
            parts.append(f'<div style="display: flex; flex-direction: column; align-items: flex-start; margin-top: {offset}px;">')
            if decimal_part:
                parts.append(f'<div style="color: {text_color}; font-family: \'{font_family}\'; font-style: {font_style_css}; font-size: {small_size}px; line-height: 1;">{decimal_part}</div>')
            if period_text:
                parts.append(f'<div style="color: {text_color}; font-family: \'{font_family}\'; font-style: {font_style_css}; font-size: {period_size}px; line-height: 1; margin-top: 2px;">{period_text}</div>')
            parts.append('</div>')

        parts.append('</div>')  # Close inner container
        parts.append('</div>')  # Close outer container
        parts.append('</foreignObject>')

        return '\n'.join(parts)

    def _render_bullet_list(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render bullet point list with HTML/CSS for word-wrap"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        items = comp.get("items", [])

        if not items:
            return ""

        text_color = style.get("text_color", "#FFFFFF")
        font_size = style.get("font_size", 16)
        font_family = style.get("font_family", "Roboto")

        # Use foreignObject with HTML/CSS
        parts = []
        parts.append(f'<foreignObject x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}">')

        # Container div
        parts.append('<div xmlns="http://www.w3.org/1999/xhtml" style="')
        parts.append('width: 100%; height: 100%;')
        parts.append('display: flex; flex-direction: column;')
        parts.append('justify-content: center;')
        parts.append(f'color: {text_color};')
        parts.append(f'font-family: \'{font_family}\';')
        parts.append(f'font-size: {font_size}px;')
        parts.append('gap: 8px;')
        parts.append('">')

        # Render each item
        for item_source in items:
            item_text = self._get_content(item_source)
            if not item_text:
                continue

            parts.append('<div style="display: flex; gap: 8px; align-items: flex-start;">')
            parts.append('<span style="flex-shrink: 0;">✓</span>')
            parts.append(f'<span style="word-wrap: break-word; overflow-wrap: break-word;">{item_text}</span>')
            parts.append('</div>')

        parts.append('</div>')
        parts.append('</foreignObject>')

        return '\n'.join(parts)

    def _render_logo_text_group(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render logo + text centered horizontally as a group using HTML foreignObject"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        # Get content sources
        logo_source = comp.get("logo_source", "")
        text_source = comp.get("text_source", "")

        logo_image = self._get_content(logo_source) if logo_source else None
        text_content = self._get_content(text_source)

        if not text_content:
            return ""

        # Logo dimensions
        logo_size = style.get("logo_size", 100)
        gap = style.get("gap", 10)

        # Text styling
        text_color = style.get("text_color", "#FFFFFF")
        font_family = style.get("font_family", "Oswald Bold")
        font_style = style.get("font_style", "normal")
        font_size = style.get("font_size", 48)
        logo_color = style.get("logo_color", None)

        # Calculate approximate width needed for the content
        char_width_ratio = 0.55 if "Oswald" in font_family else 0.6
        if font_style == 'italic':
            char_width_ratio *= 0.95
        estimated_text_width = len(text_content) * font_size * char_width_ratio
        total_estimated_width = (logo_size if logo_image else 0) + gap + estimated_text_width

        # Calculate scale factor needed to fit content in available width
        available_width = geom["width"] * 0.95  # 95% to leave some margin
        scale_factor = min(1.0, available_width / total_estimated_width) if total_estimated_width > 0 else 1.0

        # Use foreignObject with transform scale for the entire group
        parts = []
        parts.append(f'<foreignObject x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}">')

        # Outer container for centering
        parts.append('<div xmlns="http://www.w3.org/1999/xhtml" style="')
        parts.append('width: 100%;')
        parts.append('height: 100%;')
        parts.append('display: flex;')
        parts.append('justify-content: center;')
        parts.append('align-items: center;')
        parts.append('">')

        # Inner content container with transform scale applied
        parts.append('<div style="')
        parts.append('display: flex;')
        parts.append('align-items: center;')
        parts.append('gap: ' + str(gap) + 'px;')
        parts.append(f'transform: scale({scale_factor});')
        parts.append('transform-origin: center center;')
        parts.append('">')

        # Logo
        if logo_image:
            logo_filter = f'filter: hue-rotate(0deg) saturate(0%) brightness(0) invert(1);' if logo_color else ''
            if logo_color:
                # Convert hex to RGB for CSS filter
                r = int(logo_color[1:3], 16)
                g = int(logo_color[3:5], 16)
                b = int(logo_color[5:7], 16)
                logo_filter = f'filter: brightness(0) saturate(100%) invert(48%) sepia(79%) saturate(2476%) hue-rotate(316deg) brightness(98%) contrast(119%);'

            parts.append(f'<img src="{logo_image}" style="height: {logo_size}px; width: auto; {logo_filter}" />')

        # Text
        font_style_css = 'italic' if font_style == 'italic' else 'normal'
        parts.append(f'<span style="')
        parts.append(f'color: {text_color};')
        parts.append(f'font-family: \'{font_family}\';')
        parts.append(f'font-style: {font_style_css};')
        parts.append(f'font-size: {font_size}px;')
        parts.append('white-space: nowrap;')
        parts.append('">' + text_content + '</span>')

        parts.append('</div>')  # Close inner content
        parts.append('</div>')  # Close outer container
        parts.append('</foreignObject>')

        return '\n'.join(parts)
    def _render_debug_guides(self, template: Dict) -> str:
        """Render debug guides for alignment verification"""
        parts = []

        # Guide for left column boundary (x=471, right edge of left column content area)
        parts.append(f'<rect x="459" y="0" width="12" height="{template["height"]}" fill="rgba(255,0,0,0.3)"/>')
        parts.append(f'<text x="465" y="20" font-size="10" fill="red">padding 12px</text>')

        # Guide for right column boundary (x=1460, left edge of right column)
        parts.append(f'<rect x="1448" y="0" width="12" height="{template["height"]}" fill="rgba(0,255,0,0.3)"/>')
        parts.append(f'<text x="1450" y="20" font-size="10" fill="green">padding 12px</text>')

        return '\n'.join(parts)


def load_template(template_path: str) -> Dict[str, Any]:
    """Load template from JSON file"""
    with open(template_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_svg(svg_content: str, output_path: str):
    """Save SVG content to file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"✅ Generated: {output_path}")
