# -*- coding: utf-8 -*-
"""
Script to generate PWA assets: icons, manifest.json, sw.js and inject into index.html and Projeto elétrico.html
"""
import os
import math
from PIL import Image, ImageDraw

def draw_rounded_rect(draw, bounds, r, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = bounds
    # Draw corners
    draw.ellipse([x1, y1, x1 + 2*r, y1 + 2*r], fill=fill)
    draw.ellipse([x2 - 2*r, y1, x2, y1 + 2*r], fill=fill)
    draw.ellipse([x1, y2 - 2*r, x1 + 2*r, y2], fill=fill)
    draw.ellipse([x2 - 2*r, y2 - 2*r, x2, y2], fill=fill)
    # Draw inner rects
    draw.rectangle([x1 + r, y1, x2 - r, y2], fill=fill)
    draw.rectangle([x1, y1 + r, x2, y2 - r], fill=fill)
    
    if outline:
        # Arcs
        draw.arc([x1, y1, x1 + 2*r, y1 + 2*r], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2*r, y1, x2, y1 + 2*r], 270, 360, fill=outline, width=width)
        draw.arc([x2 - 2*r, y2 - 2*r, x2, y2], 0, 90, fill=outline, width=width)
        draw.arc([x1, y2 - 2*r, x1 + 2*r, y2], 90, 180, fill=outline, width=width)
        # Straight edges
        draw.line([(x1 + r, y1), (x2 - r, y1)], fill=outline, width=width)
        draw.line([(x1 + r, y2), (x2 - r, y2)], fill=outline, width=width)
        draw.line([(x1, y1 + r), (x1, y2 - r)], fill=outline, width=width)
        draw.line([(x2, y1 + r), (x2, y2 - r)], fill=outline, width=width)

def generate_icons():
    sizes = {
        'icon-192.png': 192,
        'icon-512.png': 512,
        'apple-touch-icon.png': 180
    }

    # Also save icon.svg
    svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020617"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fef08a"/>
      <stop offset="40%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#b45309"/>
    </linearGradient>
    <linearGradient id="boltGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="30%" stop-color="#fef08a"/>
      <stop offset="70%" stop-color="#f59e0b"/>
      <stop offset="100%" stop-color="#d97706"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="12" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background rounded box -->
  <rect x="16" y="16" width="480" height="480" rx="96" ry="96" fill="url(#bgGrad)" stroke="url(#goldGrad)" stroke-width="8"/>

  <!-- Circuit grid lines (BIM/CAD aesthetics) -->
  <path d="M 80,160 L 200,160 L 240,200" fill="none" stroke="#38bdf8" stroke-width="4" stroke-opacity="0.6" stroke-dasharray="8,8"/>
  <circle cx="80" cy="160" r="6" fill="#38bdf8"/>
  <circle cx="240" cy="200" r="6" fill="#38bdf8"/>

  <path d="M 432,352 L 312,352 L 272,312" fill="none" stroke="#10b981" stroke-width="4" stroke-opacity="0.6" stroke-dasharray="8,8"/>
  <circle cx="432" cy="352" r="6" fill="#10b981"/>
  <circle cx="272" cy="312" r="6" fill="#10b981"/>

  <path d="M 120,400 L 180,400 L 220,360" fill="none" stroke="#a855f7" stroke-width="4" stroke-opacity="0.6"/>
  <circle cx="120" cy="400" r="6" fill="#a855f7"/>

  <path d="M 392,120 L 332,120 L 292,160" fill="none" stroke="#f59e0b" stroke-width="4" stroke-opacity="0.6"/>
  <circle cx="392" cy="120" r="6" fill="#f59e0b"/>

  <!-- Glowing Aura for Bolt -->
  <polygon points="275,60 160,260 250,260 215,445 355,235 265,235" fill="#f59e0b" filter="url(#glow)" opacity="0.6"/>

  <!-- High-voltage Lightning Bolt -->
  <polygon points="275,60 160,260 250,260 215,445 355,235 265,235" fill="url(#boltGrad)" stroke="#ffffff" stroke-width="3"/>

  <!-- CAD Monogram Text -->
  <text x="256" y="475" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="28" fill="#f8fafc" letter-spacing="4">NBR 5410</text>
</svg>'''

    with open('icon.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print("icon.svg created.")

    # Generate PNG icons using PIL
    for filename, size in sizes.items():
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Scale factor relative to 512
        s = size / 512.0

        corner_r = int(96 * s)
        margin = int(16 * s)
        bounds = [margin, margin, size - margin, size - margin]

        # Draw rounded rectangle background with dark navy/slate
        draw_rounded_rect(draw, bounds, corner_r, fill=(15, 23, 42, 255), outline=(245, 158, 11, 255), width=max(2, int(8*s)))

        # Draw circuit traces
        # Trace 1: Cyan
        p1 = [(int(80*s), int(160*s)), (int(200*s), int(160*s)), (int(240*s), int(200*s))]
        draw.line(p1, fill=(56, 189, 248, 200), width=max(2, int(4*s)))
        draw.ellipse([int(76*s), int(156*s), int(84*s), int(164*s)], fill=(56, 189, 248, 255))
        draw.ellipse([int(236*s), int(196*s), int(244*s), int(204*s)], fill=(56, 189, 248, 255))

        # Trace 2: Green
        p2 = [(int(432*s), int(352*s)), (int(312*s), int(352*s)), (int(272*s), int(312*s))]
        draw.line(p2, fill=(16, 185, 129, 200), width=max(2, int(4*s)))
        draw.ellipse([int(428*s), int(348*s), int(436*s), int(356*s)], fill=(16, 185, 129, 255))

        # Trace 3: Purple
        p3 = [(int(120*s), int(390*s)), (int(180*s), int(390*s)), (int(220*s), int(350*s))]
        draw.line(p3, fill=(168, 85, 247, 200), width=max(2, int(4*s)))

        # Lightning bolt points scaled
        bolt_pts = [
            (int(275 * s), int(60 * s)),
            (int(160 * s), int(260 * s)),
            (int(250 * s), int(260 * s)),
            (int(215 * s), int(430 * s)),
            (int(355 * s), int(235 * s)),
            (int(265 * s), int(235 * s)),
        ]

        # Draw shadow
        shadow_pts = [(x + int(2*s), y + int(3*s)) for x, y in bolt_pts]
        draw.polygon(shadow_pts, fill=(180, 83, 9, 160))

        # Draw bolt
        draw.polygon(bolt_pts, fill=(245, 158, 11, 255), outline=(255, 255, 255, 255))

        # Inner highlight
        inner_pts = [
            (int(270 * s), int(75 * s)),
            (int(180 * s), int(250 * s)),
            (int(255 * s), int(250 * s)),
            (int(228 * s), int(390 * s)),
            (int(330 * s), int(245 * s)),
            (int(268 * s), int(245 * s)),
        ]
        draw.polygon(inner_pts, fill=(254, 240, 138, 220))

        img.save(filename, format='PNG')
        print(f"{filename} ({size}x{size}) created.")

if __name__ == '__main__':
    generate_icons()
