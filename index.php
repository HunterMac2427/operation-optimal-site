<?php
/**
 * Main template fallback — WordPress requires this file.
 */
get_header();
?>
<div class="oo-container" style="padding: 120px 24px 60px;">
    <?php if (have_posts()) : while (have_posts()) : the_post(); ?>
        <article>
            <h1><?php the_title(); ?></h1>
            <?php the_content(); ?>
        </article>
    <?php endwhile; endif; ?>
</div>
<?php get_footer(); ?>
