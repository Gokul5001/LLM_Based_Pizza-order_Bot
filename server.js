const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files from the same directory
app.use(express.static(__dirname));

// Route for the main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
    console.log(`Make sure the Python Flask server is also running at http://localhost:5000`);
});