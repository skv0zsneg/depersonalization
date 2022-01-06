from time import perf_counter
from flask import render_template, request, redirect, url_for
from app import app, db
from app.repositories import generate_random_persons
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
    # ...
    return redirect(url_for("testing_methods"))


@app.route("/run-method-1", methods=["GET"])
def run_method_1():
    # ...
    db.session.commit()


@app.route("/run-method-2", methods=["GET"])
def run_method_2():
    # ...
    db.session.commit()


@app.route("/run-method-3", methods=["GET"])
def run_method_3():
    # ...
    db.session.commit()
