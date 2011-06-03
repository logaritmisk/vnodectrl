<?php

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
