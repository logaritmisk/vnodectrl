<?php
// $Id$

/**
 * Implementation of hook_drush_command().
 */
function sqlinit_drush_command() {
  $items['sql-init'] = array(
    'bootstrap' => DRUSH_BOOTSTRAP_DRUPAL_CONFIGURATION,
    'callback' => 'sqlinit_init_database',
    'description' => 'Create a database and the user based on the preferences in the database file',
  );

  return $items;
}

/**
 * Create a database and a user.
 * this currently only works with mysql.
 */
function sqlinit_init_database() {
  global $db_url;
  $root_url = 'mysql://root@localhost';
  // Connect as root.
  $root = drush_convert_db_from_db_url($root_url);
  mysql_connect($root['host'], $root['username'], $root['password']);
  $url = drush_convert_db_from_db_url($db_url);
  // Create the database.
  $result = mysql_query('CREATE DATABASE ' .  $url['database']);
  
  // Make sure our user can write to it.
  $grant_query = 'GRANT ALL PRIVILEGES ON ' . $url['database'] . '.* TO \'' . $url['username'] . '\'@\'localhost\'';
  if (isset($url['password'])) {
    $grant_query .= ' IDENTIFIED BY \'' . $url['password'] . '\''; 
  }
  mysql_query($grant_query);
  drush_log(dt("Database and user created for project", NULL, 'success');
}
