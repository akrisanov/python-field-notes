# Reflecting a Database with Automap ---------------------------------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()

engine = create_engine("sqlite:///Chinook.sqlite")

# scan everything available on the engine we just created, and reflect everything it can
Base.prepare(engine, reflect=True)

# ORM objects for each table that is accessible under the class property of the automap Base
Base.classes.keys()
# [
#     "Album",
#     "Customer",
#     "Playlist",
#     "Artist",
#     "Track",
#     "Employee",
#     "MediaType",
#     "InvoiceLine",
#     "Invoice",
#     "Genre",
# ]
Artist = Base.classes.Artist
Album = Base.classes.Album

Session = sessionmaker(bind=engine)
session = Session()

for artist in session.query(Artist).limit(10):
    print(artist.ArtistId, artist.Name)

# When automap creates a relationship, it creates a <related_object>_collection property on the object:
artist = session.query(Artist).first()

for album in artist.album_collection:
    print("{} - {}".format(artist.Name, album.Title))
