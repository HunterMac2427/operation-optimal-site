<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php if (is_front_page()) : ?>
    <meta name="description" content="Operation Optimal by Tomo Marjanovic. Break free from a medical system designed for dependency. Reclaim your health, strength, and vitality on your own terms.">
    <link rel="canonical" href="https://operationoptimal.com/">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Operation Optimal — Health, Wellness, and Becoming Your Best You">
    <meta property="og:description" content="Nobody's coming to save you. This book is your wake-up call. Reclaim the energy, strength, and vitality you deserve.">
    <meta property="og:url" content="https://operationoptimal.com/">
    <meta property="og:image" content="<?php echo get_template_directory_uri(); ?>/assets/images/book-cover.png">
    <meta property="og:site_name" content="Operation Optimal">
    <meta property="og:locale" content="en_US">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Operation Optimal — Health, Wellness, and Becoming Your Best You">
    <meta name="twitter:description" content="Nobody's coming to save you. This book is your wake-up call. Reclaim the energy, strength, and vitality you deserve.">
    <meta name="twitter:image" content="<?php echo get_template_directory_uri(); ?>/assets/images/book-cover.png">
    <?php endif; ?>
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>

    <!-- Preorder Banner -->
    <div class="oo-banner">
        <span class="oo-banner-text">Available Now</span>
        <span class="oo-banner-sep">&mdash;</span>
        <a href="https://shop.ingramspark.com/b/084?params=5at6lb7kJLAxMxXRoIiN9BRJYvQ15Y1hGaDCZErTl3f" class="oo-banner-link">Buy Now &mdash; $24.99</a>
    </div>

    <!-- Nav -->
    <nav class="oo-nav">
        <a href="<?php echo home_url(); ?>" class="oo-nav-brand">OPERATION OPTIMAL</a>
        <div class="oo-nav-links">
            <a href="#inside">Inside</a>
            <a href="#author">Author</a>
            <a href="https://shop.ingramspark.com/b/084?params=5at6lb7kJLAxMxXRoIiN9BRJYvQ15Y1hGaDCZErTl3f" class="oo-nav-cta" target="_blank">Order Now</a>
        </div>
    </nav>

    <!-- Scroll Progress Bar -->
    <div class="oo-progress-bar"></div>

    <!-- ScrollSmoother Wrapper -->
    <div id="smooth-wrapper">
    <div id="smooth-content">
