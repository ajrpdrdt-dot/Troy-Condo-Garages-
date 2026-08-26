<?php

namespace SuperBlank\Endpoints;

use WP_REST_Response;
use WP_Error;

if (!defined('ABSPATH')) {
    exit;
}

abstract class BaseEndpoint
{
    /**
     * Constructor - should be called by child classes
     */
    public function __construct()
    {
        // Child classes should call parent::__construct() and add their own hooks
    }

    /**
     * Check if current user has admin or network admin capabilities
     * 
     * @return bool
     */
    protected function checkUserPermissions()
    {
        // Check if user is logged in
        if (!is_user_logged_in()) {
            return false;
        }

        // Check if user is admin or network admin
        $user = wp_get_current_user();

        // For single site
        if (!is_multisite()) {
            return user_can($user, 'manage_options');
        }

        // For multisite
        return user_can($user, 'manage_network') || user_can($user, 'manage_options');
    }

    /**
     * Send access forbidden error response
     */
    protected function sendAccessForbiddenError()
    {
        echo wp_json_encode(new WP_Error(
            'access_forbidden',
            'Access forbidden. Administrator privileges required.',
            array('status' => 403)
        ));
        wp_die();
    }

    /**
     * Validate nonce for the request
     * 
     * @param string $nonce_action The nonce action to verify
     * @return bool
     */
    protected function validateNonce($nonce_action = 'install_super_blank')
    {
        // Check if POST nonce is not empty
        if (empty($_POST['nonce'])) {
            return false;
        }

        $nonce = sanitize_key(wp_unslash($_POST['nonce']));
        return wp_verify_nonce($nonce, $nonce_action);
    }

    /**
     * Send invalid nonce error response
     */
    protected function sendInvalidNonceError()
    {
        echo wp_json_encode(new WP_Error(
            'error_data',
            'Invalid nonce',
            array('status' => 403)
        ));
        wp_die();
    }

    /**
     * Send success response
     * 
     * @param array $data Response data
     * @param int $status_code HTTP status code
     */
    protected function sendSuccessResponse($data = [], $status_code = 200)
    {
        echo wp_json_encode(new WP_REST_Response($data, $status_code));
        wp_die();
    }

    /**
     * Send error response
     * 
     * @param string $code Error code
     * @param string $message Error message
     * @param int $status_code HTTP status code
     */
    protected function sendErrorResponse($code, $message, $status_code = 400)
    {
        echo wp_json_encode(new WP_Error($code, $message, array('status' => $status_code)));
        wp_die();
    }

    /**
     * Abstract method that child classes must implement
     * This is the main handler method for each step
     */
    abstract public function handle_step();
}
