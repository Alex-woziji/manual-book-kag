import json
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from kag.common.benchmarks.evaluate import Evaluate
from kag.solver.logic.solver_pipeline import SolverPipeline
from kag.common.conf import KAG_CONFIG
from kag.common.registry import import_modules_from_path

from kag.common.checkpointer import CheckpointerManager
KAG_CONFIG.initialize(r"D:\WorkSpace\PycharmFile\kag\vector_db\FinalOne\kag_config.yaml")
import_modules_from_path(r"D:\WorkSpace\PycharmFile\kag\vector_db\FinalOne\solver\prompt")

def qa(query):

    print("KAG_CONFIG.all_config",KAG_CONFIG.all_config)
    resp = SolverPipeline.from_config(KAG_CONFIG.all_config["kag_solver_pipeline"])
    answer, traceLog = resp.run(query)

    print(f"\n\nso the answer for '{query}' is: {answer}\n\n")  #
    print(traceLog)
    return answer, traceLog


if __name__ == "__main__":
    import_modules_from_path(r"D:\WorkSpace\PycharmFile\kag\vector_db\FinalOne\solver\prompt")
    queries = [
        "how to check the turret clamp/unclamp proximity sensor.",
    ]
    for q in queries:
        qa(q)
