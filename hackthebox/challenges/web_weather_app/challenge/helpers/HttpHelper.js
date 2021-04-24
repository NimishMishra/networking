const http = require('http');

module.exports = {
	HttpGet(url) {
		return new Promise((resolve, reject) => {
			http.get(url, res => {
				let body = '';
				res.on('data', chunk => body += chunk);
				res.on('end', () => {
					try {
						resolve(JSON.parse(body));
					} catch(e) {
						resolve(false);
					}
				});
			}).on('error', reject);
		});
	}
}