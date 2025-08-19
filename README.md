# Interactive Book Reader

A beautiful, interactive web-based book reader that displays your PDF images as a realistic page-turning book experience.

## Features

### 📖 Realistic Book Experience
- **3D Page Turning**: Smooth page flip animations that mimic real book pages
- **Book Spine**: Visual spine effect in the middle of each spread
- **Page Stacking**: Proper z-index management for realistic page layering
- **High-Quality Images**: Displays your extracted PDF images at full resolution (3081x2400)

### 🎮 Interactive Controls
- **Navigation Buttons**: Previous/Next buttons with smooth animations
- **Page Dots**: Click any dot to jump directly to that page
- **Auto-Play**: Automatic page turning with pause/play controls
- **Keyboard Navigation**: Arrow keys for easy page turning
- **Touch/Swipe Support**: Mobile-friendly swipe gestures
- **Click Navigation**: Click left/right sides of the book to turn pages

### 🎨 Beautiful Design
- **Gradient Background**: Elegant purple gradient backdrop
- **Glass Morphism**: Modern frosted glass effects
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Loading Animation**: Smooth loading experience with progress messages
- **Page Numbers**: Overlay page numbers on each spread

## How to Use

### Getting Started
1. Open `index.html` in any modern web browser
2. Wait for all pages to load (loading screen will disappear)
3. Start reading and enjoy the interactive experience!

### Navigation Methods

#### Keyboard Shortcuts
- `←` (Left Arrow): Previous page
- `→` (Right Arrow): Next page  
- `?`: Show help dialog
- `Esc`: Close help dialog

#### Mouse/Touch Controls
- **Click Navigation**: Click left side of book for previous page, right side for next page
- **Button Controls**: Use Previous/Next buttons
- **Page Dots**: Click any dot to jump to that page
- **Auto-Play**: Click the play button to start automatic page turning
- **Mobile Swipe**: Swipe left for next page, right for previous page

### Features in Detail

#### Auto-Play Mode
- Click the "Auto Play" button to start automatic page progression
- Pages turn every 3 seconds
- When reaching the last page, automatically returns to the beginning
- Click "Pause" to stop auto-play at any time

#### Page Indicators
- Dots at the bottom show your current position in the book
- Active page is highlighted with a glowing white dot
- Click any dot to instantly jump to that page

#### Responsive Design
- **Desktop**: Full-size book experience with all controls
- **Tablet**: Optimized layout with touch-friendly controls  
- **Mobile**: Compact view with swipe navigation

## Technical Details

### Files Structure
```
extract-pdf-images/
├── index.html          # Main HTML structure
├── style.css           # Styling and animations
├── script.js           # Interactive functionality
├── book_images/        # Extracted PDF images
│   ├── page_001_img_001.png
│   ├── page_002_img_001.png
│   └── ... (11 pages total)
└── README.md          # This file
```

### Browser Compatibility
- **Chrome/Edge**: Full support for all features
- **Firefox**: Full support for all features  
- **Safari**: Full support for all features
- **Mobile Browsers**: Touch/swipe support included

### Performance Optimizations
- **Lazy Loading**: Images load progressively for faster initial load
- **Hardware Acceleration**: CSS transforms use GPU acceleration
- **Efficient Z-Index Management**: Optimized layer stacking
- **Smooth Animations**: 60fps page turning animations

## Customization

### Changing Auto-Play Speed
Edit `script.js` and modify the `speed` property:
```javascript
this.speed = 3000; // Change to desired milliseconds
```

### Modifying Page Turn Duration
Edit `style.css` and modify the transition duration:
```css
.page {
    transition: transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
```

### Customizing Colors
Edit the CSS gradient in `style.css`:
```css
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

## Troubleshooting

### Images Not Loading
- Ensure all image files are in the `book_images/` directory
- Check that image filenames match the expected pattern: `page_XXX_img_001.png`
- Verify your web server can serve the image files (if using a local server)

### Performance Issues
- Try reducing the image resolution if needed
- Ensure you're using a modern browser with hardware acceleration enabled
- Close other browser tabs to free up memory

### Mobile Issues
- Make sure touch events are enabled in your browser
- Try refreshing the page if swipe gestures aren't working
- Ensure you're not accidentally triggering browser navigation gestures

## Credits

This interactive book reader was created using:
- **PyMuPDF (fitz)**: For PDF image extraction
- **Vanilla JavaScript**: For interactive functionality
- **CSS3 Transforms**: For 3D page turning effects
- **Modern Web APIs**: For touch/gesture support

Enjoy your interactive reading experience! 📚✨
