import qrcode
import base64
import io

def generate_qr_code_no_pil(data, size=200):
    """Generate QR code without using PIL directly"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create QR code as string of 1s and 0s
    matrix = qr.get_matrix()
    
    # Convert to SVG format (which doesn't require PIL)
    svg_size = size
    svg = [
        f'<svg version="1.1" xmlns="http://www.w3.org/2000/svg" width="{svg_size}" height="{svg_size}" viewBox="0 0 {len(matrix)} {len(matrix)}">',
        '<path d="'
    ]
    
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if cell:
                svg.append(f'M{x},{y}h1v1h-1z')
    
    svg.append('" fill="black"/></svg>')
    svg_string = ''.join(svg)
    
    # Convert to base64
    svg_bytes = svg_string.encode('utf-8')
    base64_string = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{base64_string}"
