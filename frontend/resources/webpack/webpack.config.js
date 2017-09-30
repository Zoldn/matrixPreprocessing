const webpack = require('webpack');
const path = require('path');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const rules = require('./rules');
const NODE_ENV = process.env.NODE_ENV || 'development';
const resolve = require('./resolve');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const isProduction = process.env.NODE_ENV === 'production';
const local = require('./local');

console.log(`--${NODE_ENV}`);
const vendor = [
    'vue', 'vue-router', 'vuex',
    'axios', 'lodash', 'jquery',
    'chart.js', 'file-saver'
];
module.exports = {
    entry: {
        index: './src/index.js',
        vendor: vendor
    },
    module: {
        rules: rules
    },
    plugins: [
        new webpack.optimize.CommonsChunkPlugin({
            names: ['vendor', 'common']
        }),
        new webpack.NoEmitOnErrorsPlugin(),
        new ExtractTextPlugin({filename: '[name].css', allChunks: true, disable: NODE_ENV === 'watch'}),
        new webpack.DefinePlugin({
            NODE_ENV: JSON.stringify(NODE_ENV)
        }),
        new CleanWebpackPlugin([resolve('../web/build'), resolve('../web/bundle')],
            {root: resolve('../')}),
        new HtmlWebpackPlugin({
            filename: resolve('index.html'),
            template: 'webpack/index.ejs',
            livereload: isProduction || !local.livereload ? '' : '<script src="http://localhost:35729/livereload.js"></script>',
            inject: 'body',
            hash: true
        })
    ],
    resolve: {
        extensions: ['.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': resolve('src')
        }
    },
    resolveLoader: {
        modules: ['node_modules'],
        moduleExtensions: ['-loader'],
        extensions: ['.js']
    },
    expand: function (key, value) {
        this[key] = value;
        return this;
    }
};