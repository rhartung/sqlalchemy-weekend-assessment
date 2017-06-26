"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# The above query would return a datatype of a flask sqlalchemy base query.
# Without a .all(), .one(), or .first() at the end of the query,
# the query does not return an object.



# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# An association table exists solely to create a relationship between two
# tables without any common keys by binding them together with foreign keys
# populated from the relevant tables.  Association tables do not contain any new
# information and only contain foreign keys from other tables with meaningful
# information.  Association tables manage many to many relationships where it
# would make sense for each object of both tables to have the ability to
# be associated with multiple objects from the other table.  For example,
# a teacher may have many students, and a student may have many teachers.
# a StudentTeacher table would allow the creator of the database to show
# relationships between students and teachers without constraining the student
# or teacher tables.

# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries

# Get the brand with the brand_id of ``ram``.
q1 = Brand.query.filter_by(brand_id="ram").one()

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = Model.query.filter_by(name="Corvette", brand_id="che").all()

# Get all models that are older than 1960.
q3 = db.session.query(Model).filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = db.session.query(Brand).filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = Model.query.filter(Model.name.like("Cor%")).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.

# tried below query in terminal with 'is None' instead of '== None' and query
# did not work - syntactically & stylistically '== None' seems weird but worked
q6 = Brand.query.filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.

# same issue with this question as issue with q6 - 'is not None' did not work
# '!= None' does work.  Syntax seems weird but output is correct
q7 = Brand.query.filter((Brand.founded < 1950) | (Brand.discontinued != None)).all()

# Get all models whose brand_id is not ``for``.

q8 = db.session.query(Model).filter(Model.brand_id != "for").all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    model_info = db.session.query(Model.name,
                                  Brand.name,
                                  Brand.headquarters,
                                  ).join(Brand).filter(Model.year == year).all()

    for model, brand, headquarters in model_info:
        print "Model: %s, Brand: %s, HQ: %s" % (model, brand, headquarters)


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    # this was as close as I could get to the answer on this one
    # was unable to figure out how to get each brand name to print
    # only once with each affiliated model - this seems to be something
    # that should be solved with a group_by statement but each time
    # I use a group_by I get an error message that I need to include
    # Model.name and Model.year in the group_by as well, or use them
    # in an aggregate function

    brand_info = db.session.query(Brand.name,
                                  Model.name,
                                  Model.year
                                  ).join(Model).all()

    for brand, model, year in brand_info:
        print "Brand: %s, Model: %s, Year: %s" % (brand, model, year)


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    # tried query below without .format method
    # returned errors or empty string
    # added .format to replace brackets in string with mystr variable
    return Brand.query.filter(Brand.name.like("%{}%".format(mystr))).all()


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year,
                              Model.year < end_year).all()
