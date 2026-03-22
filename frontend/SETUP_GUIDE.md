# Medical AI Assistant Frontend - Setup Guide

## 📁 File Structure

```
.
├── index.html          # Main HTML entry point with React setup
├── style.css           # Complete styling (responsive design)
├── app.jsx             # React component with all functionality
└── (run on http://localhost:3000 or similar)
```

## 🚀 Setup Instructions

### Option 1: Simple HTTP Server (Recommended for Development)

```bash
# Using Python 3
python -m http.server 8080

# Or using Python 2
python -m SimpleHTTPServer 8080

# Or using Node.js (http-server)
npx http-server
```

Then open: `http://localhost:8080` (or `http://localhost:3000` depending on your server)

### Option 2: Live Server Extension (VS Code)

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## 🔧 Configuration

### API Endpoint Update

In `app.jsx`, update the API base URL to match your backend:

```javascript
// Line ~15 in app.jsx
const API_BASE_URL = "http://localhost:8000"; // Change this to your API URL
```

Common configurations:
- Local development: `http://localhost:8000`
- Production: `https://your-domain.com/api`
- Docker: `http://api-service:8000`

### CORS Configuration (Important!)

If your backend is on a different domain, you need to enable CORS in FastAPI:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📱 Features

### 1. Chat Interface
- ✅ Real-time question asking
- ✅ Auto-scrolling to latest messages
- ✅ Loading indicators
- ✅ Quick prompt suggestions
- ✅ Source document display

### 2. File Upload
- ✅ Drag and drop PDF files
- ✅ Click to browse and select
- ✅ Multiple file upload
- ✅ File preview before upload
- ✅ File removal

### 3. UI/UX
- ✅ Sidebar navigation
- ✅ Empty state with suggestions
- ✅ Alert messages (success, error, warning)
- ✅ Responsive design (mobile-friendly)
- ✅ Smooth animations
- ✅ Dark/Light mode ready

## 🎨 Customization

### Change Colors

Edit the CSS variables at the top of `style.css`:

```css
:root {
    --primary: #6366f1;           /* Main color */
    --secondary: #8b5cf6;         /* Secondary color */
    --success: #10b981;           /* Success alerts */
    --danger: #ef4444;            /* Error alerts */
    --text-primary: #1f2937;      /* Main text color */
    /* ... more variables ... */
}
```

### Change Logo and Branding

In `app.jsx`, update the sidebar:

```javascript
<div className="logo">
    🏥 <span className="logo-text">MediAI</span>
</div>
<div className="tagline">Your Medical Assistant</div>
```

### Modify Quick Prompts

In `app.jsx`, find and update:

```javascript
const quickPrompts = [
    "What is diabetes?",
    "How to prevent heart disease?",
    "Explain hypertension symptoms",
    "What causes asthma?",
];
```

## 🔌 API Integration

### Ask Question Endpoint

**Request:**
```
POST /ask/
Content-Type: multipart/form-data

question: "What is diabetes?"
```

**Response:**
```json
{
    "response": "Diabetes is a chronic disease...",
    "sources": ["uploaded_docs\\DIABETES.pdf"]
}
```

### Upload Files Endpoint

**Request:**
```
POST /upload_pdfs/
Content-Type: multipart/form-data

files: [file1.pdf, file2.pdf, ...]
```

**Response:**
```json
{
    "message": "Files uploaded successfully",
    "count": 2
}
```

## 🐛 Troubleshooting

### Issue: "Failed to get response" or API errors

**Solution:**
1. Check browser console (F12) for network errors
2. Verify API base URL is correct in `app.jsx`
3. Ensure backend is running
4. Check CORS configuration on backend

### Issue: File upload fails

**Solution:**
1. Verify endpoint is `/upload_pdfs/`
2. Ensure only PDF files are being sent
3. Check file size limits on backend
4. Verify CORS is enabled

### Issue: Style not loading

**Solution:**
1. Ensure `style.css` is in the same directory as `index.html`
2. Clear browser cache (Ctrl+Shift+Delete)
3. Check browser console for 404 errors

### Issue: React not loading

**Solution:**
1. Check internet connection (CDN requires external access)
2. Verify Babel is loading (check console for errors)
3. Check if `app.jsx` is in the same directory

## 📊 Browser Compatibility

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Production Deployment

### Option 1: Static Hosting (Vercel, Netlify, GitHub Pages)

1. Ensure API_BASE_URL points to production backend
2. Deploy the three files to your hosting provider
3. Configure CORS on backend for your production domain

### Option 2: Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
EXPOSE 8080
CMD ["npx", "http-server"]
```

### Option 3: With Backend Server

Host frontend on same server as backend:
- Put files in a `public/` or `static/` folder
- Serve via FastAPI's `StaticFiles` or Express
- Use relative URLs: `const API_BASE_URL = "/api";`

## 📝 Notes

- Frontend is fully client-side rendered (no build needed)
- Uses React 18 from CDN (no npm installation required)
- Responsive design works on all screen sizes
- All styling is inline CSS (no external dependencies except fonts)

## 🆘 Support

If you encounter issues:

1. Check browser console (F12 → Console tab)
2. Verify API endpoints are correct
3. Ensure backend is running
4. Check network tab for failed requests
5. Review error messages in alerts

---

**Made with ❤️ for Medical Professionals**
