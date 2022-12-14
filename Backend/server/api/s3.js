const S3 = require('aws-sdk/clients/s3');
const dotenv = require('dotenv');
const crypto = require('crypto');
const util = require('util');
const randomBytes = util.promisify(crypto.randomBytes);

dotenv.config();

const bucketName = '#YourBucketNameHERE';
const region = 'us-east-1';
const accessKeyID = process.env.AWS_ACCESS_KEY_ID;
const secretAccessKey = process.env.AWS_SECRET_ACCESS_KEY;

const s3 = new S3({
  region,
  accessKeyID,
  secretAccessKey,
  signatureVersion: 'v4',
});

exports.generateUploadURL = async (extension) => {
  const rawBytes = await randomBytes(16);
  const imgName = rawBytes.toString('hex') + extension;
  //The validity of the secure URL is set to 60 seconds.
  //If a request to secure URL is not made in under 60 seconds, it expires.
  // 'Expires : 60' in params addresses 60 second Secure URL validity.
  const params = {
    Bucket: bucketName,
    Key: pdfName,
    ContentType: extension == '.png' ? 'application/png' : 'application/json',
    Expires: 60,
  };
  return s3.getSignedUrlPromise('putObject', params);
};