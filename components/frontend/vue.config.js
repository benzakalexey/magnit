const path = require('path');

const dotenv = require('dotenv')
dotenv.config()

module.exports = {
    pluginOptions: {
        i18n: {
            locale: 'ru',
            fallbackLocale: 'ru',
            localeDir: 'locales',
            enableInSFC: false
        }
    },
    chainWebpack: config => {
        // Remove prefetch plugin and that's it!
        config.plugins.delete('prefetch');
    },
    configureWebpack: {
        resolve: {
            alias: {
                '@themeConfig': path.resolve(__dirname, 'theme.config.js'),                
            }
        }
    }
};
