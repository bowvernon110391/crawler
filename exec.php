<?php

function parsePrice(string $price) {
    return doubleval(str_replace(['Rp', '.'], '', $price));
}

$jobId = 33;
$cmd = "python3 main.py \"{$argv[1]}\" {$jobId}";
exec($cmd, $result, $stat);

if (!$stat) {
    // no errorlevel
    $data = json_decode(implode("\n",$result));
    
    echo "Status: {$stat}\n";
    echo "Got " . count($data) . " items\n";
    echo "==========================================\n";
    if (count($data))
        print_r($data[0]);
    else
        print_r($data);
} else {
    echo "Status: {$stat}\n";
    echo "==========================================\n";
    print_r($result);
}