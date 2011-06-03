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

  $items['vnodectrl-start'] = array(
    'description' => "Start the server.",
    'arguments' => array(
      'location' => 'The location of the servers (amazon ec2, virtualbox, ..)',
    ),
    'aliases' => array('vup'),
    'bootstrap' => DRUSH_BOOTSTRAP_DRUSH, // No bootstrap at all.
  );

  $items['vnodectrl-deploy'] = array(
    'description' => "Deploy the project.",
    'arguments' => array(
      'location' => 'The location of the servers (amazon ec2, virtualbox, ..)',
    ),
    'aliases' => array('vup'),
    'bootstrap' => DRUSH_BOOTSTRAP_DRUSH, // No bootstrap at all.
  );

  return $items;
}

/**
 * Implementation of hook_drush_help().
 *
 * This function is called whenever a drush user calls
 * 'drush help <name-of-your-command>'. This hook is optional. If a command
 * does not implement this hook, the command's description is used instead.
 *
 * This hook is also used to look up help metadata, such as help
 * category title and summary.  See the comments below for a description.
 *
 * @param
 *   A string with the help section (prepend with 'drush:')
 *
 * @return
 *   A string with the help text for your command.
 */
function vnodectrl_drush_help($section) {
  switch ($section) {
    case 'drush:vnodectrl-deploy':
      return dt("This command will make you a delicious sandwich, just how you like it.");
    // The 'title' meta item is used to name a group of
    // commands in `drush help`.  If a title is not defined,
    // the default is "All commands in ___", with the
    // specific name of the commandfile (e.g. sandwich).
    // Command files with less than four commands will 
    // be placed in the "Other commands" section, _unless_
    // they define a title.  It is therefore preferable
    // to not define a title unless the file defines a lot
    // of commands.
    case 'meta:sandwich:title':
      return dt("Sandwich commands");
    // The 'summary' meta item is displayed in `drush help --filter`,
    // and is used to give a general idea what the commands in this
    // command file do, and what they have in common.
    case 'meta:sandwich:summary':
      return dt("Automates your sandwich-making business workflows.");
  }
}

/**
 * Implementation of drush_hook_COMMAND_validate().
 *
 * The validate command should exit with
 * `return drush_set_error(...)` to stop execution of
 * the command.  In practice, calling drush_set_error
 * OR returning FALSE is sufficient.  See drush.api.php
 * for more details.
 */
function drush_sandwich_make_me_a_sandwich_validate() {
  if ($name['name'] !== 'root') {
    return drush_set_error('MAKE_IT_YOUSELF', dt('What? Make your own sandwich.'));
  }
}

/**
 * Deploy a site by telling the an aegir instance about the servers and which repository
 * we are going to be dealing with.
 */
function drush_vnodectrl_deploy($location = 'virtualbox') {
  // Deploy the servers we need.
  drush_exec("vnodectrl deploy $location");
  // Fetch the aegir server we are going to work with and tell it that we want to play.
  $config = vnodectrl_get_deploy_config();
  
}

