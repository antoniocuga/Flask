from flask import Flask, g, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import settings
import models
#import import_sunat
import import_representante

app = Flask(
    __name__,
    static_folder=settings.STATIC_PATH,
    static_url_path=settings.STATIC_URL_PATH
)
db_engine = create_engine(
    settings.DATABASE_DSN,
    echo=settings.DEBUG
)


@app.before_request
def before_request():
    g.db = sessionmaker(
        bind=db_engine
    )()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET', 'POST'])
def index():

    proveedores = g.db.query(
        models.Empresa.id,
        models.Empresa.ruc,
        models.Empresa.razon_social,
        models.Empresa.total_ganado
    ).order_by(
        models.Empresa.total_ganado.desc()
    ).limit(200)

    return render_template(
        'index.html',
        proveedores=proveedores,
    )


@app.route('/empresas', methods=['GET', 'POST'])
def empresas():

    proveedores = g.db.query(
        models.Empresa.id,
        models.Empresa.ruc,
        models.Empresa.razon_social,
        models.Empresa.total_ganado
    ).order_by(
        models.Empresa.total_ganado.desc()
    ).limit(25)

    return render_template(
        'empresas.html',
        proveedores=proveedores,
    )


@app.route('/proveedor/<int:id>')
def proveedor(id):

    proveedor = g.db.query(
        models.Empresa
    ).filter(
        models.Empresa.id == id
    ).first()

    emp_per = g.db.query(
        models.Empresa_persona
    ).filter(
        models.Empresa_persona.empresa_id == id
    )

    if emp_per.count() == 0:
        representanteClass = import_representante.importRepresentante()
        proveedor.representantes = representanteClass.save(proveedor.ruc, id)
    else:
        representantes = g.db.query(
            models.Empresa_persona
        ).filter(
            models.Empresa_persona.empresa_id == id
        ).order_by(
            models.Empresa_persona.fecha_cargo.desc()
        ).join(
            models.Persona
        ).values(
            models.Persona.id,
            models.Persona.dni,
            models.Persona.nombre,
            models.Empresa_persona.cargo,
            models.Empresa_persona.fecha_cargo
        )

        proveedor.representantes = representantes

    return render_template(
        'proveedor.html',
        proveedor=proveedor,
    )


@app.route('/representante/<int:id>')
def representante(id):

    representante = g.db.query(
        models.Persona
    ).filter(
        models.Persona.id == id
    ).first()

    empresas = g.db.query(
        models.Empresa_persona
    ).order_by(
            models.Empresa_persona.fecha_cargo.desc()
    ).filter(
        models.Empresa_persona.persona_id == id
    ).join(
        models.Persona,
        models.Empresa
    ).values(
        models.Empresa.id,
        models.Empresa.razon_social,
        models.Empresa.ruc,
        models.Empresa.total_ganado,
        models.Empresa_persona.cargo,
        models.Empresa_persona.fecha_cargo
    )

    representante.empresas = empresas

    return render_template(
        'representante.html',
        representante=representante,
    )

if __name__ == '__main__':
    app.run(
        debug=settings.DEBUG,
    )

