<?php
define('VNODECTRL', 'python /home/fabsor/projects/vnodectrl/src/vnodectrl.py');
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
 */
function vnodectrl_get_commands() {
  // Execute the vnodectrl list
  $result = drush_shell_exec(VNODECTRL . ' list-plugins');
  if ($result) {
    $commands = json_decode(implode("\n", drush_shell_exec_output()));
  }
  return $commands;
}

function vnodectrl_execute_command($command, &$output, $args = array(), $options = array()) {
  $args = implode(' ', $args);
  $result = drush_shell_exec(VNODECTRL . ' ' . $command . ' ' . $args);
  $output = drush_shell_exec_output();
  return $result;
}