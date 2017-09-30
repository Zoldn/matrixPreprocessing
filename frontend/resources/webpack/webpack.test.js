const NODE_ENV = process.env.NODE_ENV || 'development';
const resolve = require('./resolve');
let config = require('./webpack.config');
config.expand('output', {
        path: resolve('/bundle'),
        publicPath: '/',
        filename: '[name].js'
    }
).expand('devtool', '#inline-source-map').plugins.shift();
delete config.expand;
delete config.entry;
module.exports = config;