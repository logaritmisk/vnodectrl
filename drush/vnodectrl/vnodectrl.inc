<?php
/**
 * @file
 * This file contains some utility functions for dealing with vnodectrl stuff.
 */

/**
 * Fetch vnodectrl configuration.
 */
function vnodectrl_get_configuration() {
  $conf_path = $home_dir . '.vnodectrl.d/3.x/vnodectrl.conf';
  if (file_exists($conf_path)) {
    return json_decode($conf_path);
  }
  return FALSE;
}

/**
 * Get the vnodectrl deploy configration for the current project,
 * if any.
 */
function vnodectrl_get_deploy_config($path = FALSE) {
  if (!$path)
    $path =  getcwd();
  $deployfile = $path . '.vnodectrl';

  if ($path == '/') {
    return FALSE;
  }
  elseif (file_exists($deployfile)) {
    return json_decode($deployfile);
  }
  else {
    $path = substr($path, strpos(basename($path)) - 1);
    return vnodectrl_get_deploy_config($path);
  }
}

/**
 * Get commands from vnodectrl.
 * @return array
 * 	An array with all commands that exists in vnodectrl.
 */
function vnodectrl_get_commands() {
  // Execute the vnodectrl list
  $result = drush_shell_exec('vnodectrl list-plugins');
  if ($result) {
    $commands = json_decode(implode("\n", drush_shell_exec_output()));
  }
  return $commands;
}

/**
 * Execute a vnodectrl command.
 * @param string $command
 * 	The command to execute
 * @param array $output
 * 	This array will be populated with the output of the command.
 * @param array $args
 * 	Add any arguments the command needs here.
 * @param array $options
 * 	Provide a keyed array with the options for the command here.
 * @return boolean
 * 	The execution status of the command.
 */
function vnodectrl_execute_command($command, &$output, $args = array(), $options = array()) {
  $args = implode(' ', $args);
  $result = drush_shell_exec('vnodectrl ' . $command . ' ' . $args);
  $output = drush_shell_exec_output();
  return $result;
}
