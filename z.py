from db_functions import Repository, Consultora
import psycopg2

#Repository(Consultora).write(numero="3",estado="Base")

z=Repository(Consultora).read_by_primary_key("31")

print(z)

