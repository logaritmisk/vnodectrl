<?php
/**
* Implementation of hook_hosting_TASK_OBJECT_context_options().
*/
function vnodectrl_hosting_vnodectrl_context_options(&$task) {
  $task->context_options['provider'] = check_plain($task->ref->provider);
  $task->context_options['image'] = check_plain($task->ref->image);
  $task->context_options['size'] = check_plain($task->ref->title);
  $task->context_options['name'] = check_plain($task->ref->name);
}

function drush_vnodectrl_pre_hosting_task() {
  $task =& drush_get_context('HOSTING_TASK');
  if ($task->ref->type == 'server' && ($task->task_type == 'create-node' || $task->task_type == 'delete-node')) {
    $task->options['provider'] = $task->ref->provider;
    $task->options['image'] = $task->image;
    $task->options['name'] = $task->ref->title;
    $task->options['size'] = $task->ref->size;
  }
}
