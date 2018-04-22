var config = {
    default: {
        data_service: {
            host: 'localhost',
            port: 5005,
            path: '/items'
        },
    }
}

module.exports.getEnvironment = function() {
    return config[HOST_ENV] || config.default;
}
