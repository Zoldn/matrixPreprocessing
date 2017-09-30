const NODE_ENV = process.env.NODE_ENV || 'development';
const LiveReloadPlugin = require('webpack-livereload-plugin');
const resolve = require('./resolve');
const local = require('./local');
let config = require('./webpack.config');
config
    .expand('output', {
        path: resolve('/../web/bundle'),
        publicPath: '/bundle/',
        filename: '[name].js'
    })
    .expand('devtool', '#eval-source-map')
    .expand('watch', NODE_ENV === 'watch')
    .expand('cache', NODE_ENV === 'watch')
    .expand('watchOptions', {
        aggregateTimeout: 500
    });

if (local.livereload) {
    config.plugins.push(new LiveReloadPlugin());
}
delete config.expand;
module.exports = config;