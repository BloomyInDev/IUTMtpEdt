from mysql.connector import abstracts, connect, types as dbTypes
from typing import Any, Callable
from datetime import datetime


class Db:
	"""
	## Db class - Base of every class
	This class isn't meant to be called directly
	Instead, you must extend it
	"""

	def __init__(self) -> None:
		self.db = connect(
			host="127.0.0.1",
			port=3306,
			user="root",
			password="ThisPasswordIsntSecure",
			database="iutmtpedt",
			charset="utf8mb4",
			collation="utf8mb4_unicode_ci",
		)
		self.table = ""
		self.cur = self.db.cursor(prepared=True)
		pass

	def get_all(self) -> list[tuple]:
		self.cur.execute(f"SELECT * FROM {self.table}")
		return self.cur.fetchall()


class Professor(Db):
	def __init__(self) -> None:
		super().__init__()
		self.table = "Prof"

	def add(self, first_name: str, last_name: str) -> None:
		self.cur.execute(
			f"SELECT COUNT(*) FROM {self.table} WHERE prenom = %s AND nom = %s",
			(
				first_name,
				last_name,
			),
		)
		if self.cur.fetchall()[0][0] == 0:
			self.cur.execute(
				f"INSERT INTO {self.table} (prenom, nom) VALUES (%s, %s)",
				(
					first_name,
					last_name,
				),
			)
			self.db.commit()
		return

	def get(
		self, first_name: str | None = None, last_name: str | None = None
	) -> list[tuple[int, str, str]]:
		# assert (
		#    (first_name == None and last_name != None)
		#    or
		#    (first_name != None and last_name == None)
		# ), "You can't give me nothing to get someone :("

		result = None

		if first_name != None and last_name != None:
			self.cur.execute(
				f"SELECT * FROM {self.table} WHERE prenom = %s AND nom = %s",
				(first_name, last_name),
			)
			result = self.cur.fetchall()

		elif last_name == None:
			self.cur.execute(f"SELECT * FROM {self.table} WHERE nom = %s", (last_name,))
			result = self.cur.fetchall()

		elif first_name == None:
			self.cur.execute(
				f"SELECT * FROM {self.table} WHERE prenom = %s", (first_name,)
			)
			result = self.cur.fetchall()

		return result

	def get_all_names(self) -> list[tuple[str, str]]:
		"""
		Get all professors in order (lastname, firstname)

		Returns:
			list[tuple[str,str]]: list of all professors in db
		"""
		self.cur.execute(f"SELECT nom, prenom FROM {self.table}")
		return self.cur.fetchall()


class Group(Db):
	def __init__(self) -> None:
		super().__init__()
		self.table = "Classe"

	def add(self, name: str) -> None:
		self.cur.execute(f"SELECT COUNT(*) FROM {self.table} WHERE nom = %s", (name,))
		if self.cur.fetchall()[0][0] == 0:
			self.cur.execute(
				f"INSERT INTO {self.table} (nom) VALUES (%s)",
				(name,),
			)
			self.db.commit()
		return

	def get(self, name: str):
		self.cur.execute(f"SELECT * FROM {self.table} WHERE nom = %s", (name,))
		return self.cur.fetchall()

	def get_all_names(self) -> list[tuple[str]]:
		"""
		Get all groups

		Returns:
			list[tuple[str,str]]: list of all professors in db
		"""
		self.cur.execute(f"SELECT nom FROM {self.table}")
		return self.cur.fetchall()


class Event(Db):
	def __init__(self) -> None:
		super().__init__()
		self.table = "Cours"
		self.prof_link_table = "Enseigner"
		self.group_link_table = "Participants"
		self.prof_db = Professor()
		self.group_db = Group()

	def add(
		self,
		name: str,
		timeStart: int,
		timeEnd: int,
		profs: list[tuple[str, str]],
		groups: list[str],
		place: str,
		color: str,
	) -> None:
		"""
		Add an event in the database

		Args:
			name (str): Name of the event
			timeStart (int): Start date of the event
			timeEnd (int): End date of the event
			profs (list[tuple[str,str]]): Last and first name of professors
		"""
		prof_ids = []
		for prof in profs:
			if not (prof in self.prof_db.get_all_names()):
				self.prof_db.add(prof[1], prof[0])
			prof_ids.append(self.prof_db.get(prof[1], prof[0])[0][0])

		group_ids = []
		for group in groups:
			if not ((group,) in self.group_db.get_all_names()):
				self.group_db.add(group)
			group_ids.append(self.group_db.get(group)[0][0])

		self.cur.execute(
			f"SELECT COUNT(*) FROM {self.table} WHERE name = %s AND timeStart = %s AND timeEnd = %s AND place = %s",
			(name, timeStart, timeEnd, place),
		)
		if self.cur.fetchall()[0][0] == 0:
			self.cur.execute(
				f"INSERT INTO {self.table} (name, timeStart, timeEnd, place, color) VALUES (%s, %s, %s, %s, %s)",
				(name, timeStart, timeEnd, place, color),
			)
			self.db.commit()
		self.cur.execute(
			f"SELECT id FROM {self.table} WHERE name = %s AND timeStart = %s AND timeEnd = %s",
			(name, timeStart, timeEnd),
		)
		event_id = self.cur.fetchall()[0][0]

		for group_id in group_ids:
			self.cur.execute(
				f"SELECT COUNT(*) FROM {self.group_link_table} WHERE idClasse = %s AND idCours = %s",
				(group_id, event_id),
			)
			if self.cur.fetchall()[0][0] == 0:
				self.cur.execute(
					f"INSERT INTO {self.group_link_table} (idClasse, idCours) VALUES (%s, %s)",
					(group_id, event_id),
				)
				self.db.commit()

		for prof_id in prof_ids:
			self.cur.execute(
				f"SELECT COUNT(*) FROM {self.prof_link_table} WHERE idProf = %s AND idCours = %s",
				(prof_id, event_id),
			)
			if self.cur.fetchall()[0][0] == 0:
				self.cur.execute(
					f"INSERT INTO {self.prof_link_table} (idProf, idCours) VALUES (%s, %s)",
					(prof_id, event_id),
				)
				self.db.commit()

		return
