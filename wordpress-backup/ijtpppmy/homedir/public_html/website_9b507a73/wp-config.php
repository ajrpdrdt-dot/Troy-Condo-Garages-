<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * Localized language
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** Database settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', 'troy_local' );

/** Database username */
define( 'DB_USER', 'root' );

/** Database password */
define( 'DB_PASSWORD', '' );

/** Database hostname */
define( 'DB_HOST', '127.0.0.1' );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',          'AKR]Xc+|_0e`SJ!W:Z^wEe2Co&D39d^|jwu6bNv*{#zm*Gz=!I{}$heJ8Cy~Pga_' );
define( 'SECURE_AUTH_KEY',   '%O@X*5,W1E_e<hfNu6kyn&=rQPYt9`mLmJA~[6<Ah{kok/3 p<k6yN,F]C-dj)>q' );
define( 'LOGGED_IN_KEY',     'G!_5#9v5QXdYu@V0y#<pOc#[:%5nX}}#XPDY7/mO(V88:iy#;[3tVG.1Ld?Fu.zg' );
define( 'NONCE_KEY',         '|qjMW-Sv}1t|F!1cr*eJg!x=63c#/wneRVXCn4/r~>M^}Z6+B7eX0L6f.r J|o2/' );
define( 'AUTH_SALT',         'y}^[)P^}~Sp5wMCXmDBo;|;EncC{ >V&_5_7EB>njXpHDU~gRJn~Uhd!O|g4jd=u' );
define( 'SECURE_AUTH_SALT',  'A_M/Z@jA9s(9Hs.hRzgV+~6U41JJb5N[w`0.>AX6_ 9@U|$S=,[=^~>xByuaWoMV' );
define( 'LOGGED_IN_SALT',    ' _.uhEISWjr.Y{4T+Fo=f3ZuX4eHRTpiKP<NYBtr9r2h]zTqjl}M[W*`h2342^Vd' );
define( 'NONCE_SALT',        'A?YXK.Ii3=Cx&|N+cH]ul=gG.Hsg{_]IW@bO]al|.)/w@UTc.`,os^ncMH,.&C8t' );
define( 'WP_CACHE_KEY_SALT', 'OhSiwkNJe,fC?D[l]CN|wJ9DUR|c+Qqj-7U9[$1 BW2b2~WY>b=C1+oT(:M6 @AE' );


/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'hJ6_';


/* Add any custom values between this line and the "stop editing" line. */

define( 'WP_HOME', 'http://127.0.0.1:8080' );
define( 'WP_SITEURL', 'http://127.0.0.1:8080' );
define( 'DISABLE_WP_CRON', true );
define( 'WP_HTTP_BLOCK_EXTERNAL', true );
define( 'WP_MEMORY_LIMIT', '512M' );



/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
if ( ! defined( 'WP_DEBUG' ) ) {
	define( 'WP_DEBUG', false );
}

define( 'AUTOSAVE_INTERVAL', 300 );
define( 'WP_POST_REVISIONS', 20 );
define( 'EMPTY_TRASH_DAYS', 7 );
define( 'WP_AUTO_UPDATE_CORE', true );
define( 'WP_CRON_LOCK_TIMEOUT', 120 );
/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
// Settings modified by hosting provider
define('DISALLOW_FILE_EDIT', true);
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
