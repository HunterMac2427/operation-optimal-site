<?php
/**
 * Template Name: Front Page
 * Homepage for Operation Optimal
 */
get_header();
$img = get_template_directory_uri() . '/assets/images';
?>

    <!-- Hero -->
    <section class="oo-hero" id="home">
        <div class="oo-hero-inner">
            <div class="oo-hero-content">
                <span class="oo-hero-label">Available Now</span>
                <h1 class="oo-hero-title">
                    <span class="oo-title-line">
                        <span class="oo-title-word oo-title-ghost" aria-hidden="true">OPERATION</span>
                        <span class="oo-title-word oo-title-fill oo-title-white">OPERATION</span>
                    </span>
                    <span class="oo-title-line">
                        <span class="oo-title-word oo-title-ghost" aria-hidden="true">OPTIMAL</span>
                        <span class="oo-title-word oo-title-fill oo-title-gold">OPTIMAL</span>
                    </span>
                </h1>
                <p class="oo-hero-subtitle">Health, Wellness and<br><em>Becoming Your Best You</em></p>
                <div class="oo-hero-desc">
                    <p>Nobody's coming to save you.</p>
                    <p>Not your doctor. Not the medical system.</p>
                    <p class="oo-hero-callout">This book is your wake-up call.</p>
                    <p>Reclaim the energy, strength, and vitality you deserve.</p>
                </div>
                <div class="oo-hero-buttons">
                    <a href="https://shop.ingramspark.com/b/084?params=5at6lb7kJLAxMxXRoIiN9BRJYvQ15Y1hGaDCZErTl3f" class="oo-btn-primary" target="_blank">Buy Now &mdash; $24.99</a>
                    <a href="#inside" class="oo-btn-ghost">What's Inside</a>
                </div>
            </div>
            <div class="oo-hero-book">
                <img src="<?php echo $img; ?>/book-cover.png" alt="Operation Optimal book cover by Tomo Marjanovic" width="380" height="570">
            </div>
        </div>
    </section>

    <!-- Divider -->
    <div class="oo-divider"></div>

    <!-- What's Inside -->
    <section class="oo-section oo-inside" id="inside">
        <div class="oo-container">
            <div class="oo-section-header">
                <span class="oo-label">Inside the Book</span>
                <h2>WHAT'S INSIDE</h2>
            </div>
            <div class="oo-cards">
                <div class="oo-card">
                    <div class="oo-card-icon">
                        <svg width="40" height="40" viewBox="0 0 40 40" fill="none"><path d="M20 4C12 4 6 9 6 16c0 10 14 20 14 20s14-10 14-20c0-7-6-12-14-12z" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 18l4 0 2-5 4 10 2-5 4 0" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                    <h3>Own Your Health</h3>
                    <p>Stop being a passive patient. Take radical responsibility for your body, question the system, and make health your number one priority.</p>
                </div>
                <div class="oo-card">
                    <div class="oo-card-icon">
                        <svg width="40" height="40" viewBox="0 0 40 40" fill="none"><path d="M6 34L20 6l14 28" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 20h14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>
                    </div>
                    <h3>Optimize Your Body</h3>
                    <p>Decode your body's signals, master stress and hormones, and build a disciplined whole-body routine with real nutrition and recovery.</p>
                </div>
                <div class="oo-card">
                    <div class="oo-card-icon">
                        <svg width="40" height="40" viewBox="0 0 40 40" fill="none"><path d="M10 4h20v4H10z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/><path d="M14 8v24M26 8v24" stroke="currentColor" stroke-width="2.5"/><path d="M14 16h12M14 24h12" stroke="currentColor" stroke-width="2"/><path d="M8 32h24v4H8z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/></svg>
                    </div>
                    <h3>Build Your Legacy</h3>
                    <p>Transform optimal health into the foundation for wealth, influence, and a legacy that endures through your work, family, and future.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Divider -->
    <div class="oo-divider"></div>

    <!-- About the Author -->
    <section class="oo-section oo-author" id="author">
        <div class="oo-container">
            <div class="oo-author-grid">
                <div class="oo-author-image">
                    <img src="<?php echo $img; ?>/tomo-podcast.jpg" alt="Tomo Marjanovic" width="400" height="533">
                </div>
                <div class="oo-author-text">
                    <span class="oo-label">About the Author</span>
                    <h2>TOMO MARJANOVIC</h2>
                    <p>A first generation American, police veteran, and entrepreneur. After 12 years in law enforcement and receiving the Public Safety Medal of Valor, he founded Aspire Rejuvenation &mdash; a wellness center for hormone therapy and regenerative medicine known for its patient-first approach.</p>
                    <p>Named a Top 100 Healthcare Visionary by IFAH, Tomo challenges industry norms and inspires others to pursue discipline, purpose, and optimal living.</p>
                    <ul class="oo-credentials">
                        <li>Founder, Aspire Rejuvenation</li>
                        <li>12-Year Law Enforcement Veteran</li>
                        <li>Public Safety Medal of Valor</li>
                        <li>Top 100 Healthcare Visionary</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Companion Guide -->
    <section class="oo-section oo-companion" id="companion">
        <div class="oo-container">
            <div class="oo-companion-grid">
                <div class="oo-companion-text">
                    <span class="oo-label">Included with Your Order</span>
                    <h2>THE COMPANION GUIDE</h2>
                    <p>Every order includes the interactive companion workbook &mdash; a hands-on guide to help you live the principles inside Operation Optimal.</p>
                    <ul class="oo-feature-list">
                        <li>Chapter-by-chapter action plans</li>
                        <li>Stress signal checklists and mindset resets</li>
                        <li>Hormone optimization readiness tracker</li>
                        <li>30-day optimization plan with habit tracking</li>
                    </ul>
                    <a href="https://shop.ingramspark.com/b/084?params=5at6lb7kJLAxMxXRoIiN9BRJYvQ15Y1hGaDCZErTl3f" class="oo-btn-primary" target="_blank">Order Now &mdash; Companion Guide Included</a>
                </div>
                <div class="oo-companion-image">
                    <img src="<?php echo $img; ?>/companion-cover.png" alt="Operation Optimal Companion Guide" width="350" height="525">
                </div>
            </div>
        </div>
    </section>

    <!-- Divider -->
    <div class="oo-divider"></div>

    <!-- Final CTA -->
    <section class="oo-section oo-cta" id="buy">
        <div class="oo-container oo-cta-inner">
            <span class="oo-label">Available Now</span>
            <h2 class="oo-cta-heading">
                <span class="oo-line-mask"><span class="oo-line-inner">YOUR OPTIMAL IS</span></span>
                <span class="oo-line-mask"><span class="oo-line-inner">WITHIN REACH</span></span>
            </h2>
            <p>Get the book today, plus the companion guide free. $24.99.</p>
            <div class="oo-cta-buttons">
                <a href="https://shop.ingramspark.com/b/084?params=5at6lb7kJLAxMxXRoIiN9BRJYvQ15Y1hGaDCZErTl3f" class="oo-btn-primary" target="_blank">Buy Now &mdash; $24.99</a>
            </div>
        </div>
    </section>

<?php get_footer(); ?>
