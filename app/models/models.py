import sqlalchemy

metadata = sqlalchemy.MetaData()

coords_table = sqlalchemy.Table(
    "coords",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("latitude", sqlalchemy.Float),
    sqlalchemy.Column("longitude", sqlalchemy.Float),
    sqlalchemy.Column("height", sqlalchemy.Integer),
)

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("email", sqlalchemy.String(100), unique=True, nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String(100)),
    sqlalchemy.Column("last_name", sqlalchemy.String(100)),
    sqlalchemy.Column("patronymic", sqlalchemy.String(100)),
    sqlalchemy.Column("phone", sqlalchemy.String(100)),
)

ActivitiesTypes_table = sqlalchemy.Table(
    "activities_types",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("title", sqlalchemy.String(100)),
)

PerevalAreas_table = sqlalchemy.Table(
    "pereval_areas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("id_parent", sqlalchemy.Integer),
    sqlalchemy.Column("title", sqlalchemy.String(100)),
)

pereval_add_table = sqlalchemy.Table(
    "pereval_add",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("status", sqlalchemy.String(10), nullable=False, server_default="new"),
    sqlalchemy.Column("coords_id", sqlalchemy.Integer, sqlalchemy.ForeignKey('coords.id'), nullable=False),
    sqlalchemy.Column("beauty_title", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("other_titles", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("connect", sqlalchemy.Text),
    sqlalchemy.Column("add_time", sqlalchemy.DateTime(), server_default=sqlalchemy.func.now(), nullable=False),
    sqlalchemy.Column("level_winter", sqlalchemy.String(255)),
    sqlalchemy.Column("level_summer", sqlalchemy.String(255)),
    sqlalchemy.Column("level_autumn", sqlalchemy.String(255)),
    sqlalchemy.Column("level_spring", sqlalchemy.String(255)),
    sqlalchemy.Column("user_id", sqlalchemy.Integer(), sqlalchemy.ForeignKey('users.id'), nullable=False),
)

images_table = sqlalchemy.Table(
    "pereval_images",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("pereval", sqlalchemy.ForeignKey("pereval_add.id")),
    sqlalchemy.Column("data", sqlalchemy.String(100)),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("data_added", sqlalchemy.DateTime, server_default=sqlalchemy.func.now(), nullable=False),
)
