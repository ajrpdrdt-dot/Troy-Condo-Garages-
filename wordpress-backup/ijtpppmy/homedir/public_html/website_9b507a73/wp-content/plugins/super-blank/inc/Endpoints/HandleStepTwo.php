<?php

namespace SuperBlank\Endpoints;

if (!defined('ABSPATH')) {
    exit;
}

use WP_REST_Response;
use WP_Error;

class HandleStepTwo extends BaseEndpoint
{

    public function __construct()
    {
        parent::__construct();
        add_action('wp_ajax_super_blank_step2', [$this, 'handle_step']);
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

        // Download package
        $this->deleteInactivePlugins();

        // Success
        $this->sendSuccessResponse([
            'success' => true,
            'message' => 'Getting design ready...'
        ]);
    }

    public function deleteInactivePlugins()
    {

        if(is_multisite()) return;

        $all_plugins = get_plugins();
        $active_plugins = get_option('active_plugins');

        foreach ($all_plugins as $plugin_path => $plugin_data) {

            if (!in_array($plugin_path, $active_plugins)) {

                $plugin_dir = WP_PLUGIN_DIR . '/' . dirname($plugin_path);
                $plugin_file = WP_PLUGIN_DIR . '/' . $plugin_path;

                if (dirname($plugin_path) === '.') {

                    wp_delete_file($plugin_file);
                } else {

                    superBlankDeleteDirectory($plugin_dir);
                }
            }
        }

        // Flush caches (prevent plugin folder not found errors)
        wp_clean_plugins_cache(true);
        wp_cache_flush();
    }
}
