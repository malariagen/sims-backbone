// Karma configuration file, see link for more information
// https://karma-runner.github.io/1.0/config/configuration-file.html

module.exports = function (config) {
    config.set({
        basePath: '',
        frameworks: ['jasmine', '@angular-devkit/build-angular'],
        plugins: [
            require('karma-jasmine'),
            require('karma-chrome-launcher'),
            require('karma-jasmine-html-reporter'),
            require('karma-coverage-istanbul-reporter'),
            require('@angular-devkit/build-angular/plugins/karma')
        ],
        client: {
            clearContext: false // leave Jasmine Spec Runner output visible in browser
        },
        coverageIstanbulReporter: {
            dir: require('path').join(__dirname, '../../../coverage/malariagen/sims'),
            reports: ['html', 'lcovonly'],
            fixWebpackSourcePaths: true
        },
        reporters: ['progress', 'kjhtml'],
        port: 9876,
        colors: true,
        logLevel: config.LOG_INFO,
        autoWatch: true,
        browsers: [
            'ChromeHeadless',
            'ChromeNoSandbox',
            'Chrome'
        ],
        customLaunchers: {
            ChromeNoSandbox: {
                base: 'ChromeHeadless',
                flags: [
                    '--no-sandbox',
                    '--disable-gpu'
                ]
            }
        },
        singleRun: false,
        /** * maximum number of tries a browser will attempt in the case of a disconnection */
        browserDisconnectTolerance: 2,
        /** * How long will Karma wait for a message from a browser before disconnecting from it (in
         * ms). */
        browserNoActivityTimeout: 50000,
    });
};
