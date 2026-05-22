/* ============================================================
   OPERATION OPTIMAL — Animations
   Premium GSAP + Motion.dev animation system

   Sections:
   1. Plugin registration + CustomEase
   2. ScrollSmoother (desktop only)
   3. Scroll progress bar
   4. Hero pinned sequence
   5. What's Inside pinned card sequence
   6. Author section reveals
   7. Companion guide reveals
   8. CTA reveals
   9. Footer reveal
   10. Nav scroll state
   11. Button micro-interactions (Motion.dev)
   ============================================================ */

(function () {
    'use strict';

    /* ── 1. Register plugins + CustomEase ── */
    gsap.registerPlugin(ScrollTrigger, ScrollSmoother, SplitText, CustomEase, DrawSVGPlugin, ScrambleTextPlugin);

    CustomEase.create('heroReveal', 'M0,0 C0.14,0 0.27,0.12 0.42,0.35 0.56,0.56 0.65,0.78 0.74,0.9 0.82,0.98 0.9,1 1,1');
    CustomEase.create('wipeIn', 'M0,0 C0.25,0.1 0.25,1 1,1');

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ── 2. ScrollSmoother (desktop only) ── */
    var smoother = null;
    if (!reduced && window.innerWidth > 1024) {
        smoother = ScrollSmoother.create({
            wrapper: '#smooth-wrapper',
            content: '#smooth-content',
            smooth: 1.5,
            effects: true
        });
    }

    /* ── 3. Scroll Progress Bar ── */
    gsap.to('.oo-progress-bar', {
        scaleX: 1,
        ease: 'none',
        scrollTrigger: {
            trigger: '#smooth-content',
            start: 'top top',
            end: 'bottom bottom',
            scrub: 0.3
        }
    });

    /* ── Responsive split ── */
    ScrollTrigger.matchMedia({

        /* ============================================================
           DESKTOP — 1025px+
           Full animations, both pins, SplitText char splits
           ============================================================ */
        '(min-width: 1025px)': function () {

            /* ── 4. Hero Pinned Sequence ── */

            // Set book initial state BEFORE building timeline
            gsap.set('.oo-hero-book img', {
                x: 80, rotationY: 8, autoAlpha: 0,
                filter: 'drop-shadow(0 0 0 rgba(0, 0, 0, 0))'
            });

            var heroTl = gsap.timeline({
                scrollTrigger: {
                    trigger: '.oo-hero',
                    start: 'top top',
                    end: '+=150%',
                    pin: true,
                    scrub: 1,
                    anticipatePin: 1
                }
            });

            // Step 1: Label fade up
            heroTl.from('.oo-hero-label', {
                autoAlpha: 0, y: 12, duration: 0.3
            });

            // Step 2: "OPERATION" wipe reveal (white)
            heroTl.to('.oo-title-white', {
                clipPath: 'inset(0 0% 0 0)', duration: 0.6, ease: 'wipeIn'
            }, '+=0.1');

            // Step 3: "OPTIMAL" wipe reveal (gold) — overlaps slightly
            heroTl.to('.oo-title-gold', {
                clipPath: 'inset(0 0% 0 0)', duration: 0.6, ease: 'wipeIn'
            }, '-=0.25');

            // Step 4: Subtitle — SplitText line mask reveal
            var subtitleSplit = new SplitText('.oo-hero-subtitle', {
                type: 'lines',
                linesClass: 'oo-split-line'
            });
            subtitleSplit.lines.forEach(function (line) {
                var wrapper = document.createElement('div');
                wrapper.style.overflow = 'hidden';
                line.parentNode.insertBefore(wrapper, line);
                wrapper.appendChild(line);
            });
            heroTl.from(subtitleSplit.lines, {
                yPercent: 100, duration: 0.5, stagger: 0.08
            }, '-=0.15');

            // Step 5: Callout — beat + fade
            heroTl.from('.oo-hero-callout', {
                autoAlpha: 0, duration: 0.4, y: 10
            }, '+=0.15');

            // Step 6: Supporting text + buttons
            heroTl.from('.oo-hero-desc p:not(.oo-hero-callout)', {
                autoAlpha: 0, y: 12, duration: 0.3
            }, '-=0.15');
            heroTl.from('.oo-hero-buttons', {
                autoAlpha: 0, y: 12, duration: 0.3
            }, '-=0.15');

            // Step 7: Book cover — 3D entrance
            heroTl.to('.oo-hero-book img', {
                autoAlpha: 1, x: 0, rotationY: 0,
                filter: 'drop-shadow(0 25px 50px rgba(0, 0, 0, 0.6))',
                duration: 1, ease: 'heroReveal',
                onStart: function () {
                    gsap.set('.oo-hero-book img', { willChange: 'transform' });
                },
                onComplete: function () {
                    gsap.set('.oo-hero-book img', { willChange: 'auto' });
                }
            }, '-=0.5');


            /* ── 5. What's Inside — Graceful Entrance ── */

            var insideTl = gsap.timeline({
                defaults: { ease: 'power2.out' },
                scrollTrigger: {
                    trigger: '.oo-inside',
                    start: 'top 82%',
                    once: true
                }
            });

            insideTl.from('.oo-inside .oo-label', {
                autoAlpha: 0, y: 8, duration: 0.3
            });

            var insideHeadingSplit = new SplitText('.oo-inside .oo-section-header h2', {
                type: 'chars',
                charsClass: 'oo-split-char'
            });
            insideTl.from(insideHeadingSplit.chars, {
                autoAlpha: 0, y: 12, duration: 0.3, stagger: 0.015
            }, '-=0.15');

            // Cards — all three rise together with stagger
            insideTl.from('.oo-card', {
                autoAlpha: 0, y: 20, duration: 0.5, stagger: 0.1
            }, '-=0.1');

            // DrawSVG icons fire together after cards land
            var allIconPaths = document.querySelectorAll('.oo-card svg path, .oo-card svg rect, .oo-card svg line');
            if (allIconPaths.length) {
                insideTl.from(allIconPaths, {
                    drawSVG: '0%', duration: 0.4, stagger: 0.03
                }, '-=0.3');
            }


            /* ── 6. Author Section ── */
            gsap.set('.oo-author-image img', { scale: 1.05 });

            var authorTl = gsap.timeline({
                defaults: { ease: 'power2.out' },
                scrollTrigger: {
                    trigger: '.oo-author',
                    start: 'top 80%',
                    once: true
                }
            });

            authorTl.to('.oo-author-image img', {
                clipPath: 'inset(0% 0% 0% 0%)',
                scale: 1, duration: 0.7, ease: 'wipeIn'
            });

            authorTl.from('.oo-author-text .oo-label', {
                autoAlpha: 0, y: 8, duration: 0.25
            }, '-=0.5');

            var authorHeadingSplit = new SplitText('.oo-author-text h2', {
                type: 'chars',
                charsClass: 'oo-split-char'
            });
            authorTl.from(authorHeadingSplit.chars, {
                autoAlpha: 0, y: 10, duration: 0.25, stagger: 0.015
            }, '-=0.2');

            var authorBioSplit = new SplitText('.oo-author-text p', {
                type: 'lines',
                linesClass: 'oo-split-line'
            });
            authorTl.from(authorBioSplit.lines, {
                autoAlpha: 0, y: 10, duration: 0.3, stagger: 0.04
            }, '-=0.1');

            var credentialItems = gsap.utils.toArray('.oo-credentials li');
            credentialItems.forEach(function (li, i) {
                var originalText = li.textContent;
                li.textContent = '';
                authorTl.to(li, {
                    duration: 0.4,
                    scrambleText: {
                        text: originalText,
                        chars: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                        speed: 0.6
                    }
                }, i === 0 ? '-=0.05' : '-=0.2');
            });


            /* ── 7. Companion Guide ── */
            var companionTl = gsap.timeline({
                defaults: { ease: 'power2.out' },
                scrollTrigger: {
                    trigger: '.oo-companion',
                    start: 'top 80%',
                    once: true
                }
            });

            companionTl.from('.oo-companion-text .oo-label', {
                autoAlpha: 0, y: 8, duration: 0.25
            });

            var companionHeadingSplit = new SplitText('.oo-companion-text h2', {
                type: 'chars',
                charsClass: 'oo-split-char'
            });
            companionTl.from(companionHeadingSplit.chars, {
                autoAlpha: 0, y: 10, duration: 0.25, stagger: 0.015
            }, '-=0.1');

            var companionDescSplit = new SplitText('.oo-companion-text p', {
                type: 'lines',
                linesClass: 'oo-split-line'
            });
            companionTl.from(companionDescSplit.lines, {
                autoAlpha: 0, y: 10, duration: 0.3, stagger: 0.04
            }, '-=0.1');

            companionTl.from('.oo-feature-list li', {
                autoAlpha: 0, y: 8, duration: 0.25, stagger: 0.06
            }, '-=0.15');

            companionTl.from('.oo-companion-text .oo-btn-primary', {
                autoAlpha: 0, y: 8, duration: 0.25
            }, '-=0.1');

            companionTl.from('.oo-companion-image img', {
                autoAlpha: 0, y: 25, duration: 0.5
            }, '-=0.6');


            /* ── 8. CTA Section ── */
            var ctaTl = gsap.timeline({
                defaults: { ease: 'power2.out' },
                scrollTrigger: {
                    trigger: '.oo-cta',
                    start: 'top 80%',
                    once: true
                }
            });

            ctaTl.from('.oo-cta .oo-label', {
                autoAlpha: 0, y: 8, duration: 0.25
            });

            ctaTl.from('.oo-line-inner', {
                yPercent: 100, duration: 0.4, stagger: 0.08, ease: 'power3.out'
            }, '-=0.1');

            gsap.fromTo('.oo-cta-heading', {
                '--glow-scale': 0.5
            }, {
                '--glow-scale': 1,
                duration: 3,
                ease: 'sine.inOut',
                yoyo: true,
                repeat: -1,
                delay: 1
            });

            ctaTl.from('.oo-cta p', {
                autoAlpha: 0, y: 8, duration: 0.3
            }, '-=0.15');

            ctaTl.from('.oo-cta-buttons a', {
                autoAlpha: 0, y: 8, duration: 0.25, stagger: 0.08
            }, '-=0.15');


            /* ── 9. Footer ── */
            gsap.from('.oo-footer-inner > *', {
                autoAlpha: 0, y: 10, duration: 0.35, stagger: 0.06,
                scrollTrigger: {
                    trigger: '.oo-footer',
                    start: 'top 90%',
                    once: true
                }
            });

        },

        /* ============================================================
           MOBILE — 1024px and below
           Fast, clean fades. No pins, no ScrollSmoother,
           no SplitText, no ScrambleText, no DrawSVG.
           Only GSAP core + ScrollTrigger.
           ============================================================ */
        '(max-width: 1024px)': function () {

            /* ── Helper: simple once-reveal ── */
            function reveal(sel, vars) {
                var o = { autoAlpha: 0, y: 20, duration: 0.5, ease: 'power2.out' };
                for (var k in vars) o[k] = vars[k];
                var trig = o.trigger || sel; delete o.trigger;
                o.scrollTrigger = { trigger: trig, start: 'top 85%', once: true };
                gsap.from(sel, o);
            }

            /* ── Hero — quick load entrance ── */
            var mobileHero = gsap.timeline({ delay: 0.15 });
            mobileHero.from('.oo-hero-label', { autoAlpha: 0, y: 10, duration: 0.3 });
            mobileHero.from('.oo-hero-title', { autoAlpha: 0, y: 15, duration: 0.4 }, '-=0.15');
            mobileHero.from('.oo-hero-subtitle', { autoAlpha: 0, y: 10, duration: 0.3 }, '-=0.15');
            mobileHero.from('.oo-hero-desc', { autoAlpha: 0, y: 10, duration: 0.3 }, '-=0.1');
            mobileHero.from('.oo-hero-buttons', { autoAlpha: 0, y: 10, duration: 0.3 }, '-=0.1');

            /* ── Scroll reveals ── */
            reveal('.oo-card', { stagger: 0.1, trigger: '.oo-cards' });
            reveal('.oo-author-image', { y: 0, duration: 0.6 });
            reveal('.oo-author-text > *', { stagger: 0.06, trigger: '.oo-author-text' });
            reveal('.oo-companion-text > *', { stagger: 0.06, trigger: '.oo-companion-text' });
            reveal('.oo-companion-image img', { trigger: '.oo-companion-image' });

            /* ── CTA ── */
            reveal('.oo-cta .oo-label', { trigger: '.oo-cta' });
            reveal('.oo-cta-heading', { trigger: '.oo-cta', y: 15 });
            reveal('.oo-cta p', { trigger: '.oo-cta' });
            reveal('.oo-cta-buttons a', { stagger: 0.08, trigger: '.oo-cta-buttons' });

            /* ── Footer ── */
            reveal('.oo-footer-inner > *', { stagger: 0.06, y: 10, trigger: '.oo-footer' });
        }
    });


    /* ── 10. Nav scroll state (all breakpoints) ── */
    ScrollTrigger.create({
        trigger: '.oo-hero',
        start: 'top top',
        end: '90% top',
        onLeave: function () { document.querySelector('.oo-nav').classList.add('scrolled'); },
        onEnterBack: function () { document.querySelector('.oo-nav').classList.remove('scrolled'); }
    });


    /* ── 11. Button micro-interactions — Motion.dev (all breakpoints) ── */
    if (!reduced && typeof Motion !== 'undefined') {
        var hover = Motion.hover;
        var press = Motion.press;
        var animate = Motion.animate;

        document.querySelectorAll('.oo-btn-primary, .oo-btn-ghost, .oo-nav-cta').forEach(function (btn) {
            hover(btn, function () {
                animate(btn, { scale: 1.03 }, { type: 'spring', stiffness: 400, damping: 15 });
                return function () {
                    animate(btn, { scale: 1 }, { type: 'spring', stiffness: 400, damping: 15 });
                };
            });

            press(btn, function () {
                animate(btn, { scale: 0.97 });
                return function () {
                    animate(btn, { scale: 1 }, { type: 'spring', bounce: 0.3 });
                };
            });
        });
    }

})();
