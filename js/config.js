var config = {
  default: {
    data_service: {
      host: 'localhost',
      port: 8080,
      path: '/data'
    },
  }
}

module.exports.getEnvironment = function() {
    return config[HOST_ENV] || config.default;
}
