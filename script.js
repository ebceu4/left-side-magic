class TurnJSBook {
    constructor() {
        console.log('📚 TurnJSBook: Starting initialization...');
        this.totalPages = 21; // 21 individual pages (cover + 20 content pages)
        this.isLoaded = false;
        
        this.flipbook = $('#flipbook');
        this.prevBtn = $('#prev-btn');
        this.nextBtn = $('#next-btn');
        this.loadingElement = $('#loading');
        
        this.init();
    }
    
    async init() {
        console.log('🔄 TurnJSBook: Starting initialization...');
        try {
            this.showLoading();
            await this.createPages();
            this.initializeTurnJS();
            this.bindEvents();
            this.hideLoading();
            console.log('✅ TurnJSBook: Initialization complete!');
        } catch (error) {
            console.error('❌ TurnJSBook: Initialization failed:', error);
            this.showError(error);
        }
    }
    
    showLoading() {
        this.loadingElement.removeClass('hidden');
    }
    
    hideLoading() {
        this.loadingElement.addClass('hidden');
    }
    
    showError(error) {
        console.error('💥 showError: Displaying error to user:', error);
        const loadingText = this.loadingElement.find('p');
        loadingText.text(`Error: ${error.message}. Check console for details.`);
        loadingText.css('color', '#ff6b6b');
    }
    
    async createPages() {
        console.log('📖 createPages: Creating individual pages for Turn.js...');
        
        // Create pages using the split individual page images
        for (let i = 0; i < this.totalPages; i++) {
            console.log(`📄 createPages: Processing page ${i + 1}/${this.totalPages}...`);
            
            let imagePath;
            if (i === 0) {
                // Cover page
                imagePath = 'individual_pages/page_000_cover.jpg';
            } else {
                // Regular pages (1-21)
                imagePath = `individual_pages/page_${i.toString().padStart(3, '0')}.jpg`;
            }
            
            // Create a page for each individual image
            const page = $('<div class="page"></div>');
            const img = $('<img>').attr('src', imagePath).attr('alt', `Page ${i + 1}`);
            
            console.log(`🔍 createPages: Loading image for page ${i + 1}: ${imagePath}`);
            await this.loadImage(img[0]);
            
            page.append(img);
            this.flipbook.append(page);
        }
        
        console.log(`✅ createPages: Created ${this.totalPages} individual pages`);
    }
    
    loadImage(img) {
        return new Promise((resolve, reject) => {
            console.log(`🔍 loadImage: Loading ${img.src}`);
            
            const timeout = setTimeout(() => {
                console.error(`⏰ loadImage: Timeout loading ${img.src}`);
                reject(new Error(`Image load timeout: ${img.src}`));
            }, 30000);
            
            img.onload = () => {
                console.log(`✅ loadImage: Loaded ${img.src}`);
                clearTimeout(timeout);
                resolve();
            };
            
            img.onerror = (error) => {
                console.error(`❌ loadImage: Failed to load ${img.src}`, error);
                clearTimeout(timeout);
                reject(new Error(`Failed to load image: ${img.src}`));
            };
            
            if (img.complete) {
                console.log(`⚡ loadImage: Already loaded ${img.src}`);
                clearTimeout(timeout);
                resolve();
            }
        });
    }
    
    initializeTurnJS() {
        console.log('📚 initializeTurnJS: Initializing Turn.js...');
        
        // Check if jQuery and Turn.js are loaded
        if (typeof $ === 'undefined') {
            throw new Error('jQuery is not loaded');
        }
        
        if (typeof $.fn.turn === 'undefined') {
            throw new Error('Turn.js is not loaded');
        }
        
        console.log('✅ initializeTurnJS: jQuery and Turn.js are loaded');
        console.log('📖 initializeTurnJS: Flipbook element:', this.flipbook);
        console.log('📊 initializeTurnJS: Number of pages in flipbook:', this.flipbook.children().length);
        
        this.flipbook.turn({
            width: 800,
            height: 600,
            autoCenter: true,
            duration: 1000,
            gradients: true,
            elevation: 50,
            when: {
                turning: (event, page, view) => {
                    console.log(`📖 Turn.js: Turning to page ${page}`);
                },
                turned: (event, page, view) => {
                    console.log(`✅ Turn.js: Turned to page ${page}`);
                    this.updateUI(page);
                }
            }
        });
        
        // Set initial page
        this.updateUI(1);
        this.isLoaded = true;
        
        console.log('✅ initializeTurnJS: Turn.js initialized successfully!');
    }
    
    bindEvents() {
        console.log('🎮 bindEvents: Binding navigation events...');
        
        this.prevBtn.on('click', () => {
            if (this.isLoaded) {
                this.flipbook.turn('previous');
            }
        });
        
        this.nextBtn.on('click', () => {
            if (this.isLoaded) {
                this.flipbook.turn('next');
            }
        });
        
        // Keyboard navigation
        $(document).on('keydown', (e) => {
            if (!this.isLoaded) return;
            
            if (e.key === 'ArrowLeft') {
                this.flipbook.turn('previous');
            } else if (e.key === 'ArrowRight') {
                this.flipbook.turn('next');
            }
        });
        
        console.log('✅ bindEvents: Events bound successfully!');
    }
    
    updateUI(page) {
        if (!page) page = this.flipbook.turn('page');
        
        // Update navigation buttons
        this.prevBtn.prop('disabled', page <= 1);
        this.nextBtn.prop('disabled', page >= this.totalPages);
        
        // Update page shadows
        this.updatePageShadows(page);
        
        console.log(`🔄 updateUI: Updated UI for page ${page}/${this.totalPages}`);
    }
    
    updatePageShadows(page) {
        // Remove all existing shadow classes
        this.flipbook.find('.page').removeClass('left-shadow right-shadow');
        
        // Get current view pages (Turn.js shows 2 pages in spread view)
        const view = this.flipbook.turn('view');
        
        if (view && view.length > 0) {
            // Right page always has shadow (except when it's the last single page)
            if (view.length >= 2) {
                // Two-page spread
                const leftPageIndex = view[0] - 1;  // Convert to 0-based index
                const rightPageIndex = view[1] - 1; // Convert to 0-based index
                
                // Left page shadow only appears after first page is turned (page > 1)
                if (page > 1 && leftPageIndex >= 0) {
                    this.flipbook.find('.page').eq(leftPageIndex).addClass('left-shadow');
                }
                
                // Right page shadow
                if (rightPageIndex >= 0) {
                    this.flipbook.find('.page').eq(rightPageIndex).addClass('right-shadow');
                }
            } else {
                // Single page view (first or last page)
                const pageIndex = view[0] - 1; // Convert to 0-based index
                
                if (page === 1) {
                    // First page - only right shadow
                    this.flipbook.find('.page').eq(pageIndex).addClass('right-shadow');
                } else {
                    // Last page - only left shadow
                    this.flipbook.find('.page').eq(pageIndex).addClass('left-shadow');
                }
            }
        }
        
        console.log(`🌟 updatePageShadows: Updated shadows for page ${page}`);
    }
}

// Initialize when document is ready
$(document).ready(() => {
    console.log('🌟 Document ready - Starting Turn.js book...');
    
    try {
        new TurnJSBook();
    } catch (error) {
        console.error('💥 Failed to initialize Turn.js book:', error);
        $('#loading p').text('Failed to load book. Please refresh the page.');
        $('#loading p').css('color', '#ff6b6b');
    }
});