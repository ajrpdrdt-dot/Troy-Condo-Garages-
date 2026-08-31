<?php
/**
 * Plugin Name: Live snapshot preview
 * Description: Serves current troycondogarages.com HTML snapshots for local preview.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_action(
	'template_redirect',
	function () {
		if ( is_admin() || wp_doing_ajax() || wp_doing_cron() ) {
			return;
		}

		$path = trim( (string) parse_url( $_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH ), '/' );
		$dir  = WP_CONTENT_DIR . '/live-snapshot';

		$file = ( $path === '' ) ? $dir . '/index.html' : $dir . '/' . $path . '.html';
		if ( ! is_file( $file ) ) {
			$base = basename( $path );
			$alt  = $dir . '/' . $base . '.html';
			if ( is_file( $alt ) ) {
				$file = $alt;
			}
		}

		if ( ! is_file( $file ) ) {
			return;
		}

		$html = file_get_contents( $file );
		if ( false !== $html && false === strpos( $html, 'AW-18398757431' ) ) {
			$gtag = <<<'HTML'
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-18398757431"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-18398757431');
</script>

HTML;
			$html = preg_replace( '/<\/head>/i', $gtag . '</head>', $html, 1 );
		}

		header( 'Content-Type: text/html; charset=UTF-8' );
		echo $html;
		exit;
	},
	0
);
