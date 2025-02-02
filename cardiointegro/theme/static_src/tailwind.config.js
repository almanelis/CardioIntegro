module.exports = {
    content: [
        './templates/**/*.html',
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',
        './node_modules/flowbite/**/*.js',
    ],
    theme: {
        colors: {
            salad: '#99D98C',
            sea: '#34A0A4',
            deepsea: '#0B1725',
        },
        extend: {
            fontFamily: {
                'open-sans': ['Open Sans', 'sans-serif']
            },
        },
        backdropBlur: {
            full: '100px',
          },
        // boxShadow: {
        //     'sea': '6.5px -6.5px 12px 0px rgba(12, 138, 173, 0.7v)',
        //   }
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('flowbite/plugin'),
    ],
};
