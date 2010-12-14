<?php
$virtual_base = array(
    'remote-host' => 'virtual0',
    'remote-user' => 'ubuntu',
    'path-aliases' => array(
      '%drush' => '/opt/drush',
      '%drush-script' => '/opt/drush/drush',
      '%dump' => '/home/ubuntu/sql_dump.sql',
     ),
);
// Replace your-username with your username on green12
$g12_base = array(
  'remote-host' => 'green12.nodeone.se',
  'remote-user' => 'your-username',
  'path-aliases' => array(
    '%drush' => '/usr/local/share/drush',
    '%drush-script' => '/usr/local/share/drush/drush',
    '%dump' => '/home/your-username/sql_dump.sql',
  ),
);
/**
 * Uncomment the lines below and adjust to your preference.
 */
/*
// Replace example with your preferred name and NUMBER with the number of the site.
$aliases['example-virtual'] = array(
  'uri' => 'loc.example.com',
  'root' => '/srv/www/NUMBER/web',
) + $virtual_base;

$aliases['example-g12'] = array(
    'uri' => 'dev.example.org',
    'root' => '/srv/www/NUMBER/web',
) + $g12_base;
*/
// Copy the aliases above for each project you are working on.
