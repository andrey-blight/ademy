from data.db_session import global_init, create_session
from data.db_models import User

global_init()
u = User(name="Andrey", surname="Kizhinov", age=17, sex=54)
s = create_session()
s.add(u)
s.commit()
