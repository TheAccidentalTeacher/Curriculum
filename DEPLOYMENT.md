# Rural Geography Simulations - Deployment Guide

## Netlify Deployment

This site is optimized for deployment on Netlify with the following features:

### 🚀 **Deployment Options**

#### **Option 1: Git-based Deployment (Recommended)**
1. Push this repository to GitHub
2. Connect your GitHub account to Netlify
3. Create new site from Git
4. Select this repository
5. Deploy settings:
   - **Build command**: (leave empty)
   - **Publish directory**: `.` (root directory)
   - **Branch**: `main`

#### **Option 2: Manual Deployment**
1. Zip all files in this directory
2. Go to Netlify Dashboard
3. Drag and drop the zip file to deploy

### 📁 **Deployment Configuration**

The following files optimize the Netlify deployment:

- **`netlify.toml`**: Main configuration with security headers and caching
- **`_redirects`**: URL routing and friendly shortcuts
- **`index.html`**: Optimized main landing page

### 🔗 **Friendly URLs**

The deployment includes these convenient shortcuts:

- `/earth-systems` → Earth Systems Explorer
- `/migration` → Global Migration Challenge  
- `/oregon-trail` → Oregon Trail Level Example
- `/nation-builder` → Nation Builder Challenge
- `/trade` → Global Trade Network
- `/amazon` → Amazon Expedition
- `/silk-road` → Silk Road Trader Challenge
- `/saharan` → Trans-Saharan Adventure
- `/teaching-guide` → Teaching Sequence Guide

### ⚡ **Performance Optimizations**

- Security headers for all HTML files
- Caching headers for CSS and JavaScript
- Automatic compression
- Fast global CDN delivery

### 📊 **Expected Performance**

- **Load time**: < 2 seconds
- **Lighthouse score**: 90+ across all metrics
- **Mobile-friendly**: Fully responsive design
- **Offline capability**: Works without internet once loaded

### 🔒 **Security Features**

- XSS protection
- Content type sniffing protection
- Frame options security
- Referrer policy enforcement

---

**Ready for deployment!** 🎉

The site will be available at: `https://your-site-name.netlify.app`
