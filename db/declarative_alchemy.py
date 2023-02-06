from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.orm import mapped_column

from sqlalchemy import create_engine
from config import postgres as conf
from psycopg2.errors import UniqueViolation
from static.data import regions

def make_engine(user, password, host, port, db):
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    return engine

engine = make_engine(**conf)

class Base(DeclarativeBase):
    pass

class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True)

    region: Mapped[str] 

    def __repr__(self) -> str:
        return f"Region(id={self.id!r}, region={self.region!r})"

class Datafile(Base):
    __tablename__ = "datafile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    datafile: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Datafile(id={self.id!r}, datafile={self.datafile!r})"

class Vacancy(Base):
    __tablename__ = "vacancy"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    vacancy: Mapped[str] = mapped_column(String)
    region: Mapped[Optional[str]] = mapped_column(ForeignKey("region.id"))

    data: Mapped[Optional[str]] = mapped_column(ForeignKey("datafile.id"))

    def __repr__(self) -> str:
        return f"Vacancy(id={self.id!r}, vacancy={self.vacancy!r}, region={self.region!r}, data={self.data})"

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = Session(engine)


# region1 = Region(id=1, region = "Москва")
# region2 = Region(id=2, region = "Санкт-Петербург")
# region3 = Region(id=3, region = "Екатеринбург")
# region4 = Region(id=113, region = "Россия")
# region5 = Region(id=237, region = "Сочи")
# region6 = Region(id=1427, region = "Дербент")
# regions = [region1, region2, region3, region4, region5, region6]


#regions = [{'id': 1, 'region': 'Москва'}, {'id': 2, 'region': 'Санкт-Петербург'}, {'id': 3, 'region': 'Екатеринбург'}, {'id': 113, 'region': 'Россия'}, {'id': 237, 'region': 'Сочи'}, {'id': 1427, 'region': 'Дербент'}]

def create_regions_table():
    stmnt = insert(Region).values(regions).on_conflict_do_nothing()

    session.execute(stmnt)
    session.commit()

create_regions_table()


def save_request(vacancy_name, region, filename):
    if not session.query(Datafile).filter(Datafile.datafile == filename).all():
        datafile = Datafile(datafile=filename)
        session.add(datafile)
        session.flush()
    
   
        vacancy = Vacancy(vacancy=vacancy_name, region=region, data=datafile.id)
        session.add(vacancy)
        session.commit()

def return_built_info():
    vac_q = session.query(Vacancy)
    dat_q = session.query(Datafile)
    reg_q = session.query(Region)

    for vac in vac_q:
        table = [vac.vacancy, reg_q.get({"id": vac.region}).region, dat_q.get({"id": vac.data}).datafile]
        yield table




if __name__ == "__main__":
    print(list(return_built_info()))
    print(len(list(return_built_info())))
    

