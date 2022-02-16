<?php

function parsePrice(string $price) {
    return doubleval(str_replace(['Rp', '.'], '', $price));
}

$cmd = "python3 main.py \"{$argv[1]}\"";
exec($cmd, $result, $stat);
$data = json_decode(implode("\n",$result));

echo "Status: {$stat}\n";
echo "Got " . count($data) . " items\n";
echo "==========================================\n";
print_r($data[0]);