<?php
/**
 * Plugin Name: Google Ads gtag (AW-18398757431)
 * Description: Adds Google Ads conversion tracking tag to site header.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Output Google Ads gtag snippet in the document head.
 */
function troy_condo_garages_google_ads_gtag() {
	?>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18398757431"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-18398757431');
</script>
	<?php
}
add_action( 'wp_head', 'troy_condo_garages_google_ads_gtag', 1 );
