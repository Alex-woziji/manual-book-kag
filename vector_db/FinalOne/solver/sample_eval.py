import json
import pandas as pd

from kag.solver.logic.solver_pipeline import SolverPipeline
from kag.common.conf import KAG_CONFIG
from kag.common.registry import import_modules_from_path

pd.set_option('mode.chained_assignment', None)
import_modules_from_path("./prompt")
failures = pd.read_csv(r"../../../data/csv/failures_updated.csv")
with open("../../../builder/solution_mapping.json", "r") as f:
    solution_type = json.load(f)


def get_sample_data(num):
    type_1_record = failures[failures['failure_type'] == 1]
    type_1_record.index = range(len(type_1_record))
    sample_data = type_1_record[:num]
    sample_data.loc[:, 'solution_des'] = sample_data['solution_method'].apply(
        lambda x: solution_type['failure_type_2_solution_sample'][int(x)])
    return sample_data


def qa(query):
    resp = SolverPipeline.from_config(KAG_CONFIG.all_config["kag_solver_pipeline"])
    answer, traceLog = resp.run(query)

    print(f"\n\nso the answer for '{query}' is: {answer}\n\n")  #
    print(traceLog)
    return answer, traceLog


if __name__ == "__main__":
    sample_data = get_sample_data(2)

    result = []
    for ind, row in sample_data.iterrows():
        print(f"search in type {row['failure_type']}")
        result.append(qa(f"how to {row['solution_des']}?"))
    sample_data.loc[:, 'answer'] = [each[0] for each in result]
    sample_data.loc[:, 'retrieve_doc'] = [each[1] for each in result]
    sample_data.to_excel("../output/solver_record.xlsx", index=False)
