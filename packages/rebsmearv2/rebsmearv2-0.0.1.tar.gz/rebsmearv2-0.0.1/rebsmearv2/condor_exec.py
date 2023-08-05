#!/usr/bin/env python
import os
import re
import math
import htcondor
import argparse
from datetime import date
from pprint import pprint
from collections import defaultdict

from helpers.condor import condor_submit
from helpers.git import git_rev_parse, git_diff
from helpers.dataset import files_from_eos
from helpers.deployment import pack_repo
from helpers.paths import xrootd_format

from rebalance.rebalancer import RebalanceExecutor

pjoin = os.path.join

def parse_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outpath', help='Path to save the output under.')
    parser.add_argument('--tree',type=str, default='Events', help='Name of the TTree in the input files.')
    parser.add_argument('--jobs','-j', type=int, default=1, help='Number of cores to use / request.')
    parser.add_argument('--dummyjer', help='Placeholder Gaussian width for JER (for testing).', type=float, default=None)

    subparsers = parser.add_subparsers(help='sub-command help')
    # Arguments passed to the "run" operation
    parser_run = subparsers.add_parser('run', help='Running help')
    parser_run.add_argument('--dataset', type=str, help='Dataset name to run over.')
    parser_run.set_defaults(func=do_run)

    # Arguments passed to the "worker" operation
    parser_worker = subparsers.add_parser('worker', help='Running help')
    parser_worker.add_argument('--dataset', type=str, help='Dataset name to run over.')
    parser_worker.add_argument('--filelist', type=str, help='Text file with file names to run over.')
    parser_worker.add_argument('--chunk', type=str, help='Number of this chunk for book keeping.')
    parser_worker.set_defaults(func=do_worker)

    # Arguments passed to the "submit" operation
    parser_submit = subparsers.add_parser('submit', help='Submission help')
    parser_submit.add_argument('--dataset', type=str, help='Dataset regex to use.')
    parser_submit.add_argument('--filesperjob', type=int, default=4, help='Number of files to process per job')
    parser_submit.add_argument('--eventsperjob', type=int, default=5e6, help='Number of events to process per job')
    parser_submit.add_argument('--name', type=str, default=f'{date.today().strftime("%Y-%m-%d")}_rebsmear_run', help='Name to identify this submission')
    parser_submit.add_argument('--dry', action="store_true", default=False, help='Do not trigger submission, just dry run.')
    parser_submit.add_argument('--test', action="store_true", default=False, help='Only run over one file per dataset for testing.')
    parser_submit.add_argument('--asynchronous', action="store_true", default=False, help='Submit asynchronously.')
    parser_submit.add_argument('--memory',type=int, default=None, help='Memory to request (in MB). Default is 2100 * number of cores.')
    parser_submit.set_defaults(func=do_submit)

    args = parser.parse_args()
    return args

def chunk_by_files(items, nchunk):
    '''Split list of items into nchunk ~equal sized chunks'''
    chunks = [[] for _ in range(nchunk)]
    for i in range(len(items)):
        chunks[i % nchunk].append(items[i])
    return chunks

def run_rebalancing_job(fileset, dataset, treename):
    '''Wrapper script to run a rebalancing job.'''
    proc = RebalanceExecutor(fileset, dataset, treename)

def do_run(args):
    """Run the R&S locally."""
    # Run over all files associated to dataset
    fileset = files_from_eos(regex=args.dataset)

    ndatasets = len(fileset)
    nfiles = sum([len(x) for x in fileset.values()])
    print(f"Running over {ndatasets} datasets with a total of {nfiles} files.")

    for dataset, files in fileset.items():
        pass

def do_worker(args):
    '''Run the R&S on a worker node.'''
    # Run over all files associated to dataset
    with open(args.filelist, "r") as f:
        files = [xrootd_format(x.strip()) for x in f.readlines()]
    fileset = {args.dataset : files}

    ndatasets = len(fileset)
    nfiles = sum([len(x) for x in fileset.values()])
    print(f"Running over {ndatasets} datasets with a total of {nfiles} files.")


def do_submit(args):
    '''Handle HTcondor submission.'''
    # Extract files per dataset
    dataset_files = files_from_eos(regex=args.dataset)
    # Test mode: 1 file per dataset
    if args.test:
        tmp = {}
        for k, v in dataset_files.items():
            tmp[k] = v[:1]
        dataset_files = tmp
    
    # Output directory for this job
    outdir = f'./submission/{args.name}'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    # Repo version information
    with open(pjoin(outdir, 'version.txt'),'w') as f:
        f.write(git_rev_parse()+'\n')
        f.write(git_diff()+'\n')

    # Sub-directory to store submission files
    filedir = 'files'
    if not os.path.exists(pjoin(outdir, filedir)):
        os.makedirs(pjoin(outdir, filedir))

    input_files = []
    # Pack the repository and ship it with the job
    gridpack_path = pjoin(outdir, 'gridpack.tgz')
    gridpack_exists = os.path.exists(gridpack_path)
    if (not gridpack_exists):
        pack_repo(gridpack_path)
    input_files.append(gridpack_path)

    for dataset, files in dataset_files.items():
        print(f"Writing submission files for dataset: {dataset}.")

        nchunk = math.ceil(len(files)/args.filesperjob)
        chunks = chunk_by_files(files, nchunk=int(nchunk))
        for ichunk, chunk in enumerate(chunks):
            # Save input files to a txt file and send to job
            tmpfile = pjoin(outdir, filedir, f"input_{dataset}_{ichunk:03d}of{len(chunks):03d}.txt")
            with open(tmpfile, "w") as f:
                for file in chunk:
                    f.write(f"{file}\n")

            # Job file creation
            arguments = [
                args.processor,
                f'--outpath .',
                f'--jobs {args.jobs}',
                f'--tree {args.tree}',
                'worker',
                f'--dataset {dataset}',
                f'--filelist {os.path.basename(tmpfile)}',
                f'--chunk {ichunk}'
            ]

            job_input_files = input_files + [
                os.path.abspath(tmpfile),
            ]

            chunkname = f'{dataset}_{ichunk:03d}of{len(chunks):03d}'
            submission_settings = {
                "Initialdir" : outdir,
                # "executable": bucoffea_path("execute/htcondor_wrap.sh"),
                "should_transfer_files" : "YES",
                "when_to_transfer_output" : "ON_EXIT",
                "transfer_input_files" : ", ".join(job_input_files),
                # "environment" : '"' + ' '.join([f"{k}={v}" for k, v in environment.items()]) + '"',
                "arguments": " ".join(arguments),
                "Output" : f"{filedir}/out_{chunkname}.txt",
                "Error" : f"{filedir}/err_{chunkname}.txt",
                "log" : f"{filedir}/log_{chunkname}.txt",
                "request_cpus" : str(args.jobs),
                "request_memory" : str(args.memory if args.memory else args.jobs*2100),
                "+MaxRuntime" : f"{60*60*12}",
                "on_exit_remove" : "((ExitBySignal == False) && (ExitCode == 0)) || (NumJobStarts >= 2)",
            }

            sub = htcondor.Submit(submission_settings)
            jdl = pjoin(outdir,filedir,f'job_{chunkname}.jdl')
            
            with open(jdl,"w") as f:
                f.write(str(sub))
                f.write("\nqueue 1\n")

            # Submission
            if args.dry:
                jobid = -1
                print(f"Submitted job {jobid}")
            else:
                if args.asynchronous:
                    jdl_to_submit.append(jdl)
                else:
                    jobid = condor_submit(jdl)
                    print(f"Submitted job {jobid}")
    
    if args.asynchronous:
        print('Starting asynchronous submission.')
        p = Pool(processes=8)
        res = p.map_async(condor_submit, jdl_to_submit)
        res.wait()
        if res.successful():
            print(f"Asynchronous submission successful for {len(jdl_to_submit)} jobs.")
        else:
            print("Asynchronous submission failed.")

def main():
    args = parse_cli()
    args.func(args)

if __name__ == '__main__':
    main()