<?php

namespace SuperBlank\Endpoints;

if (!defined('ABSPATH')) {
    exit;
}

use WP_REST_Response;
use WP_Error;

class HandleStepOneTwo extends BaseEndpoint
{

    public function __construct()
    {
        parent::__construct();
        add_action('wp_ajax_super_blank_step1_2', [$this, 'handle_step']);
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

        $this->deleteOptions();

        $this->deletePostsData();

        // Success
        $this->sendSuccessResponse([
            'success' => true,
            'message' => 'Deep cleanup...'
        ]);
    }

    public function deleteOptions()
    {

        $options = [
            'site_logo',
            'site_icon'
        ];

        superBlankDeleteExactOptions($options);

        $patterns = [
            'astra%',
            '%astra',
            '%astra%',
            'elementor%',
            '%elementor',
            '%elementor%',
            'wpforms%',
            '%wpforms',
            '%wpforms%',
            'woocommerce%',
            '%woocommerce',
            '%woocommerce%',
        ];

        superBlankDeleteOptionsByPattern($patterns);
    }

    public function deletePostsData()
    {

        // Delete attachments
        superBlankCleanAttachmentsWithFiles();

        // Delete posts
        superBlankCleanPosts();

        // Delete specific posts
        superBlankCleanSpecificPosts();

        // Set permalinks
        superBlankSetPermalinkStructure('/%postname%/');

        // Delete all categories and tags
        superBlankCleanTerms();

        // Delete all comments
        superBlankCleanComments();

        // Delete Termmeta trash
        superBlankDeleteLostRecordsTermmeta();

        // Delete Postmeta trash
        superBlankDeleteLostRecordsPostmeta();
    }
}
