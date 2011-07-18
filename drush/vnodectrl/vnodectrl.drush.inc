<?php

/**
 * @file
 *   Example drush command.
 *
 *   To run this *fun* command, execute `sudo drush --include=./examples mmas`
 *   from within your drush directory.
 *
 *   See `drush topic docs-commands` for more information about command authoring.
 *
 *   You can copy this file to any of the following
 *     1. A .drush folder in your HOME folder.
 *     2. Anywhere in a folder tree below an active module on your site.
 *     3. /usr/share/drush/commands (configurable)
 *     4. In an arbitrary folder specified with the --include option.
 */

/**
 * Implementation of hook_drush_command().
 *
 * In this hook, you specify which commands your
 * drush module makes available, what it does and
 * description.
 *
 * Notice how this structure closely resembles how
 * you define menu hooks.
 *
 * See `drush topic docs-commands` for a list of recognized keys.
 *
 * @return
 *   An associative array describing your command(s).
 */
function vnodectrl_drush_command() {
  $items = array();
  require_once('vnodectrl.inc');
  $commands = vnodectrl_get_commands();
  foreach ($commands as $name => $command) {
    $item = array();
    $item['description'] = $command->description;
    if (isset($command->arguments)) {
      $item['arguments'] = (array)$command->arguments;
    }
    $item['bootstrap'] = DRUSH_BOOTSTRAP_DRUSH;
    $item['callback'] = 'drush_vnodectrl_exec';
    $items[$command->command] = $item;
    $item['callback'] = 'drush_vnodectrl_provision_exec';
    $items['provision-' . $command->command] = $item;
    unset($item['arguments']);
  }
  return $items;
}

/**
 * Execute any given vnodectrl command.
 */
function drush_vnodectrl_exec() {
  $args = func_get_args();
  $command = drush_get_command();
  $output = array();
  $result = vnodectrl_execute_command($command['command'], $output, $args);
  drush_print(implode("\n", $output));
  return $result;
}

function drush_vnodectrl_provision_exec() {
  $args = func_get_args();
  $command = drush_get_command();
  $command = substr($command['command'], strlen('provision-'));
  if ($command == 'create-node') {
    $provider = drush_get_option('provider', FALSE);
    $name = drush_get_option('name', FALSE);
    $image = drush_get_option('image', FALSE);
    $size = drush_get_option('size', FALSE);
    if ($provider && $name && $image && $size) {
      return vnodectrl_execute_command($command, $args, array($provider, $image, $size, $name));
    }
    else {
      drush_error('The required options were not provided.');
      return FALSE;
    }
  }
}


