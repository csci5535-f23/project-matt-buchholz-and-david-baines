import json
import os

from google.cloud import bigquery
import re

TEMPLATE = f"""SELECT files.repo_name, files.path, files.ref, contents.content \n \
FROM `bigquery-public-data.github_repos.files` as files, \n \
     `bigquery-public-data.github_repos.contents` as contents \n \
WHERE contents.id = files.id AND \n \
      contents.id in UNNEST(@ids);"""

def extract_id(line):
    match = re.search(r'"id":\s*"(.*?)"', line)
    if match:
        return str(match.group(1))
    return None

def execute_bigquery_query(ids):
    # Initialize BigQuery client
    bq_client = bigquery.Client(project='pl-prj')


    query_template = TEMPLATE
    query_params = [bigquery.ArrayQueryParameter("ids", "STRING", ids)]
    job_config = bigquery.QueryJobConfig(query_parameters=query_params)

    # Execute the query
    query_job = bq_client.query(query_template, job_config=job_config)
    result = query_job.result()

    for row in result:
        print(row)


def main(manifest_file):
    with open(manifest_file, 'r') as file:
        lines = file.readlines()
        ids = [extract_id(line) for line in lines if extract_id(line) is not None]
        ids = ids[:10]

    # Execute BigQuery query
    execute_bigquery_query(ids)

import shutil
def extract_python(codenet_dir):
    for item in os.listdir(codenet_dir):
        if os.path.isdir(codenet_dir + item):
            try:
                for file in os.listdir(codenet_dir + "/" + item + '/Python'):
                    path = codenet_dir + "/" + item + '/Python/' + file
                    shutil.copyfile(path, './python_codenet/' + file)
            except:
                for file in os.listdir(codenet_dir + "/" + item):
                    if file.endswith('.py'):
                        path = codenet_dir + "/" + item + '/' + file
                        shutil.copyfile(path, './python_codenet/' + file)




if __name__ == "__main__":
    extract_python('codenet/data/')
    # manifest_directory = 'dataset_manifests/'
    # manifest_file_path = manifest_directory + \
    #                      '20200621_Python_github_python_minus_ethpy150open_deduplicated_manifest_manifest.jsontxt-00000-of-00041'
    #
    # # Run the script
    # main(manifest_file_path)