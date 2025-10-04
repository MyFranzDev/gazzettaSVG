#!/usr/bin/env node

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function convertSvgToPng(svgPath, pngPath, scale = 2) {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // Read SVG file
        const svgContent = fs.readFileSync(svgPath, 'utf8');

        // Extract dimensions from SVG
        const widthMatch = svgContent.match(/width="(\d+)"/);
        const heightMatch = svgContent.match(/height="(\d+)"/);

        if (!widthMatch || !heightMatch) {
            throw new Error('Could not extract SVG dimensions');
        }

        const width = parseInt(widthMatch[1]);
        const height = parseInt(heightMatch[1]);

        // Set viewport to SVG dimensions * scale for high quality
        await page.setViewport({
            width: width * scale,
            height: height * scale,
            deviceScaleFactor: scale
        });

        // Create HTML with embedded SVG
        const html = `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        width: ${width}px;
                        height: ${height}px;
                    }
                    svg {
                        display: block;
                    }
                </style>
            </head>
            <body>
                ${svgContent}
            </body>
            </html>
        `;

        // Load the HTML
        await page.setContent(html, { waitUntil: 'networkidle0' });

        // Wait a bit for fonts to load
        await new Promise(resolve => setTimeout(resolve, 500));

        // Take screenshot
        await page.screenshot({
            path: pngPath,
            type: 'png',
            clip: {
                x: 0,
                y: 0,
                width: width,
                height: height
            }
        });

        console.log(`PNG generated successfully: ${pngPath}`);

    } catch (error) {
        console.error('Error converting SVG to PNG:', error);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

// Get command line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
    console.error('Usage: node svg_to_png.js <svg_path> <png_path> [scale]');
    process.exit(1);
}

const svgPath = args[0];
const pngPath = args[1];
const scale = args[2] ? parseInt(args[2]) : 2; // Default 2x for retina quality

if (!fs.existsSync(svgPath)) {
    console.error(`SVG file not found: ${svgPath}`);
    process.exit(1);
}

convertSvgToPng(svgPath, pngPath, scale);
