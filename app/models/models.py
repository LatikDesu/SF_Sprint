import sqlalchemy

metadata = sqlalchemy.MetaData()

coords_table = sqlalchemy.Table(
    "coords",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("scene_id", sqlalchemy.Integer, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("path_img", sqlalchemy.String(100)),
)

users_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("window_id", sqlalchemy.Integer),
    sqlalchemy.Column("scene_id", sqlalchemy.ForeignKey("scene.scene_id")),
    sqlalchemy.Column("text", sqlalchemy.String(1000), nullable=True),
    sqlalchemy.Column("character", sqlalchemy.String(100), nullable=True),
    sqlalchemy.Column("path_img", sqlalchemy.String(100), nullable=True),
    sqlalchemy.Column("position", sqlalchemy.String(100), nullable=True),
)
