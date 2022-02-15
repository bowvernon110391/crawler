<?php

$data = stream_get_contents(STDIN);
$json = json_decode($data);

if (!is_null($json)) {
    print("Got ". count($json) ." products\n");
    print_r($json);
}