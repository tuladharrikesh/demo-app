'use strict';

const express = require('express');
const app = express();

const PORT = 8080;
const HOST = '0.0.0.0';

app.set('view engine', 'pug')
// Application
app.get('/', (req, res) => {
    res.sendFile('index.html', {root: __dirname});
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`)
