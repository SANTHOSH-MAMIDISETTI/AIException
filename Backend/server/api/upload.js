const S3 = require('./s3');

module.exports = async (req, res) => {
    const {extension} = req.params;
    const url = await S3.generateUploadURL(extension);
    res.send({ url });
  
};