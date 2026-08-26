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

		header( 'Content-Type: text/html; charset=UTF-8' );
		readfile( $file );
		exit;
	},
	0
);
