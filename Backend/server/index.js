const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const apiRouter = require('./apiRouter');

app.use(bodyParser.json({ extended: true }));
app.use('/api', apiRouter);

app.get('/', (req, res) => {
  console.log('URL', req.url);
  res.status(200).send('Working!');
});

app.listen(8080, () => {
  console.log('Server running on port 8080');
});
