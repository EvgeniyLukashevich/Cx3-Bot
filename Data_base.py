import mysql.connector as sqdb


class DataBase():
    def __init__(self, base):
        self.base = base
        self.cur = self.base.cursor()
        # self.create_table('user_list')
        # self.create_table('quest_list')

    def create_table(self, list_select: str):
        match list_select:
            case 'user_list':
                self.base.execute(
                    f'CREATE TABLE IF NOT EXISTS user_list (user_id INT AUTO_INCREMENT PRIMARY KEY, dis_id, name, task, points, family)')
            case 'quest_list':
                self.base.execute(f'CREATE TABLE IF NOT EXISTS quest_list (quest_id PRIMARY KEY, task, answer)')
        self.base.commit()

    def get_user(self, list_select: str, *args):
        match list_select:
            case 'user_id':
                self.cur.execute(f'SELECT dis_id FROM user_list')
                return [tuple(elem) for elem in self.cur]
            case 'user':
                self.cur.execute(f'SELECT dis_id, name, task FROM user_list WHERE dis_id = {args[0]}')
                return [tuple(elem) for elem in self.cur]
            case 'task':
                self.cur.execute(f'SELECT task FROM user_list WHERE dis_id = {args[0]}')
                return [elem[0] for elem in self.cur]
            case 'status':
                self.cur.execute(f'SELECT status FROM user_list WHERE dis_id = {args[0]}')
                return [elem[0] for elem in self.cur]
            case 'date':
                self.cur.execute(f'SELECT date_reg FROM user_list WHERE dis_id = {args[0]}')
                return [elem[0] for elem in self.cur]
            case 'family':
                self.cur.execute(f'SELECT family FROM user_list WHERE dis_id = {args[0]}')
                return [elem[0] for elem in self.cur]

    def get_quest(self, list_select: str, language: str, number: int, *args):
        match list_select:
            case 'all':
                self.cur.execute(f'SELECT * FROM quest_list')
                return [tuple(elem) for elem in self.cur]
            case 'id':
                self.cur.execute(f'SELECT quest_id FROM quest_list')
                return [elem[0] for elem in self.cur]
            case 'quest':
                self.cur.execute(f'SELECT quest_id, task, answer FROM quest_list WHERE task = {args[0]}').fetchall()
            case 'task':
                self.cur.execute(f'SELECT {language} FROM quest_list WHERE quest_id = {number}')
                return [elem[0] for elem in self.cur]
            case 'answer':
                self.cur.execute(f'SELECT {language}1 FROM quest_list WHERE quest_id = {number}')
                return [elem for elem in self.cur][0]

    def add_item(self, list_select: str, new_item):
        match list_select:
            case 'new_user':
                self.cur.execute(
                    f'INSERT INTO user_list (dis_id, name, task, points, family, date_reg) VALUES (%s, %s, %s, %s, %s, %s)',
                    new_item)
                self.base.commit()
            case 'new_quest':
                self.cur.execute(f'INSERT INTO quest_list (task, answer) VALUES (%s, %s)', new_item)
                self.base.commit()

    def update_item(self, list_select: str, id, task):
        match list_select:
            case 'set_task':
                self.cur.execute(f'UPDATE user_list SET task = (%s) WHERE dis_id = (%s)', (task, id))
                self.base.commit()
            case 'set_family':
                self.cur.execute(f'UPDATE user_list SET family = (%s) WHERE dis_id = (%s)', (task, id))
                self.base.commit()

    def delete_item(self, id, list_select: str):
        match list_select:
            case 'user_list':
                self.cur.execute(f'DELETE FROM {list_select} WHERE dis_id = {id}')
            case 'quest_list':
                self.cur.execute(f'DELETE FROM {list_select} WHERE quest_id = {id}')
        self.base.commit()
