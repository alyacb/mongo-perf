#!/usr/bin/env python3

from dataclasses import dataclass
import json
import sys
from optparse import OptionParser

@dataclass(eq=True, frozen=True)
class Metric:
    name: str
    thread_count: int
    ops_per_sec: float


@dataclass(eq=True, frozen=True)
class MetricKey:
    name: str
    thread_count: int


def parse_metrics_from_json(json_input):
    metrics = []
    if type(json_input) != list:
        json_input=[json_input]

    for o in json_input:
        for i in o["results"]:
            for k, r in i["results"].items():
                if (str(k)).isnumeric():
                    for v in r["ops_per_sec_values"]:
                        metrics.append(Metric(name=str(i["name"]), thread_count=int(k), ops_per_sec=float(v)))
    return metrics


def print_summary(metrics):
    groups = {}

    for m in metrics:
        k = MetricKey(name = m.name, thread_count = m.thread_count)
        if k not in groups:
            groups[k]=[]
        groups[k].append(m.ops_per_sec)

    print("name\tthread_count\tops_per_sec\tcount\tstdev")
    for k, l in groups.items():
        count = len(l)
        mean = sum(l) / count
        variance = sum(((x - mean) ** 2) for x in l) / (count-1)
        stdev=variance**0.5
        print(
            f"{k.name}\t{k.thread_count}\t{mean}\t{count}\t{stdev}"
        )


def print_tsv(metrics):
    print("name\tthread_count\tops_per_sec")
    for m in metrics:
        print(
            f"{m.name}\t{m.thread_count}\t{m.ops_per_sec}"
        )


def main():
    """Execute Main program."""
    usage = "usage: %prog [options]"
    parser = OptionParser(description=__doc__, usage=usage)

    parser.add_option(
        "-i",
        "--input",
        dest="input",
        default=None,
    )

    parser.add_option(
        "-f",
        "--format",
        dest="format",
        default=None,
    )

    (options, args) = parser.parse_args()

    if options.input == None:
        input_str = sys.stdin.read()
    else:
        with open(options.input, 'r') as file:
            input_str = file.read()
    
    metrics = parse_metrics_from_json(json.loads(input_str))
       
    if options.format == "summary_tsv":
        print_summary(metrics)
    elif options.format == "tsv":
        print_tsv(metrics)
    else:
        raise Exception(f"Unknown option: '{options.format}'")


if __name__ == "__main__":
    main()