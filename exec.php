<?php

function parsePrice(string $price) {
    return doubleval(str_replace(['Rp', '.'], '', $price));
}

$jobId = 33;
$cmd = "python3 crawl_tokopedia.py \"{$argv[1]}\" -l {$jobId} -n 5";
exec($cmd, $result, $stat);

if (!$stat) {
    // no errorlevel
    $data = json_decode(implode("\n",$result));
    
    echo "Status: {$stat}\n";
    echo "Got " . count($data) . " items\n";
    echo "==========================================\n";
    if (count($data)) {
        print_r($data[0]);
        // print($data[0]->name . ' @ ' . $data[0]->shop->name);
    }
    else
        print_r($data);
} else {
    echo "Status: {$stat}\n";
    echo "==========================================\n";
    print_r($result);
}