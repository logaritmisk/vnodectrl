<?php

function drush_hosting_vnodectrl_pre_hosting_task() {
  $task =& drush_get_context('HOSTING_TASK');
  if ($task->ref->type == 'server' && ($task->task_type == 'create-node' || $task->task_type == 'delete-node')) {
    $task->options['provider'] = $task->ref->provider;
    $task->options['image'] = $task->image;
    $task->options['name'] = $task->ref->title;
    $task->options['size'] = $task->ref->size;
  }
}
