from time import perf_counter
from flask import render_template, request, redirect, url_for
from app import app, db
from app.repositories import (
    generate_random_persons,
    run_depersonalization_identifier,
    run_un_depersonalization_identifier,
    write_time_into_experimental_data,
    run_depersonalization_shuffle,
    run_undepersonalization_shuffle,
    run_depersonalization_decomposition,
    run_undepersonalization_decomposition
)
from app.models.experiment import TestData, ExperimentalData
from app.models.identifier import (
    DepersonalizeDataForIdentifierMethod,
    ConformityTableForIdentifierMethod,
    UnDepersonalizationDataForIdentifierMethod,
)
from app.models.shuffle import (
    TableForShuffleMethod,
    UnDepersonalizationDataForShuffleMethod,
)
from app.models.decomposition import (
    FirstDepersonalizeTableForDecompositionMethod,
    SecondDepersonalizeTableForDecompositionMethods,
    LinkTableForDecompositionMethod,
    UnDepersonalizationDataForDecompositionMethod,
)


# -- pages ---
@app.route("/", methods=["GET"])
@app.route("/testing-methods", methods=["GET"])
def testing_methods():
    return render_template("creating_test_db.html", test_datas=TestData.query.all())


@app.route("/method-1", methods=["GET"])
def method_1():
    return render_template(
        "method_1.html",
        experimental_data=ExperimentalData()
        .query.filter_by(method_name="identifier")
        .first(),
        depersonalize_data=DepersonalizeDataForIdentifierMethod().query.all(),
        conformity_table=ConformityTableForIdentifierMethod().query.all(),
        undepersonalize_data=UnDepersonalizationDataForIdentifierMethod().query.all(),
    )


@app.route("/method-2", methods=["GET"])
def method_2():
    return render_template(
        "method_2.html",
        experimental_data=ExperimentalData()
        .query.filter_by(method_name="shuffle")
        .first(),
        shuffle_table=TableForShuffleMethod().query.all(),
        undepersonalize_data=UnDepersonalizationDataForShuffleMethod().query.all(),
    )


@app.route("/method-3", methods=["GET"])
def method_3():
    return render_template(
        "method_3.html",
        experimental_data=ExperimentalData()
        .query.filter_by(method_name="decomposition")
        .first(),
        first_table=FirstDepersonalizeTableForDecompositionMethod().query.all(),
        second_table=SecondDepersonalizeTableForDecompositionMethods().query.all(),
        link_table=LinkTableForDecompositionMethod().query.all(),
        undepersonalize_data=UnDepersonalizationDataForDecompositionMethod().query.all(),
    )


@app.route("/summary", methods=["GET"])
def summary():
    return render_template(
        "summary.html",
        identifier_data=ExperimentalData()
        .query.filter_by(method_name="identifier")
        .first(),
        shuffle_data=ExperimentalData()
        .query.filter_by(method_name="shuffle")
        .first(),
        decomposition_data=ExperimentalData()
        .query.filter_by(method_name="decomposition")
        .first(),
    )


# -- actions ---
@app.route("/generate-persons", methods=["POST"])
def generate_persons():
    person_count = request.form['personCount']

    generate_random_persons(db, person_count)

    return redirect(url_for("testing_methods"))


@app.route("/run-method-1", methods=["POST"])
def run_method_1():
    t_start = perf_counter()
    run_depersonalization_identifier(db)
    t_de = perf_counter() - t_start

    t_start = perf_counter()
    run_un_depersonalization_identifier(db)
    t_unde = perf_counter() - t_start

    write_time_into_experimental_data(db,
                                      t_de,
                                      t_unde,
                                      'identifier')

    return redirect(url_for("method_1"))


@app.route("/run-method-2", methods=["POST"])
def run_method_2():
    t_start = perf_counter()
    run_depersonalization_shuffle(db)
    t_de = perf_counter() - t_start

    t_start = perf_counter()
    run_undepersonalization_shuffle(db)
    t_unde = perf_counter() - t_start

    write_time_into_experimental_data(db,
                                      t_de,
                                      t_unde,
                                      'shuffle')

    return redirect(url_for("method_2"))


@app.route("/run-method-3", methods=["POST"])
def run_method_3():
    t_start = perf_counter()
    run_depersonalization_decomposition(db)
    t_de = perf_counter() - t_start

    t_start = perf_counter()
    run_undepersonalization_decomposition(db)
    t_unde = perf_counter() - t_start

    write_time_into_experimental_data(db,
                                      t_de,
                                      t_unde,
                                      'decomposition')

    return redirect(url_for("method_3"))
