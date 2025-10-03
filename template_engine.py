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
                print(f"⚠️ Font {name} not found (tried {', '.join(filenames)}), using system fallback")
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
        """Render text block with optional header and main text (both auto-sized to fill space)"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        # Get header and main content
        header_source = comp.get("header_source", "")
        content_source = comp.get("content_source", "")

        header_text = self._get_content(header_source) if header_source else ""
        main_text = self._get_content(content_source)

        parts = []

        # Optional background
        if style.get("background"):
            bg_color = style.get("background")
            parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" fill="{bg_color}"/>')

        # Text styling
        text_color = style.get("text_color", "#FFFFFF")
        alignment = style.get("alignment", "center")
        text_anchor = "middle" if alignment == "center" else "start"

        # Calculate available space
        total_height = geom["height"]
        total_width = geom["width"]

        # If we have both header and main text, split space between them
        if header_text and main_text:
            # Allocate space: 40% for header, 60% for main text
            header_height_alloc = total_height * 0.40
            main_height_alloc = total_height * 0.60

            # Auto-size both texts to fill their allocated space
            header_font_family = style.get("header_font_family", "Roboto Bold")
            main_font_family = style.get("font_family", "Oswald Bold")

            header_font_size = self._calculate_optimal_font_size(
                header_text,
                total_width,
                header_height_alloc,
                header_font_family,
                min_size=10,
                max_size=style.get("max_header_font_size", 30),
                padding_ratio=0.90
            )

            main_font_size = self._calculate_optimal_font_size(
                main_text,
                total_width,
                main_height_alloc,
                main_font_family,
                min_size=style.get("min_font_size", 18),
                max_size=style.get("max_font_size", 60),
                padding_ratio=0.90
            )

            # Calculate total actual content height with some spacing
            spacing = 3
            total_content_height = header_font_size + spacing + main_font_size

            # Center the entire block vertically
            start_y = geom["y"] + (total_height - total_content_height) / 2

            # Position texts
            header_y = start_y + header_font_size * 0.85
            main_y = start_y + header_font_size + spacing + main_font_size * 0.85

        elif header_text:
            # Only header, use full space
            header_font_family = style.get("header_font_family", "Roboto Bold")
            header_font_size = self._calculate_optimal_font_size(
                header_text,
                total_width,
                total_height,
                header_font_family,
                min_size=10,
                max_size=style.get("max_header_font_size", 30),
                padding_ratio=0.90
            )
            header_y = geom["y"] + geom["height"] / 2 + header_font_size / 3
            main_font_size = 0

        elif main_text:
            # Only main text, use full space
            main_font_family = style.get("font_family", "Oswald Bold")
            main_font_size = self._calculate_optimal_font_size(
                main_text,
                total_width,
                total_height,
                main_font_family,
                min_size=style.get("min_font_size", 18),
                max_size=style.get("max_font_size", 60),
                padding_ratio=0.90
            )
            main_y = geom["y"] + geom["height"] / 2 + main_font_size / 3
            header_font_size = 0

        else:
            header_font_size = 0
            main_font_size = 0

        # Render header
        if header_text:
            header_font_family = style.get("header_font_family", "Roboto Bold")
            header_x = geom["x"] + geom["width"] / 2 if alignment == "center" else geom["x"]

            parts.append(f'<text x="{header_x}" y="{header_y}" font-family="{header_font_family}" font-size="{header_font_size}" fill="{text_color}" text-anchor="{text_anchor}">{header_text}</text>')

        # Main text
        if main_text:
            main_font_family = style.get("font_family", "Oswald Bold")
            main_x = geom["x"] + geom["width"] / 2 if alignment == "center" else geom["x"]

            parts.append(f'<text x="{main_x}" y="{main_y}" font-family="{main_font_family}" font-size="{main_font_size}" fill="{text_color}" text-anchor="{text_anchor}">{main_text}</text>')

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
        font_family = style.get("font_family", "Oswald Bold")
        alignment = style.get("alignment", "center")

        # Auto-size text if enabled
        if style.get("auto_size", False):
            font_size = self._calculate_optimal_font_size(
                text_content.replace('\n', ' '),  # Treat as single line for sizing
                geom["width"],
                geom["height"],
                font_family,
                min_size=style.get("min_font_size", 10),
                max_size=style.get("max_font_size", 60)
            )
        else:
            font_size = style.get("font_size", 24)

        # Handle multiline text
        lines = text_content.split('\n')

        # Calculate total height of multiline text
        line_height = font_size * 1.2
        total_height = len(lines) * line_height

        # Calculate starting Y to center the text block vertically
        start_y = geom["y"] + (geom["height"] - total_height) / 2 + font_size

        parts = []
        for i, line in enumerate(lines):
            if alignment == "center":
                text_x = geom["x"] + geom["width"] / 2
                text_anchor = "middle"
            elif alignment == "right":
                text_x = geom["x"] + geom["width"]
                text_anchor = "end"
            else:  # left
                text_x = geom["x"]
                text_anchor = "start"

            text_y = start_y + i * line_height

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

        # Button text with auto-sizing
        text_color = style.get("text_color", "#000000")
        font_family = style.get("font_family", "Roboto Bold")
        font_style = style.get("font_style", "normal")  # normal or italic

        # Get base font size or calculate optimal
        if style.get("auto_size", True):
            font_size = self._calculate_optimal_font_size(
                text_content,
                geom["width"],
                geom["height"],
                font_family,
                min_size=style.get("min_font_size", 10),
                max_size=style.get("max_font_size", 60),
                padding_ratio=0.75  # 25% padding for buttons
            )
        else:
            font_size = style.get("font_size", 18)

        text_x = geom["x"] + geom["width"] / 2
        text_y = geom["y"] + geom["height"] / 2 + font_size / 3

        parts.append(f'<text x="{text_x}" y="{text_y}" font-family="{font_family}" font-size="{font_size}" font-style="{font_style}" fill="{text_color}" text-anchor="middle">{text_content}</text>')

        return '\n'.join(parts)

    def _render_logo(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render logo (user uploaded or default G+)"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})
        content_source = comp.get("content_source", "")

        parts = []

        # Check if user provided a logo image
        logo_image = self._get_content(content_source) if content_source else None

        if logo_image:
            # User uploaded logo
            bg_color = style.get("background", "#FFFFFF")

            # Background
            parts.append(f'<rect x="{geom["x"]}" y="{geom["y"]}" width="{geom["width"]}" height="{geom["height"]}" fill="{bg_color}"/>')

            # Logo image (centered, with padding)
            padding = style.get("padding", 10)
            img_x = geom["x"] + padding
            img_y = geom["y"] + padding
            img_w = geom["width"] - padding * 2
            img_h = geom["height"] - padding * 2

            parts.append(f'<image href="{logo_image}" x="{img_x}" y="{img_y}" width="{img_w}" height="{img_h}" preserveAspectRatio="xMidYMid meet"/>')
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
        """Render price with large integer, small decimal/currency, and period below

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

        parts = []

        text_color = style.get("text_color", "#FFFFFF")
        font_family = style.get("font_family", "Oswald Bold")
        alignment = style.get("alignment", "center")

        # Split price into integer and decimal parts
        # Expected format: "14,99€" or "14.99€" or just "14€"
        import re
        match = re.match(r'^(\d+)([.,]\d+)?(.*)$', price_text.strip())

        if match:
            integer_part = match.group(1)  # "14"
            decimal_part = (match.group(2) or "") + (match.group(3) or "")  # ",99€"
        else:
            # Fallback: use entire price as integer
            integer_part = price_text
            decimal_part = ""

        # Font sizes
        large_size = int(geom["height"] * 0.75)  # Integer takes ~75% of height
        small_size = int(geom["height"] * 0.35)  # Decimal/period takes ~35% of height
        period_size = int(geom["height"] * 0.25)  # Period even smaller ~25% of height

        # Calculate anchor point based on alignment
        if alignment == "center":
            anchor_x = geom["x"] + geom["width"] / 2
        elif alignment == "right":
            anchor_x = geom["x"] + geom["width"]
        else:  # left
            anchor_x = geom["x"]

        # Vertical centering calculation
        content_height = large_size
        if period_text:
            content_height += period_size * 1.0

        start_y = geom["y"] + (geom["height"] - content_height) / 2

        # Get font style from component style
        font_style = style.get("font_style", "normal")

        # Spacing between integer and decimal parts
        spacing = 5  # pixels

        if alignment == "right":
            # For right alignment, we align the rightmost element (decimal or period) to anchor
            int_y = start_y + large_size

            # Calculate approximate widths for positioning
            char_width_large = large_size * 0.6
            char_width_small = small_size * 0.6
            char_width_period = period_size * 0.6

            if decimal_part and period_text:
                # Has both decimal and period - period is rightmost
                period_x = anchor_x
                period_y = int_y
                period_width = len(period_text) * char_width_period
                parts.append(f'<text x="{period_x}" y="{period_y}" font-family="{font_family}" font-size="{period_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{period_text}</text>')

                # Decimal goes above period, also right-aligned
                dec_x = anchor_x
                dec_y = start_y + small_size * 1.2
                parts.append(f'<text x="{dec_x}" y="{dec_y}" font-family="{font_family}" font-size="{small_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{decimal_part}</text>')

                # Integer left of decimal, right-aligned
                decimal_width = len(decimal_part) * char_width_small
                int_x = dec_x - decimal_width - spacing
                parts.append(f'<text x="{int_x}" y="{int_y}" font-family="{font_family}" font-size="{large_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{integer_part}</text>')

            elif decimal_part:
                # Only decimal, no period
                dec_x = anchor_x
                dec_y = start_y + small_size * 1.2
                parts.append(f'<text x="{dec_x}" y="{dec_y}" font-family="{font_family}" font-size="{small_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{decimal_part}</text>')

                decimal_width = len(decimal_part) * char_width_small
                int_x = dec_x - decimal_width - spacing
                parts.append(f'<text x="{int_x}" y="{int_y}" font-family="{font_family}" font-size="{large_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{integer_part}</text>')

            else:
                # Only integer, maybe period
                if period_text:
                    period_x = anchor_x
                    period_y = int_y
                    parts.append(f'<text x="{period_x}" y="{period_y}" font-family="{font_family}" font-size="{period_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{period_text}</text>')

                    period_width = len(period_text) * char_width_period
                    int_x = period_x - period_width - spacing
                else:
                    int_x = anchor_x

                parts.append(f'<text x="{int_x}" y="{int_y}" font-family="{font_family}" font-size="{large_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{integer_part}</text>')
        elif alignment == "left":
            # For left alignment, integer starts at anchor, decimal/period follow
            int_y = start_y + large_size

            # Calculate approximate widths for positioning
            char_width_large = large_size * 0.6
            char_width_small = small_size * 0.6

            # Integer part: left-aligned to anchor
            int_x = anchor_x
            integer_width = len(integer_part) * char_width_large
            parts.append(f'<text x="{int_x}" y="{int_y}" font-family="{font_family}" font-size="{large_size}" font-style="{font_style}" fill="{text_color}" text-anchor="start">{integer_part}</text>')

            if decimal_part:
                # Decimal part: positioned after integer with spacing
                dec_x = int_x + integer_width + spacing
                dec_y = start_y + small_size * 1.2
                parts.append(f'<text x="{dec_x}" y="{dec_y}" font-family="{font_family}" font-size="{small_size}" font-style="{font_style}" fill="{text_color}" text-anchor="start">{decimal_part}</text>')

            if period_text:
                # Period: positioned after integer with spacing, same baseline
                period_x = int_x + integer_width + spacing
                period_y = int_y
                parts.append(f'<text x="{period_x}" y="{period_y}" font-family="{font_family}" font-size="{period_size}" font-style="{font_style}" fill="{text_color}" text-anchor="start">{period_text}</text>')

        else:
            # Center alignment (original logic)
            int_x = anchor_x - spacing
            int_y = start_y + large_size
            parts.append(f'<text x="{int_x}" y="{int_y}" font-family="{font_family}" font-size="{large_size}" font-style="{font_style}" fill="{text_color}" text-anchor="end">{integer_part}</text>')

            # Render decimal part (small, left-aligned from anchor with spacing, top-aligned)
            if decimal_part:
                dec_x = anchor_x + spacing
                dec_y = start_y + small_size * 1.2  # Top-aligned
                parts.append(f'<text x="{dec_x}" y="{dec_y}" font-family="{font_family}" font-size="{small_size}" font-style="{font_style}" fill="{text_color}" text-anchor="start">{decimal_part}</text>')

            # Render period (smaller, aligned to baseline of integer, left-aligned from anchor with spacing)
            if period_text:
                period_x = anchor_x + spacing
                period_y = int_y  # Same baseline as integer
                parts.append(f'<text x="{period_x}" y="{period_y}" font-family="{font_family}" font-size="{period_size}" font-style="{font_style}" fill="{text_color}" text-anchor="start">{period_text}</text>')

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

    def _render_logo_text_group(self, comp: Dict, canvas_width: int, canvas_height: int) -> str:
        """Render logo + text centered horizontally as a group"""
        geom = self._get_geometry(comp, canvas_width, canvas_height)
        style = comp.get("style", {})

        # Get content sources
        logo_source = comp.get("logo_source", "")
        text_source = comp.get("text_source", "")

        logo_image = self._get_content(logo_source) if logo_source else None
        text_content = self._get_content(text_source)

        if not text_content:
            return ""

        parts = []

        # Logo dimensions
        logo_size = style.get("logo_size", 100)
        gap = style.get("gap", 10)

        # Text styling
        text_color = style.get("text_color", "#FFFFFF")
        font_family = style.get("font_family", "Oswald Bold")
        font_style = style.get("font_style", "normal")
        font_size = style.get("font_size", 48)

        # Calculate approximate text width (for centering)
        char_width_ratio = 0.55 if "Oswald" in font_family else 0.6
        text_width = len(text_content) * font_size * char_width_ratio

        # Total group width
        total_width = (logo_size if logo_image else 0) + (gap if logo_image else 0) + text_width

        # Center the group
        center_x = geom["x"] + geom["width"] / 2
        group_start_x = center_x - total_width / 2

        # Vertical centering (spostato più in alto)
        center_y = geom["y"] + geom["height"] / 2 - 10  # -10px per spostare in alto

        # Render logo (if provided)
        if logo_image:
            logo_x = group_start_x
            logo_y = center_y - logo_size / 2
            padding = style.get("logo_padding", 8)
            logo_color = style.get("logo_color", None)

            # If logo_color is specified, apply a color filter
            if logo_color:
                filter_id = f"logo-color-{comp.get('id', 'default')}"
                # Create a color filter that replaces white with the specified color
                parts.append(f'''<defs>
                    <filter id="{filter_id}">
                        <feColorMatrix type="matrix" values="
                            0 0 0 0 {int(logo_color[1:3], 16)/255}
                            0 0 0 0 {int(logo_color[3:5], 16)/255}
                            0 0 0 0 {int(logo_color[5:7], 16)/255}
                            0 0 0 1 0"/>
                    </filter>
                </defs>''')
                parts.append(f'<image href="{logo_image}" x="{logo_x + padding}" y="{logo_y + padding}" width="{logo_size - padding * 2}" height="{logo_size - padding * 2}" preserveAspectRatio="xMidYMid meet" filter="url(#{filter_id})"/>')
            else:
                parts.append(f'<image href="{logo_image}" x="{logo_x + padding}" y="{logo_y + padding}" width="{logo_size - padding * 2}" height="{logo_size - padding * 2}" preserveAspectRatio="xMidYMid meet"/>')

        # Render text
        text_x = group_start_x + (logo_size + gap if logo_image else 0)
        text_y = center_y + font_size / 3  # Baseline adjustment

        parts.append(f'<text x="{text_x}" y="{text_y}" font-family="{font_family}" font-size="{font_size}" font-style="{font_style}" fill="{text_color}" text-anchor="start">{text_content}</text>')

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
