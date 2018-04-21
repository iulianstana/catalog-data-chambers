var webpack = require('webpack')
module.exports = {
    plugins: [
        new webpack.DefinePlugin({
            HOST_ENV: JSON.stringify(process.env.ENV)
        })
    ]
}
