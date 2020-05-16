from flask import render_template, request

from package import app, db
from package.models import Tubes, Tables, Manufactures, Tomog, Generator, Technologies, tomog_techno, Hints, Image


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/tomograph', methods=['GET'])
def tomograph():
    return render_template('tomograph.html', manufactures=db.session.query(Manufactures.manufacture_name).all(), tomographs=db.session.query(Tomog.tomog_model, Manufactures.manufacture_name,
                           Tables.table_name, Tables.horizont_range,Tomog.slicecount,Tomog.spiraltype, Tables.max_weight,
                            Manufactures.country, Generator.generator_name, Tomog.tubecount, Tomog.gantry, Tomog.fov_x, Tomog.fov_z,
                            Tomog.fps, Tomog.slice_thicness, Tomog.spatial_resolution, Tomog.rotation_time, Tomog.room_size,
                            Tomog.performance, Generator.power, Generator.current, Generator.voltage, Manufactures.manufacture_longname,
                            Tubes.tube_model, Tubes.focus, Tubes.capacity, Tubes.coolingrate, Tubes.servise_life, Image.name, Image.path,
                           db.func.group_concat(Technologies.technology_name).label('technology_name_list'))\
                           .join(Manufactures, Tomog.manufacture_id==Manufactures.id)\
                           .join(Tables, Tomog.table_id==Tables.id)\
                           .join(Generator, Tomog.generator_id==Generator.id)\
                           .join(Tubes, Tomog.tube_id==Tubes.id)\
                           .join(tomog_techno, Tomog.id==tomog_techno.c.tomog_id)\
                           .join(Technologies, tomog_techno.c.techno_id==Technologies.id)\
                           .join(Image, Tomog.image_id==Image.id)
                           .group_by(Tomog.id))

@app.route('/tomograph_filter', methods=['GET','POST'])
def tomograph_filter():
    manufacturers = Manufactures.query.all()  # получаем из БД все неймы Производителей
    masss = list(request.form.keys())
    print(masss)
    srez_l = request.form.get('srez_l')
    srez_h = request.form.get('srez_h')
    return render_template('tomograph.html', manufactures=manufacturers, tomographs=db.session.query(Tomog.tomog_model, Manufactures.manufacture_name,
                           Tables.table_name, Tables.horizont_range,Tomog.slicecount,Tomog.spiraltype, Tables.max_weight,
                            Manufactures.country, Generator.generator_name, Tomog.tubecount, Tomog.gantry, Tomog.fov_x, Tomog.fov_z,
                            Tomog.fps, Tomog.slice_thicness, Tomog.spatial_resolution, Tomog.rotation_time, Tomog.room_size,
                            Tomog.performance, Generator.power, Generator.current, Generator.voltage, Manufactures.manufacture_longname,
                            Tubes.tube_model, Tubes.focus, Tubes.capacity, Tubes.coolingrate, Tubes.servise_life, Image.name, Image.path,
                           db.func.group_concat(Technologies.technology_name).label('technology_name_list'))\
                           .join(Manufactures, Tomog.manufacture_id==Manufactures.id)\
                           .join(Tables, Tomog.table_id==Tables.id)\
                           .join(Generator, Tomog.generator_id==Generator.id)\
                           .join(Tubes, Tomog.tube_id==Tubes.id)\
                           .join(tomog_techno, Tomog.id==tomog_techno.c.tomog_id)\
                           .join(Technologies, tomog_techno.c.techno_id==Technologies.id)\
                           .join(Image, Tomog.image_id==Image.id)
                           .group_by(Tomog.id).filter(Manufactures.manufacture_name.in_(masss)).filter(Tomog.tubecount.in_(masss)).filter(Tomog.slicecount >=int(srez_l), Tomog.slicecount <=int(srez_h)))



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
    return render_template('hints.html',hints=Hints.query.all())

@app.route('/technologies', methods=['GET'])
def technologies():
    return render_template('technologies.html', manufactures=Manufactures.query.add_columns(Manufactures.manufacture_name).all(),
                           technologies=Technologies.query.join(Manufactures, Technologies.manufacture_id==Manufactures.id)\
                           .add_columns(Manufactures.manufacture_name, Technologies.technology_name, Technologies.technology_text).all())

@app.route('/compare', methods=['GET'])
def compare():

    return render_template('compare.html')