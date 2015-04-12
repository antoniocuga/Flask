#from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, \
    Unicode, UnicodeText, CHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Entity = declarative_base()


class Persona(Entity):
    __tablename__ = 'personas'

    id = Column(Integer, primary_key=True)
    dni = Column(CHAR(20), nullable=False)
    nombre = Column(UnicodeText, nullable=False)
    empresa = relationship(
        'Empresa',
        secondary='empresa_persona'
    )


class Empresa(Entity):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True)
    ruc = Column(Unicode(255), nullable=False)
    razon_social = Column(UnicodeText, nullable=False)
    nombre_comercial = Column(UnicodeText, nullable=True)
    inicio_actividades = Column(DateTime)
    actividades_com_ext = Column(UnicodeText)
    telefono = Column(UnicodeText)
    fax = Column(UnicodeText)
    estado = Column(UnicodeText)
    condicion = Column(UnicodeText)
    direccion = Column(UnicodeText)
    total_ganado = Column(Numeric(15, 2), nullable=True)
    update = Column(Integer, default=0)
    persona = relationship(
        'Persona',
        secondary='empresa_persona'
    )


class Sucursal(Entity):
    __tablename__ = 'sucursales'

    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    tipo = Column(UnicodeText, nullable=False)
    direccion = Column(UnicodeText, nullable=False)


class Empresa_persona(Entity):
    __tablename__ = 'empresa_persona'

    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    persona_id = Column(Integer, ForeignKey('personas.id'))
    cargo = Column(UnicodeText, nullable=False)
    fecha_cargo = Column(DateTime)


class Departamento(Entity):
    __tablename__ = 'departamentos'

    id = Column(Integer, primary_key=True)
    departamento = Column(Unicode(255), nullable=False)


class Provincia(Entity):
    __tablename__ = 'provincias'

    id = Column(Integer, primary_key=True)
    provincia = Column(UnicodeText, nullable=False)


class Distrito(Entity):
    __tablename__ = 'distritos'

    id = Column(Integer, primary_key=True)
    distritos = Column(UnicodeText, nullable=False)


class TipoGobierno(Entity):
    __tablename__ = 'tipo_gobierno'

    id = Column(Integer, primary_key=True)
    tipo = Column(Unicode(255), nullable=False)


class Sectores(Entity):
    __tablename__ = 'sectores_gobierno'

    id = Column(CHAR(1), primary_key=True)
    sector = Column(UnicodeText, nullable=False)


class Pliegos(Entity):
    __tablename__ = 'pliegos_gobierno'

    id = Column(Integer, primary_key=True)
    pliego = Column(UnicodeText, nullable=False)

if __name__ == '__main__':

    from sqlalchemy import create_engine

    import settings

    engine = create_engine(
        settings.DATABASE_DSN,
        echo=settings.DEBUG
    )
    Entity.metadata.create_all(engine)
