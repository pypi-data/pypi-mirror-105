import os
import datetime as dt


def get_db_data(db, all_e_ids):
    """ Helper to get all data from pickledb database. """
    total_data = get_total_experiments(db, all_e_ids)
    last_data = get_last_experiment(db, all_e_ids[-1])
    time_data = get_time_experiment(db, all_e_ids[-1])
    return total_data, last_data, time_data


def get_total_experiments(db, all_experiment_ids):
    """ Get data from db to show in 'total_experiments' panel. """
    run, done, aborted, sge, slurm, gcp, local = 0, 0, 0, 0, 0, 0, 0
    report_gen, gcs_stored, retrieved = 0, 0, 0
    for e_id in all_experiment_ids:
        status = db.dget(e_id, "job_status")
        # Job status
        run += status == "running"
        done += status == "completed"
        aborted += status not in ["running", "completed"]
        # Execution resource data
        resource = db.dget(e_id, "exec_resource")
        sge += resource == "sge-cluster"
        slurm += resource == "slurm-cluster"
        gcp += resource == "gcp-cloud"
        local += resource not in ["sge-cluster", "slurm-cluster", "gcp-cloud"]
        # Additional data: Report generated, GCS stored, Results retrieved
        try:
            report_gen += db.dget(e_id, "report_generated")
            gcs_stored += db.dget(e_id, "stored_in_gcloud")
            retrieved += db.dget(e_id, "retrieved_results")
        except:
            pass
    # Return results dictionary
    results = {"total": str(len(all_experiment_ids)),
               "run": str(run), "done": str(done), "aborted": str(aborted),
               "sge": str(sge), "slurm": str(slurm), "gcp": str(gcp),
               "local": str(local), "report_gen": str(report_gen),
               "gcs_stored": str(gcs_stored),"retrieved": str(retrieved)}
    return results


def get_time_experiment(db, last_experiment_id):
    """ Get data from db to show in 'time_experiment' panel. """
    meta_args = db.dget(last_experiment_id, "meta_job_args")
    job_spec_args = db.dget(last_experiment_id, "job_spec_args")
    single_job_args = db.dget(last_experiment_id, "single_job_args")

    if meta_args["job_type"] == "hyperparameter-search":
        total_jobs = (job_spec_args["num_search_batches"]
                      * job_spec_args["num_iter_per_batch"]
                      * job_spec_args["num_evals_per_iter"])
        total_batches = job_spec_args["num_search_batches"]
        jobs_per_batch = (job_spec_args["num_iter_per_batch"]
                          * job_spec_args["num_evals_per_iter"])
    elif meta_args["job_type"] == "multiple-experiments":
        total_jobs = (len(job_spec_args["config_fnames"])*
                      job_spec_args["num_seeds"])
        total_batches = 1
        jobs_per_batch = "-"
    else:
        total_jobs = 1
        total_batches = 1
        jobs_per_batch = "-"

    start_time = db.dget(last_experiment_id, "start_time")

    if "time_per_job" in single_job_args.keys():
        time_per_batch = single_job_args["time_per_job"]
        days, hours, minutes = time_per_batch.split(":")
        hours_add, tot_mins = divmod(total_batches * int(minutes), 60)
        days_add, tot_hours = divmod(total_batches * int(hours)+hours_add, 24)
        tot_days = total_batches * int(days) + days_add
        tot_days, tot_hours, tot_mins = (str(tot_days), str(tot_hours),
                                         str(tot_mins))
        if len(tot_days) < 2: tot_days = "0" + tot_days
        if len(tot_hours) < 2: tot_hours = "0" + tot_hours
        if len(tot_mins) < 2: tot_mins = "0" + tot_mins
        est_duration = tot_days + ":" + tot_hours + ":" + tot_mins

        # Check if last experiment has already terminated!
        try:
            stop_time = db.dget(last_experiment_id, "stop_time")
        except:
            start_date = dt.datetime.strptime(start_time, "%m/%d/%Y %H:%M:%S")
            end_date = start_date + dt.timedelta(days=int(tot_days),
                                                 hours=int(tot_hours),
                                                 minutes=int(tot_mins))
            stop_time = end_date.strftime("%m/%d/%Y %H:%M:%S")
    else:
        start_time = "-"
        stop_time = "-"
        time_per_batch = "-"
        est_stop_time = "-"
        est_duration = "-"

    results = {"total_jobs": total_jobs,
               "total_batches": total_batches,
               "jobs_per_batch": jobs_per_batch,
               "time_per_batch": time_per_batch,
               "start_time": start_time,
               "stop_time": stop_time,
               "est_duration": est_duration}
    return results


def get_last_experiment(db, last_experiment_id):
    """ Get data from db to show in 'last_experiments' panel. """
    # Return results dictionary
    e_path = db.dget(last_experiment_id, "exp_retrieval_path")
    meta_args = db.dget(last_experiment_id, "meta_job_args")
    job_spec_args = db.dget(last_experiment_id, "job_spec_args")
    e_type = meta_args["job_type"]
    e_dir = meta_args["experiment_dir"]
    e_script = meta_args["base_train_fname"]
    e_config = os.path.split(meta_args["base_train_config"])[1]
    try:
        e_report = meta_args["report_generation"]
    except:
        e_report = False
    results = {"e_id": str(last_experiment_id),
               "e_dir": e_dir,
               "e_type": e_type,
               "e_script": e_script,
               "e_config": e_config,
               "report_gen": e_report}

    # Add additional data based on the experiment type
    if e_type == "hyperparameter-search":
        results["search_type"] = job_spec_args["search_type"]
        results["eval_metrics"] = job_spec_args["eval_metrics"]
        results["params_to_search"] = job_spec_args["params_to_search"]
    elif e_type == "multiple-experiments":
        results["config_fnames"] = job_spec_args["config_fnames"]
    return results
