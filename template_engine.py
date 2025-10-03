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
            "Oswald-Bold": "Oswald-Bold.woff2",
            "Roboto-Regular": "Roboto-Regular.woff2",
            "Roboto-Bold": "Roboto-Bold.woff2"
        }

        for name, filename in font_files.items():
            try:
                path = os.path.join("font", filename)
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode("utf-8")
                    self.fonts[name] = f"data:font/woff2;base64,{b64}"
            except FileNotFoundError:
                print(f"⚠️ Font {filename} not found, using system fallback")
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

        svg_parts.append('</svg>')

        return '\n'.join(svg_parts)

    def _generate_font_defs(self) -> str:
        """Generate font face definitions"""
        defs = ['<defs>', '<style type="text/css">']

        for name, data_uri in self.fonts.items():
            if data_uri:
                font_family = name.replace("-", " ")
                weight = "bold" if "Bold" in name else "normal"
                defs.append(f'''
                @font-face {{
                    font-family: '{font_family}';
                    font-weight: {weight};
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
        """Render a colored background layer"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        fill = style.get("background", "#223047")
        opacity = style.get("opacity", 1)

        return f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" fill="{fill}" opacity="{opacity}"/>'

    def _render_text_block(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render text block with background"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        text_content = self._get_content(content_source)

        parts = []

        # Background
        bg_color = style.get("background", self.background.get("main_color", "#223047"))
        parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" fill="{bg_color}"/>')

        # Text
        text_color = style.get("text_color", "#FFFFFF")
        font_size = style.get("font_size", 20)
        font_family = style.get("font_family", "Oswald Bold")
        alignment = style.get("alignment", "center")

        # Calculate text position
        text_x = geom["x"] + geom["width"] / 2 if alignment == "center" else geom["x"] + 10
        text_y = geom["y"] + geom["height"] / 2 + font_size / 3
        text_anchor = "middle" if alignment == "center" else "start"

        parts.append(f'<text x="{text_x}" y="{text_y}" font-family="{font_family}" font-size="{font_size}" fill="{text_color}" text-anchor="{text_anchor}">{text_content}</text>')

        return '\n'.join(parts)

    def _render_text_only(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render text without background"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        text_content = self._get_content(content_source)
        if not text_content:
            return ""

        text_color = style.get("text_color", "#FFFFFF")
        font_size = style.get("font_size", 24)
        font_family = style.get("font_family", "Oswald Bold")
        alignment = style.get("alignment", "center")

        # Handle multiline text
        lines = text_content.split('\n')

        parts = []
        for i, line in enumerate(lines):
            text_x = geom["x"] + geom["width"] / 2 if alignment == "center" else geom["x"]
            text_y = geom["y"] + (i + 1) * font_size * 1.2
            text_anchor = "middle" if alignment == "center" else "start"

            parts.append(f'<text x="{text_x}" y="{text_y}" font-family="{font_family}" font-size="{font_size}" fill="{text_color}" text-anchor="{text_anchor}">{line}</text>')

        return '\n'.join(parts)

    def _render_image(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render user image"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        content_source = comp.get("content_source", "")

        image_data = self._get_content(content_source)
        if not image_data:
            return ""

        fit = comp.get("style", {}).get("fit", "cover")
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

    def _render_cta_button(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render CTA button"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        text_content = self._get_content(content_source)

        parts = []

        # Button background
        bg_color = style.get("background", "#FFD700")
        border_radius = style.get("border_radius", 25)

        parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" rx="{border_radius}" ry="{border_radius}" fill="{bg_color}"/>')

        # Button text
        text_color = style.get("text_color", "#000000")
        font_size = style.get("font_size", 18)
        font_family = style.get("font_family", "Roboto Bold")

        text_x = geom["x"] + geom["width"] / 2
        text_y = geom["y"] + geom["height"] / 2 + font_size / 3

        parts.append(f'<text x="{text_x}" y="{text_y}" font-family="{font_family}" font-size="{font_size}" fill="{text_color}" text-anchor="middle">{text_content}</text>')

        return '\n'.join(parts)

    def _render_logo(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render G+ logo"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        parts = []

        # Logo background
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

    def _render_bullet_list(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render bullet point list"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        items = comp.get("items", [])

        parts = []

        text_color = style.get("text_color", "#FFFFFF")
        font_size = style.get("font_size", 16)
        font_family = style.get("font_family", "Roboto Regular")
        line_spacing = style.get("line_spacing", font_size * 1.5)

        for i, item_source in enumerate(items):
            item_text = self._get_content(item_source)
            if not item_text:
                continue

            y_pos = geom["y"] + i * line_spacing + font_size

            # Checkmark bullet
            parts.append(f'<text x="{geom["x"]}" y="{y_pos}" font-family="{font_family}" font-size="{font_size}" fill="{text_color}">✓</text>')

            # Item text
            parts.append(f'<text x="{geom["x"] + font_size + 5}" y="{y_pos}" font-family="{font_family}" font-size="{font_size}" fill="{text_color}">{item_text}</text>')

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
