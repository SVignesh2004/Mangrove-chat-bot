module.exports = {
  // Use explicit requires to ensure PostCSS resolves the correct packages
  // relative to this project folder.
  plugins: [
    require('@tailwindcss/postcss'),
    require('autoprefixer'),
  ],
};
