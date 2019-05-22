const webpack = require('webpack');

module.exports = {
    plugins: [new webpack.DefinePlugin({
        'sprocess.env': {
            GOOGLE_API_KEY: JSON.stringify(process.env.GOOGLE_API_KEY),
            CLIENT_ID: JSON.stringify(process.env.CLIENT_ID),
            CLIENT_SECRET: JSON.stringify(process.env.CLIENT_SECRET),
        }
    })]
}
