<?php

/**
 * @file
 * Utility functions for talking to an aegir server through an
 * API.
 */

/**
 * Represents a connection to an Aegir server.
 */
class VnodectrlAegirConnection {
  var $curl;
  
  function __construct($hostname, $port, $username, $password) {
    
  }

  /**
   * Save a server on aegir. If the server already exists, it will be updated.
   */
  function saveServer($hostname, $addresses, $database = 'mysql', $web_server = 'apache') {
    
  }

  /**
   * Return a list of servers on the platform.
   */
  function listServers() {

  }

  /**
   * Delete a server from the Aegir platform.
   */
  function deleteServer($hostname) {

  }

  /**
   * Save a platform on the aegir server.
   */
  function savePlatform($server, $name, $path) {

  }

  /**
   * Return a list of platforms on the Aegir server.
   */
  function listPlatforms() {

  }
}

/**
 * Get a connection to an aegir server.
 */
function vnodectrl_get_aegir_connection($vars) {
  
}