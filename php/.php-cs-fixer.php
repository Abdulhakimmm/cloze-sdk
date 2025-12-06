<?php

$config = new PhpCsFixer\Config();
return $config
    ->setRules([
        '@PSR12' => true,
        'blank_line_after_namespace' => true,
        'blank_line_after_opening_tag' => true,
    ])
    ->setFinder(
        PhpCsFixer\Finder::create()
            ->in(__DIR__ . '/src')
    );

