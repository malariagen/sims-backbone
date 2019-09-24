const webpack = require('webpack');

module.exports = {
    plugins: [new webpack.DefinePlugin({
        'sprocess.env': {
            GOOGLE_API_KEY: JSON.stringify(process.env.GOOGLE_API_KEY),
            CLIENT_ID: JSON.stringify(process.env.CLIENT_ID),
            CLIENT_SECRET: JSON.stringify(process.env.CLIENT_SECRET),
            SIMS_REDIRECT_URI: JSON.stringify(process.env.SIMS_REDIRECT_URI),
            BACKBONE_API_LOCATION: JSON.stringify(process.env.BACKBONE_API_LOCATION),
            ALFRESCO_LOCATION: JSON.stringify(process.env.ALFRESCO_LOCATION),
        }
    })]
}
