/**
 * RubyMark.js - Live rendering of RubyMark syntax in web browsers
 * Handles standard Markdown along with custom syntax:
 *   - Ruby annotations: {base}(text) -> <ruby>base<rp> (</rp><rt>text</rt><rp>) </rp></ruby>
 *   - Strikethroughs: ~~text~~ -> <del>text</del>
 */

(function() {
    const MARKED_CDN_URL = 'https://cdn.jsdelivr.net/npm/marked@12.0.1/lib/marked.umd.js';
    let markedInitialized = false;

    /**
     * Dynamically loads a script from a URL and returns a Promise.
     */
    function loadScript(url) {
        return new Promise((resolve, reject) => {
            // Check if marked is already loaded in the environment
            if (window.marked) {
                resolve(window.marked);
                return;
            }
            
            // Check if there is an existing script tag loading marked
            const existingScript = document.querySelector(`script[src="${url}"]`);
            if (existingScript) {
                existingScript.addEventListener('load', () => resolve(window.marked));
                existingScript.addEventListener('error', (e) => reject(e));
                return;
            }

            const script = document.createElement('script');
            script.src = url;
            script.async = true;
            script.onload = () => resolve(window.marked);
            script.onerror = (e) => reject(e);
            document.head.appendChild(script);
        });
    }

    /**
     * Initialize marked.js extensions
     */
    function initMarked(markedInstance) {
        if (markedInitialized) return;

        // Custom Rubymark Extension
        // Matches {base}(text) where base doesn't have curly braces, and text doesn't have closing parenthesis
        const rubymarkExtension = {
            name: 'rubymark',
            level: 'inline',
            start(src) {
                return src.indexOf('{');
            },
            tokenizer(src, tokens) {
                const rubyRegex = /^\{([^{}]+)\}\(([^)]+)\)/;
                const match = rubyRegex.exec(src);
                if (match) {
                    return {
                        type: 'rubymark',
                        raw: match[0],
                        base: match[1],
                        text: match[2]
                    };
                }
            },
            renderer(token) {
                return `<ruby>${token.base}<rp> (</rp><rt>${token.text}</rt><rp>) </rp></ruby>`;
            }
        };

        markedInstance.use({
            extensions: [rubymarkExtension],
            gfm: true,
            breaks: true // Matches python nl2br
        });

        markedInitialized = true;
    }

    /**
     * Helper to dedent indented markdown text from HTML templates
     */
    function dedent(str) {
        if (!str) return '';
        const lines = str.split('\n');
        
        let minIndent = Infinity;
        let startIdx = 0;
        
        // Skip first line if empty
        if (lines.length > 0 && lines[0].trim() === '') {
            startIdx = 1;
        }
        
        for (let i = startIdx; i < lines.length; i++) {
            const line = lines[i];
            if (line.trim() === '') continue;
            const match = line.match(/^(\s*)/);
            if (match) {
                const indent = match[1].length;
                if (indent < minIndent) {
                    minIndent = indent;
                }
            }
        }
        
        if (minIndent === Infinity) {
            minIndent = 0;
        }
        
        const processedLines = lines.map((line, idx) => {
            if (idx === 0 && line.trim() === '') return '';
            if (line.trim() === '') return '';
            return line.slice(minIndent);
        });
        
        while (processedLines.length > 0 && processedLines[0].trim() === '') {
            processedLines.shift();
        }
        while (processedLines.length > 0 && processedLines[processedLines.length - 1].trim() === '') {
            processedLines.pop();
        }
        
        return processedLines.join('\n');
    }

    /**
     * Web Component <ruby-mark> (Standard compliant custom element)
     */
    class RubyMarkElement extends HTMLElement {
        constructor() {
            super();
            this._rawContent = '';
        }

        connectedCallback() {
            if (!this._rawContent) {
                this._rawContent = this.getAttribute('content') || this.innerHTML;
            }
            this.render();
        }

        static get observedAttributes() {
            return ['content'];
        }

        attributeChangedCallback(name, oldValue, newValue) {
            if (name === 'content' && oldValue !== newValue) {
                this._rawContent = newValue;
                this.render();
            }
        }

        async render() {
            try {
                const markedInstance = await loadScript(MARKED_CDN_URL);
                initMarked(markedInstance);

                let markdownText = '';
                if (this.hasAttribute('content')) {
                    markdownText = this.getAttribute('content');
                } else {
                    // textContent decodes entity names like &lt; into < automatically
                    markdownText = this.textContent;
                }

                const cleanedText = dedent(markdownText);
                const html = markedInstance.parse(cleanedText);
                this.innerHTML = html;
            } catch (err) {
                console.error('Failed to parse <ruby-mark> content:', err);
            }
        }
    }

    /**
     * Process non-hyphened legacy <rubymark> elements
     */
    async function processRubyMarkLegacyElements() {
        const elements = document.querySelectorAll('rubymark');
        if (elements.length === 0) return;

        try {
            const markedInstance = await loadScript(MARKED_CDN_URL);
            initMarked(markedInstance);

            elements.forEach(el => {
                if (el.dataset.rubymarkProcessed) return;
                el.dataset.rubymarkProcessed = 'true';

                let markdownText = el.getAttribute('content') || el.textContent;
                const cleanedText = dedent(markdownText);
                el.innerHTML = markedInstance.parse(cleanedText);
            });
        } catch (err) {
            console.error('Failed to parse <rubymark> content:', err);
        }
    }

    // Set up MutationObserver to watch for dynamically inserted <rubymark> tags
    const observer = new MutationObserver((mutations) => {
        let needsReprocess = false;
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.tagName === 'RUBYMARK' || node.querySelectorAll('rubymark').length > 0) {
                        needsReprocess = true;
                    }
                }
            });
        });
        if (needsReprocess) {
            processRubyMarkLegacyElements();
        }
    });

    // Register objects, components, and scan document
    const RubyMark = {
        render: async function(text) {
            const markedInstance = await loadScript(MARKED_CDN_URL);
            initMarked(markedInstance);
            return markedInstance.parse(text);
        },
        renderSync: function(text) {
            if (window.marked && markedInitialized) {
                return window.marked.parse(text);
            }
            throw new Error("marked.js is not loaded or initialized yet. Use async RubyMark.render(text) instead.");
        }
    };

    if (typeof window !== 'undefined') {
        window.RubyMark = RubyMark;

        // Register custom element
        if (window.customElements && !window.customElements.get('ruby-mark')) {
            window.customElements.define('ruby-mark', RubyMarkElement);
        }

        // Run scanning and setup observer on document load
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                processRubyMarkLegacyElements();
                observer.observe(document.body, { childList: true, subtree: true });
            });
        } else {
            processRubyMarkLegacyElements();
            observer.observe(document.body, { childList: true, subtree: true });
        }
    }

    if (typeof module !== 'undefined' && module.exports) {
        module.exports = RubyMark;
    }
})();
