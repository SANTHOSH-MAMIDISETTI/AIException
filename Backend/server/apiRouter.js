const express = require('express');
const router = express.Router();
const upload = require('./api/upload.js');

//Upload IMG to Amazon Bucket
router.get('/upload/:extension', upload);

module.exports = router;



