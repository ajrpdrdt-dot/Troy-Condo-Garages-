<?php

namespace SuperBlank\Endpoints;

if (!defined('ABSPATH')) {
    exit;
}

use WP_REST_Response;
use WP_Error;
use SuperBlank\Quiet_Skin;
use Plugin_Upgrader;

class HandleStepFive extends BaseEndpoint
{

    public function __construct()
    {
        parent::__construct();
        add_action('wp_ajax_super_blank_step5', [$this, 'handle_step']);
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

        // Install plugin
        $this->install_elementor();

        // Success
        $this->sendSuccessResponse([
            'success' => true,
            'message' => 'Installing Elementor plugin...'
        ]);
    }

    public function install_elementor()
    {

        if(is_multisite()) return;

        include_once(ABSPATH . 'wp-admin/includes/plugin-install.php');
        include_once(ABSPATH . 'wp-admin/includes/class-wp-upgrader.php');
        include_once(ABSPATH . 'wp-admin/includes/misc.php');
        include_once(ABSPATH . 'wp-admin/includes/file.php');

        $plugin_slug = 'elementor';
        $plugin = $plugin_slug . '/elementor.php';

        if (!is_plugin_active($plugin)) {
            $api = plugins_api('plugin_information', array('slug' => $plugin_slug));

            if (is_wp_error($api)) {

                echo wp_json_encode(new WP_Error('error_data', 'Failed to get Elementor plugin: ' . $api->get_error_message(), array('status' => 404)));
                wp_die();
            }

            $upgrader = new Plugin_Upgrader(new Quiet_Skin());
            $result = $upgrader->install($api->download_link);

            if (is_wp_error($result)) {

                echo wp_json_encode(new WP_Error('error_data', 'Failed to install Elementor plugin: ' . $result->get_error_message(), array('status' => 404)));
                wp_die();
            }

            activate_plugin($plugin);
        }
    }
}
