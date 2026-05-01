const https = require('https');

https.get('https://threadborn.vercel.app/api/dashboard?action=config&lang=en', (resp) => {
  let data = '';
  resp.on('data', (chunk) => { data += chunk; });
  resp.on('end', () => {
    console.log("English Config:", data);
  });
}).on("error", (err) => {
  console.log("Error: " + err.message);
});
