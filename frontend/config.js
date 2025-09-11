// Frontend configuration
// This file loads environment variables for the frontend
const config = {
    API_BASE_URL: 'http://localhost:8000' // Default value, can be overridden by environment
};

// Try to load from .env file if available (for development)
try {
    // Note: This is a simple implementation. In production, you might want to use a build tool
    // to replace these values at build time
    const envContent = `
API_BASE_URL=http://localhost:8000
`;
    // Parse .env content (simplified)
    const lines = envContent.split('\n');
    lines.forEach(line => {
        const [key, value] = line.split('=');
        if (key && value) {
            config[key.trim()] = value.trim();
        }
    });
} catch (error) {
    console.log('Using default configuration');
}

window.CONFIG = config;
