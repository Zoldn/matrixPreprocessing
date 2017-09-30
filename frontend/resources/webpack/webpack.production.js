const NODE_ENV = process.env.NODE_ENV || 'development';
const resolve = require('./resolve');
let config = require('./webpack.config');
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
config.expand('output', {
        path: resolve('/../web/build'),
        publicPath: '/build/',
        filename: '[name].js'
    }
).plugins.push(
    // Compress extracted CSS. We are using this plugin so that possible
    // duplicated CSS from different components can be deduped.
    new OptimizeCSSPlugin({
        cssProcessorOptions: {
            safe: true
        }
    }),
    new UglifyJsPlugin({
        compress: {
            warnings: false,
            drop_console: true,
            unsafe: true
        }
    })
);
delete config.expand;
module.exports = config;