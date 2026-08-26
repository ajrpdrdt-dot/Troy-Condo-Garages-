<?php

namespace SuperBlank\Endpoints;

if (!defined('ABSPATH')) {
    exit;
}

use WP_REST_Response;
use WP_Error;
use SuperBlank\Quiet_Skin;
use Theme_Upgrader;

class HandleStepThree extends BaseEndpoint
{

    public function __construct()
    {
        parent::__construct();
        add_action('wp_ajax_super_blank_step3', [$this, 'handle_step']);
    }

    public function handle_step()
    {
        // Check user permissions first
        if (!$this->checkUserPermissions()) {
            $this->sendAccessForbiddenError();
        }

        // Validate nonce
        if (!$this->validateNonce()) {
            $this->sendInvalidNonceError();
        }

        /**
         * Execution code here
         */
        $use_theme = 'astra';

        // Extract Theme
        $this->installTheme($use_theme);

        // Success
        $this->sendSuccessResponse([
            'success' => true,
            'message' => 'Activating Astra theme...' //'Theme activated successfully'
        ]);
    }

    public function installTheme($theme_slug)
    {

        if (is_multisite()) {

            switch_theme($theme_slug);
            return;
        }

        $default_theme = $theme_slug ? $theme_slug : 'twentytwentyfour';

        $default_theme_object = wp_get_theme($default_theme);

        if (!$default_theme_object->exists()) {

            $skin = new Quiet_Skin();
            $upgrader = new Theme_Upgrader($skin);
            $result = $upgrader->install("https://downloads.wordpress.org/theme/{$default_theme}.zip");

            if (is_wp_error($result)) {

                echo wp_json_encode(new WP_Error('error_data', "Failed to install {$default_theme}: " . $result->get_error_message(), array('status' => 404)));

                wp_die();
            }
        }

        switch_theme($default_theme);

        $themes = wp_get_themes();

        foreach ($themes as $theme_name => $theme) {

            if ($theme_name !== $default_theme) {

                delete_theme($theme_name);
            }
        }
    }
}
