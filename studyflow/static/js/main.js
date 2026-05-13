// ============================================================
// StudyFlow — Main JavaScript
//
// This file runs on EVERY page.
// It handles:
//   1. Dark mode toggle (save preference in localStorage)
//   2. Toast notification system
//   3. Sidebar mobile toggle
//   4. Current date display
//   5. Misc utilities
// ============================================================


// ============================================================
// DARK MODE
// ============================================================

// When the page loads, check if user previously chose dark mode
// localStorage stores small pieces of data in the browser
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('studyflow-theme') || 'light';
    applyTheme(savedTheme);
    
    // Display current date in header
    updateDateDisplay();
});

function toggleTheme() {
    // Get current theme from the html element
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    // Apply new theme
    applyTheme(newTheme);
    
    // Save preference so it persists when user refreshes
    localStorage.setItem('studyflow-theme', newTheme);
}

function applyTheme(theme) {
    // Set the data-theme attribute on the html element
    // Our CSS uses this to switch color variables
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update the button text and icon
    const icon = document.getElementById('themeIcon');
    const label = document.getElementById('themeLabel');
    
    if (icon && label) {
        if (theme === 'dark') {
            icon.textContent = '☀️';
            label.textContent = 'Light Mode';
        } else {
            icon.textContent = '🌙';
            label.textContent = 'Dark Mode';
        }
    }
}


// ============================================================
// TOAST NOTIFICATION
// ============================================================
// Call showToast('Your message here') from any page
// to show a small popup at the bottom right.

let toastTimeout = null; // Track existing toast timeout

function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMessage');
    
    if (!toast) return;
    
    // Set the message
    toastMsg.textContent = message;
    
    // Show the toast (adds 'show' class which triggers CSS transition)
    toast.classList.add('show');
    
    // Clear any existing timeout to avoid conflicts
    if (toastTimeout) clearTimeout(toastTimeout);
    
    // Auto-hide after `duration` milliseconds
    toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}


// ============================================================
// SIDEBAR MOBILE TOGGLE
// ============================================================

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const btn = document.getElementById('mobileMenuBtn');
    
    sidebar.classList.toggle('open');
    btn.textContent = sidebar.classList.contains('open') ? '✕' : '☰';
}

// Close sidebar when clicking outside it on mobile
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const menuBtn = document.getElementById('mobileMenuBtn');
    
    if (!sidebar || !menuBtn) return;
    
    // If click is outside sidebar and not on the menu button
    if (!sidebar.contains(e.target) && e.target !== menuBtn) {
        sidebar.classList.remove('open');
        menuBtn.textContent = '☰';
    }
});


// ============================================================
// DATE DISPLAY
// ============================================================

function updateDateDisplay() {
    const dateEl = document.getElementById('currentDate');
    if (!dateEl) return;
    
    const now = new Date();
    
    // Format: "Saturday, 9 May 2026"
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    dateEl.textContent = now.toLocaleDateString('en-IN', options);
}


// ============================================================
// KEYBOARD SHORTCUT: Press 'D' to toggle dark mode
// (Nice little easter egg for hackathon demos!)
// ============================================================

document.addEventListener('keydown', function(e) {
    // Don't trigger if user is typing in an input field
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    // Press 'D' key to toggle dark mode
    if (e.key === 'd' || e.key === 'D') {
        toggleTheme();
        showToast('Theme toggled! 🌙');
    }
});


// ============================================================
// SMOOTH ANIMATIONS on scroll (for future use)
// ============================================================

// Makes elements fade in when they scroll into view
// Uses IntersectionObserver — a modern browser API
const observerOptions = {
    threshold: 0.1,      // Trigger when 10% of element is visible
    rootMargin: '0px 0px -20px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards for scroll animations
document.addEventListener('DOMContentLoaded', function() {
    // Small delay to let page render first
    setTimeout(() => {
        document.querySelectorAll('.attendance-card, .semester-card, .reminder-card').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            observer.observe(el);
        });
    }, 100);
});
