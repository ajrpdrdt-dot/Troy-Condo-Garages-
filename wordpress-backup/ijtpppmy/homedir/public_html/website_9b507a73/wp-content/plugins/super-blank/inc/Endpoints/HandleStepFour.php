<?php

namespace SuperBlank\Endpoints;

if (!defined('ABSPATH')) {
    exit;
}

use WP_REST_Response;
use WP_Error;
use SuperBlank\Quiet_Skin;
use Plugin_Upgrader;

class HandleStepFour extends BaseEndpoint
{

    public function __construct()
    {
        parent::__construct();
        add_action('wp_ajax_super_blank_step4', [$this, 'handle_step']);
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
        $this->installWpforms();

        // Import forms
        $this->wpformsImportForms();

        // Success
        $this->sendSuccessResponse([
            'success' => true,
            'message' => 'Installing WP Forms plugin...'
        ]);
    }

    public function installWpforms()
    {

        if(is_multisite()) return;

        include_once(ABSPATH . 'wp-admin/includes/plugin-install.php');
        include_once(ABSPATH . 'wp-admin/includes/class-wp-upgrader.php');
        include_once(ABSPATH . 'wp-admin/includes/misc.php');
        include_once(ABSPATH . 'wp-admin/includes/file.php');

        $plugin_slug = 'wpforms-lite';
        $plugin = $plugin_slug . '/wpforms.php';

        if (!is_plugin_active($plugin)) {

            $api = plugins_api('plugin_information', array('slug' => $plugin_slug));

            if (is_wp_error($api)) {

                echo wp_json_encode(new WP_Error('error_data', 'Failed to get WPForms plugin: ' . $api->get_error_message(), array('status' => 404)));

                wp_die();
            }

            $upgrader = new Plugin_Upgrader(new Quiet_Skin());
            $result = $upgrader->install($api->download_link);

            if (is_wp_error($result)) {

                echo wp_json_encode(new WP_Error('error_data', 'Failed to install WPForms plugin: ' . $result->get_error_message(), array('status' => 404)));

                wp_die();
            }

            activate_plugin($plugin);
        }
    }

    public function wpformsImportForms()
    {

        $wpFormsFile = SUPER_BLANK_PLUGIN_PATH . 'settings/wpforms.json';

        if (!file_exists($wpFormsFile)) return;

        if (class_exists('WPForms\Admin\Tools\Views\Import')) {

            $importer = new \WPForms\Admin\Tools\Views\Import();
            $importer->import_forms($wpFormsFile);
        }
    }
}
