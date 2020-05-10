from flask import render_template

from package import app, db
from package.models import Tubes, Tables, Manufactures, Tomog, Generator, Technologies, tomog_techno


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/tomograph', methods=['GET'])
def tomograph():
    return render_template('tomograph.html', tomographs=db.session.query(Tomog.tomog_model, Manufactures.manufacture_name,
                           Tables.table_name, Tables.horizont_range,Tables.max_weight, Manufactures.country, Generator.generator_name,
                           db.func.group_concat(Technologies.technology_name).label('technology_name_list'))\
                           .join(Manufactures, Tomog.manufacture_id==Manufactures.id)\
                           .join(Tables, Tomog.table_id==Tables.id)\
                           .join(Generator, Tomog.generator_id==Generator.id)\
                           .join(Tubes, Tomog.tube_id==Tubes.id)\
                           .join(tomog_techno, Tomog.id==tomog_techno.c.tomog_id)\
                           .join(Technologies, tomog_techno.c.techno_id==Technologies.id)\
                           .group_by(Tomog.id))


@app.route('/manufacture', methods=['GET'])
def manufacture():
    return render_template('manufacture.html', manufactures=Manufactures.query.all())

@app.route('/tubes', methods=['GET'])
def tubes():
    return render_template('tubes.html', tubes=Tubes.query.join(Manufactures, Tubes.manufacture_id==Manufactures.id)\
                           .add_columns(Manufactures.manufacture_name, Manufactures.manufacture_longname, Manufactures.country,
                                        Tubes.tube_model, Tubes.focus, Tubes.capacity, Tubes.coolingrate, Tubes.servise_life).all())

@app.route('/generators', methods=['GET'])
def generators():
    return render_template('generators.html', generators=Generator.query.join(Manufactures, Generator.manufacture_id==Manufactures.id)\
                           .add_columns(Manufactures.manufacture_name, Manufactures.manufacture_longname, Manufactures.country,
                                        Generator.generator_name, Generator.power, Generator.current, Generator.voltage).all())

@app.route('/tables', methods=['GET'])
def tables():
    return render_template('tables.html', tables=Tables.query.join(Manufactures, Tables.manufacture_id==Manufactures.id)\
                           .add_columns(Tables.table_name, Tables.horizont_range, Tables.max_weight, Manufactures.manufacture_name,
                                        Manufactures.manufacture_longname, Manufactures.country).all())

@app.route('/hints', methods=['GET'])
def hints():
    return render_template('hints.html')

@app.route('/technologies', methods=['GET'])
def technologies():
    return render_template('technologies.html', technologies=Technologies.query.join(Manufactures, Technologies.manufacture_id==Manufactures.id)\
                           .add_columns(Manufactures.manufacture_name, Technologies.technology_name, Technologies.technology_text).all())