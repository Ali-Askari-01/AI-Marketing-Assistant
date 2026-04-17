// Debug script to check if the application loads correctly
console.log('Debug script loaded');

// Check if DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded');
    
    // Check if main app object exists
    if (typeof app !== 'undefined') {
        console.log('App object exists:', app);
        console.log('App methods:', Object.getOwnPropertyNames(app));
    } else {
        console.error('App object not found');
    }
    
    // Check if auth object exists
    if (typeof auth !== 'undefined') {
        console.log('Auth object exists:', auth);
    } else {
        console.error('Auth object not found');
    }
    
    // Test basic functionality
    try {
        const testDiv = document.createElement('div');
        testDiv.innerHTML = '<p style="color: green;">Debug test successful!</p>';
        document.body.appendChild(testDiv);
        setTimeout(() => testDiv.remove(), 3000);
    } catch (error) {
        console.error('Debug test failed:', error);
    }
});
