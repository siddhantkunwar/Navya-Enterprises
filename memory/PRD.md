# Navya Enterprises - Agricultural Equipment Catalogue Website

## Original Problem Statement
Build a showcase/catalogue website for Navya Enterprises, an agricultural equipment dealership based in Udaipur, Rajasthan (since 1999). The website layout is based on hand-drawn paper wireframes provided by the client with 5 pages. Currently a showcase site, with plans to convert to e-commerce later.

## Architecture
- **Frontend**: React.js with Tailwind CSS, React Router, Lucide React icons
- **Backend**: FastAPI (Python) with MongoDB (Motor async driver)
- **Database**: MongoDB - products collection with 72 products across 6 categories
- **Fonts**: Cormorant Garamond (headings) + Outfit (body)
- **Brand Colors**: Soft Sage Green #AAB696, Dark Olive Green #38443B, Earthy Brown #6B3F34, Deep Forest Green #4B5D44
- **Deployment**: Vercel (frontend), Emergent preview (backend)

## User Personas
- **Agricultural professionals** looking for equipment and supplies
- **Government/institutional buyers** for bulk procurement
- **Nursery/greenhouse operators** seeking tools and inputs
- **B2B clients** for ongoing procurement needs

## Core Requirements (Static)
1. 5-page website: Home, About Us, Products, Product Detail, Connect With Us
2. Match hand-drawn paper wireframe layouts
3. Use ONLY client-provided brand color palette
4. 72 products across 6 categories from catalogue
5. Product filtering by category (button + sidebar checkbox)
6. Connect page = info display only (NOT a form)
7. No founder description on About page

## What's Been Implemented

### Initial Build (Jan 2026)
- [x] Full 5-page website matching wireframe layouts
- [x] Header with Navya logo + navigation (Home, About Us, Products, Connect)
- [x] Footer with company info, quick links, Instagram & YouTube social links
- [x] Home Page: Hero image, Brief About section, Popular Products carousel, Brands carousel, Testimonials
- [x] About Us Page: Business Strategy & Vision, About Our Firm, Product Range
- [x] Products Page: Hero, search bar, category button filters, sidebar checkbox filters, 4-column product grid (72 products)
- [x] Product Detail Page: Back button, product image + description, model variants section
- [x] Connect Page: Hero, Get In Touch info display, Google Maps embed
- [x] All products seeded from catalogue with descriptions, categories, and model variants
- [x] Backend API endpoints for products, categories, and contact info
- [x] Responsive design with mobile navigation
- [x] Brand color palette strictly applied throughout
- [x] 100% test pass rate (backend, frontend, integration)

### Home Page Refinements (Jan 2026)
- [x] Header changed to white bg for logo contrast
- [x] Logo size increased (header h-[127px])
- [x] Font changed to Playfair Display (headings) + Lato (body) per reference
- [x] Hero image replaced with client-provided field image
- [x] Tagline: "Built for the fields that feed the future."
- [x] Infinite CSS marquee for brand partner logos
- [x] Smart back button with route state passing

### Real Product Images (Jan 2026)
- [x] Uploaded and mapped .webp images for Rotavator, Seed Drill, Cultivator
- [x] Cleaned up product variant arrays for non-variant products

### Vercel Deployment & SEO (Feb 2026)
- [x] Created `vercel.json` with SPA rewrites for React Router deep links
- [x] Added `.npmrc` with `legacy-peer-deps=true` for npm compatibility
- [x] Added `.nvmrc` pinning Node.js to v20
- [x] Added `engines` field in package.json for Node 20
- [x] Added `ajv@8.17.1` as explicit dependency (fixes CRA build on Vercel)
- [x] Comprehensive SEO meta tags: title, description, keywords, author, canonical
- [x] Open Graph tags (og:title, og:description, og:image, og:url, og:site_name)
- [x] Twitter Card tags (summary_large_image)
- [x] Favicon and apple-touch-icon set to Navya logo
- [x] Theme-color updated to brand green #2E7D32
- [x] robots meta set to index, follow

### Image Optimization & Independence (Feb 2026)
- [x] Moved hero image from Emergent CDN to local `/hero-home.webp` (25MB → 740KB)
- [x] Compressed all 69 product images PNG→WebP preserving RGBA transparency (253MB → 2MB)
- [x] Fixed black background bug (was converting RGBA→RGB, losing transparency)
- [x] Removed all PNG originals — only lightweight WebP files remain
- [x] Zero external image dependencies — all assets are local
- [x] 100% test pass rate (iteration 9)
- [x] Removed all backend API dependencies from frontend
- [x] Created `/src/data/products.js` with 70 products, categories, popular filter, getProductById helper
- [x] Created `/src/data/contact.js` with contact info
- [x] Updated HomePage, ProductsPage, ProductDetailPage, ConnectPage to use static imports
- [x] Removed axios API calls from all pages
- [x] Site is now fully static — works on Vercel with zero backend dependency
- [x] 100% test pass rate (iteration 8)

## Deployment Notes
- **Vercel**: Root directory = `frontend/`. `vercel.json` handles SPA rewrites. Build: `yarn build`. Output: `build/`.
- **No backend needed**: All data is embedded in the frontend as static JS files.
- **`REACT_APP_BACKEND_URL` is no longer required** on Vercel — can be removed from env vars.
- **OG Image**: After custom domain setup, update `og:image`, `og:url`, and `canonical` in `index.html` with production domain absolute URLs.
- **Node Version**: Set `NODE_VERSION=20` in Vercel env vars.

## Prioritized Backlog

### P1 (Important)
- Add WhatsApp contact button
- Product inquiry form on product detail page
- Product search with suggestions/autocomplete

### P2 (Nice to Have)
- Image gallery/multiple images per product
- Product comparison feature
- Download product catalogue PDF
- Newsletter/enquiry subscription

### Future (E-commerce Conversion)
- Shopping cart & checkout
- Online payment integration
- User accounts & order history
- Inventory management admin panel
