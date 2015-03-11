var gulp = require('gulp'),
    stylus = require('gulp-stylus'),
    uglify = require('gulp-uglify'),
    concat = require('gulp-concat'),
    imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant');

var paths = {
    scripts: [
        './bower_components/jquery/dist/jquery.min.js',
        './js/card.js',
        './js/app.js'
    ],
    stylus: './stylus/**',
    images: '../images-src/**'
};

gulp.task('js', function() {
    gulp.src(paths.scripts)
        .pipe(uglify())
        .pipe(concat('global.min.js'))
        .pipe(gulp.dest('../js'))
});

gulp.task('stylus', function () {
  gulp.src('./stylus/global.styl')
    .pipe(stylus())
    .pipe(gulp.dest('../css'))
});

gulp.task('images', function () {
    return gulp.src('../images-src/**')
        .pipe(imagemin({
            progressive: true,
            svgoPlugins: [{removeViewBox: false}],
            use: [pngquant()]
        }))
        .pipe(gulp.dest('../images-dist'));
});

gulp.task('watch', function() {
    gulp.watch(paths.scripts, ['js']);
    gulp.watch(paths.stylus, ['stylus']);
    gulp.watch(paths.images, ['images']);
});

gulp.task('default', ['stylus', 'js', 'images']);
