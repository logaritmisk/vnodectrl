<?php
/**
 * Implementation of hook_hosting_feature().
 */
function vnodectrl_hosting_feature() {
  $features['vnodectrl'] = array(
  // title to display in form
    'title' => t('Vnodectrl'),
  // description
    'description' => t('Let\'s you create new cloud server instances through libcloud'),
  // initial status ( HOSTING_FEATURE_DISABLED, HOSTING_FEATURE_ENABLED, HOSTING_FEATURE_REQUIRED )
    'status' => HOSTING_FEATURE_DISABLED,
  // module to enable/disable alongside feature
    'module' => 'vnodectrl',
  // associate with a specific node type.
    'node' => 'server',
  // which group to display in ( null , experimental )
    'group' => 'experimental'
  );
  return $features;
}