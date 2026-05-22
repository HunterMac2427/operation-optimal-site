<?php
/**
 * Operation Optimal Theme Functions
 */

function oo_theme_setup() {
    add_theme_support('title-tag');
    add_theme_support('custom-logo');
    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption'));
    add_theme_support('post-thumbnails');
}
add_action('after_setup_theme', 'oo_theme_setup');

function oo_enqueue_assets() {
    $uri = get_template_directory_uri();

    // Google Fonts
    wp_enqueue_style('oo-fonts', 'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap', array(), null);

    // Main stylesheet
    wp_enqueue_style('oo-main', $uri . '/assets/css/main.css', array('oo-fonts'), '2');

    // GSAP + ScrollTrigger (CDN)
    wp_enqueue_script('gsap', 'https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js', array(), '3.14', true);
    wp_enqueue_script('gsap-st', 'https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js', array('gsap'), '3.14', true);

    // GSAP Premium (self-hosted)
    wp_enqueue_script('gsap-smoother', $uri . '/assets/js/ScrollSmoother.min.js', array('gsap', 'gsap-st'), '3.14', true);
    wp_enqueue_script('gsap-split', $uri . '/assets/js/SplitText.min.js', array('gsap'), '3.14', true);
    wp_enqueue_script('gsap-ease', $uri . '/assets/js/CustomEase.min.js', array('gsap'), '3.14', true);
    wp_enqueue_script('gsap-draw', $uri . '/assets/js/DrawSVGPlugin.min.js', array('gsap'), '3.14', true);
    wp_enqueue_script('gsap-scramble', $uri . '/assets/js/ScrambleTextPlugin.min.js', array('gsap'), '3.14', true);

    // Motion.dev (CDN)
    wp_enqueue_script('motion', 'https://cdn.jsdelivr.net/npm/motion@latest/dist/motion.js', array(), null, true);

    // Site animations
    wp_enqueue_script('oo-animations', $uri . '/assets/js/animations.js', array('gsap', 'gsap-st', 'gsap-smoother', 'gsap-split', 'gsap-ease', 'motion'), '2', true);
}
add_action('wp_enqueue_scripts', 'oo_enqueue_assets');

// Remove emoji scripts
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('wp_head', 'wp_generator');

// Custom page title
function oo_custom_title($title) {
    if (is_front_page()) {
        return 'Operation Optimal — Health, Wellness, and Becoming Your Best You | Tomo Marjanovic';
    }
    return $title;
}
add_filter('pre_get_document_title', 'oo_custom_title');
